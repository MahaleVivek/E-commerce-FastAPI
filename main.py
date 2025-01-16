from fastapi import FastAPI
from routers import seller, product, order, customer, wallet
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Initialize the database
Base.metadata.create_all(bind=engine)

# Include routers
# These routers will be responsible for different functionalities such as seller, product, order, etc.
app.include_router(seller.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(customer.router)
app.include_router(wallet.router)

@app.get("/")
def read_root():
    """
    The root endpoint of the application. Returns a welcome message.
    """
    return {"message": "Welcome to the Amazon Seller Page API"}


# Allow all origins for now, or restrict it to specific URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve static files
#app.mount("/static", StaticFiles(directory="static"), name="static")
