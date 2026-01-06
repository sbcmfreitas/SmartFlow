from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models, database, utils
from app.routers import transactions, auth

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Define database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SmartFlow API")

@app.on_event("startup")
def on_startup():
    logger.info("Starting SmartFlow API...")


# Configure CORS
origins = ["*"] # Adjust in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    db = database.SessionLocal()
    try:
        utils.create_initial_user(db)
    finally:
        db.close()

app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "SmartFlow API is running"}
