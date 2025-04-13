from fastapi import APIRouter, File, UploadFile, HTTPException
from google.cloud import storage
from typing import List
import os

BUCKET_NAME = "ml-dataset-veroxe"
SCHEMA_FOLDER = "schemas/"

router = APIRouter()

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

@router.post("/schemas/upload")
async def upload_schema(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed.")
    
    blob = bucket.blob(SCHEMA_FOLDER + file.filename)
    blob.upload_from_file(file.file, content_type="application/json")

    return {"message": f"Schema '{file.filename}' uploaded successfully."}

@router.get("/schemas")
def list_schemas() -> List[str]:
    blobs = storage_client.list_blobs(BUCKET_NAME, prefix=SCHEMA_FOLDER)
    return [blob.name.replace(SCHEMA_FOLDER, "") for blob in blobs]

@router.delete("/schemas/{filename}")
def delete_schema(filename: str):
    blob = bucket.blob(SCHEMA_FOLDER + filename)
    if not blob.exists():
        raise HTTPException(status_code=404, detail="Schema not found.")
    blob.delete()
    return {"message": f"Schema '{filename}' deleted successfully."}
