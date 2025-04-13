from fastapi import FastAPI
from schemas_api import router as schemas_router

app = FastAPI()
app.include_router(schemas_router, prefix="/api")
