from fastapi import APIRouter, Depends, HTTPException, status
from app.services.db_service import db_dependency
from app.models.auth_model import User
from app.validations.auth_validations import (
    UserCreate,
    TokenData,
    UserResponse,
    UserRole,
)
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from app.services.utils import send_password_reset_email
from typing import List

auth_router = APIRouter(tags=["Auth"])

SECRET_KEY = "Abc1abc2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception


def get_current_user_role(current_user: dict = Depends(verify_token)):
    return current_user.get("role")


# # Dependency to check if the user has admin privileges
def check_admin_privilege(role: str = Depends(get_current_user_role)):
    if role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privilege required"
        )
    return role


# # Dependency to check if the user has shop owner privileges
def check_shop_owner_privilege(role: str = Depends(get_current_user_role)):
    if role == UserRole.shop_owner:
        return role


# Dependency to check if the user has customer privileges
def check_customer_privilege(role: str = Depends(get_current_user_role)):
    if role != UserRole.customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Customer privilege required"
        )
    return role


# Dependency to check if the user has Admin or customer privileges
def check_admin_or_customer(role: str = Depends(get_current_user_role)):
    if role in (UserRole.admin, UserRole.customer):
        return role


# Dependency to check if the user has Admin or Shop Owner privileges
def check_admin_or_shop_owner(role: str = Depends(get_current_user_role)):
    if role in (UserRole.admin, UserRole.shop_owner):
        return role


# Dependency to check if the user has Customer or Shop Owner privileges
def check_customer_or_shop_owner(role: str = Depends(get_current_user_role)):
    if role in (UserRole.customer, UserRole.shop_owner):
        return role


# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: db_dependency, email: str):
    return db.query(User).filter(User.email == email).first()


# Function to get current user from token
def get_current_user(db: db_dependency, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


# Function to get current active user
def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


# Function to generate password reset token
def generate_password_reset_token(email: str) -> str:
    expire_time = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"sub": email, "exp": expire_time}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@auth_router.post("/register")
def register_user(db: db_dependency, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}


@auth_router.post("/login")
def login_user(
    db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/get_profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_active_user)):
    return current_user


@auth_router.get("/get_all_user", response_model=List[UserResponse])
def get_all_user(
    db: db_dependency,
    shop_owner_id: int = None,
    current_user: User = Depends(get_current_active_user),
):
    if current_user.role == UserRole.admin:
        if shop_owner_id is not None:
            shop_owner = (
                db.query(User)
                .filter(User.id == shop_owner_id, User.role == UserRole.shop_owner)
                .first()
            )
            if not shop_owner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Shop owner is Not Found",
                )
            return shop_owner
        else:
            shop_owners = db.query(User).filter(User.role == UserRole.shop_owner).all()
            return shop_owners
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin Privilege requiredx"
        )


@auth_router.put("/update_profile")
def update_profile(
    db: db_dependency,
    is_active: bool,
    shop_owner_id: int = None,
    current_user: User = Depends(get_current_active_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin Privilege required"
        )
    shop_owner = (
        db.query(User)
        .filter(User.id == shop_owner_id, User.role == UserRole.shop_owner)
        .first()
    )
    if not shop_owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop owner is Not Found"
        )
    shop_owner.is_active = is_active
    db.commit()
    return {"message": "User Profile Updated Successfully "}


@auth_router.put("/change-password")
def change_user_password(
    db: db_dependency,
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
):
    if not verify_password(old_password, current_user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid current password",
        )
    hashed_password = pwd_context.hash(new_password)
    current_user.password = hashed_password
    db.commit()
    return {"message": "Password changed successfully"}


@auth_router.post("/reset-password-mail")
def send_password_reset_mail(db: db_dependency, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reset_token = generate_password_reset_token(user.email)
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
    send_password_reset_email(email, reset_link)
    return {"message": "Password reset email sent successfully"}
