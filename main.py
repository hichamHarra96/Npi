from fastapi import FastAPI

from controller import npi_controller
from database.connection import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(npi_controller.router, prefix="/api")
