import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config.db_config import engine
from app.models import auth_model, cart_model, order_model, product_model
from app.routes.auth_routes import auth_router
from app.routes.address_route import address_router
from app.routes.cart_route import cart_router
from app.routes.order_route import order_router
from app.routes.product_route import product_router
from app.routes.review_rating_route import review_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    docs_url="/api/v1/docs",
    # docs_url="/api/v2/docs",
    redoc_url="/api/v1/redoc",
    # redoc_url="/api/v2/redoc",
    title="Online Grocery Store",
    version="1.0",
    # version="2.0",
    openapi_url="/api/v1/openapi.json",
    # openapi_url="/api/v2/openapi.json",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Static file setup config
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["Home"])
def home():
    return {"message" : "Welcome to Online Grocery Store"}

auth_model.Base.metadata.create_all(bind = engine)
cart_model.Base.metadata.create_all(bind = engine)
order_model.Base.metadata.create_all(bind = engine)
product_model.Base.metadata.create_all(bind = engine)

app.include_router(auth_router)
app.include_router(address_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(product_router)
app.include_router(review_router)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8000, 
                reload=True
            )
    