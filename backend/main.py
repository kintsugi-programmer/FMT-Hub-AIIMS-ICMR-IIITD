from fastapi import FastAPI, Form, UploadFile, File
import shutil
import os
import mysql.connector
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve the 'uploads' folder as static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Database Connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="new_user",
        password="new_password",
        database="google_form"
    )

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/submit-form/")
async def submit_form(
    text1: str = Form(...),
    text2: str = Form(...),
    text3: str = Form(...),
    file: UploadFile = File(...)
):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO forms (text1, text2, text3, file_path) VALUES (%s, %s, %s, %s)",
        (text1, text2, text3, file_path)
    )
    db.commit()
    db.close()

    return {"message": "Form submitted successfully", "file_path": file_path}


# Define response model
class FormResponse(BaseModel):
    id: int
    text1: str
    text2: str
    text3: str
    file_path: str

@app.get("/get-forms/", response_model=List[FormResponse])
def get_forms():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM forms")
    forms = cursor.fetchall()
    
    db.close()
    return forms