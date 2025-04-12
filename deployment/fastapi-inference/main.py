import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Veroxe API is running"}


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))  # This line is essential!
    uvicorn.run("main:app", host="0.0.0.0", port=port)