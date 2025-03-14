Here’s your **final, in-depth documentation** covering everything from setting up the **FastAPI + Next.js project**, including **Linux console commands, file structure, processes, and deployment**.

---

# 🚀 **Full Development Documentation**
## **Project: Google Forms Clone (FastAPI + Next.js + MySQL)**  

### 📌 **Overview**
- **Backend:** FastAPI (Python) + MySQL
- **Frontend:** Next.js 14 (React + TypeScript)
- **Hosting Options:** Ngrok (temporary), Nginx (permanent), VPS (cloud)

---

## **1️⃣ Folder & File Structure**
```
📂 Project-Root/
│
├── 📂 backend/                     # FastAPI Backend
│   ├── main.py                     # FastAPI application
│   ├── database.py                  # MySQL connection
│   ├── models.py                    # Database models
│   ├── routes.py                    # API endpoints
│   ├── uploads/                      # Stored media files (ignored in Git)
│   ├── logs/                         # Log files (ignored in Git)
│   ├── venv/                         # Virtual environment (ignored in Git)
│   ├── .gitignore                    # Git ignore for backend
│   ├── requirements.txt              # Python dependencies
│
├── 📂 frontend/                     # Next.js 14 Frontend
│   ├── src/                          # Main source directory
│   │   ├── app/                      # Pages directory
│   │   │   ├── page.tsx              # Home page (Form submission)
│   │   │   ├── view/page.tsx         # View submissions page
│   │   ├── components/               # Reusable components
│   │   ├── styles/                   # Global styles
│   ├── public/                        # Static assets
│   ├── .gitignore                     # Git ignore for frontend
│   ├── package.json                    # Node.js dependencies
│   ├── next.config.js                   # Next.js configuration
│
├── 📂 deployment/                     # Deployment scripts
│   ├── nginx.conf                      # Nginx configuration
│   ├── docker-compose.yml               # Docker setup (if needed)
│
├── README.md                            # Project documentation
```

---

## **2️⃣ FastAPI Backend Setup (Linux)**
### 🔹 **Step 1: Create & Activate Virtual Environment**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 🔹 **Step 2: Install Dependencies**
```bash
pip install fastapi uvicorn mysql-connector-python python-multipart
```

### 🔹 **Step 3: Create `main.py`**
```python
from fastapi import FastAPI, Form, UploadFile, File
import shutil, os, mysql.connector
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# MySQL Connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="new_user",
        password="new_password",
        database="google_form"
    )

@app.post("/submit-form/")
async def submit_form(
    text1: str = Form(...),
    text2: str = Form(...),
    text3: str = Form(...),
    file: UploadFile = File(...)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO forms (text1, text2, text3, file_path) VALUES (%s, %s, %s, %s)",
                   (text1, text2, text3, file_path))
    db.commit()
    db.close()
    return {"message": "Form submitted", "file_path": file_path}

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
```

### 🔹 **Step 4: Start FastAPI**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## **3️⃣ MySQL Setup**
### 🔹 **Step 1: Create Database & User**
```bash
mysql -u root -p
```
```sql
CREATE DATABASE google_form;
CREATE USER 'new_user'@'localhost' IDENTIFIED BY 'new_password';
GRANT ALL PRIVILEGES ON google_form.* TO 'new_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 🔹 **Step 2: Create Table**
```sql
USE google_form;
CREATE TABLE forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text1 TEXT,
    text2 TEXT,
    text3 TEXT,
    file_path TEXT
);
```

---

## **4️⃣ Next.js 14 Frontend Setup**
### 🔹 **Step 1: Install Next.js**
```bash
cd frontend
npx create-next-app@latest frontend
cd frontend
npm install axios
```

### 🔹 **Step 2: Create `app/page.tsx`**
```tsx
"use client";
import { useState } from "react";
import axios from "axios";

export default function Home() {
    const [formData, setFormData] = useState({ text1: "", text2: "", text3: "", file: null });

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });
    const handleFileChange = (e) => setFormData({ ...formData, file: e.target.files[0] });

    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = new FormData();
        data.append("text1", formData.text1);
        data.append("text2", formData.text2);
        data.append("text3", formData.text3);
        data.append("file", formData.file);

        try {
            const response = await axios.post("http://localhost:8000/submit-form/", data, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            alert(response.data.message);
        } catch (error) {
            console.error("Error submitting form", error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="text1" placeholder="Text 1" onChange={handleChange} />
            <input type="text" name="text2" placeholder="Text 2" onChange={handleChange} />
            <input type="text" name="text3" placeholder="Text 3" onChange={handleChange} />
            <input type="file" name="file" onChange={handleFileChange} />
            <button type="submit">Submit</button>
        </form>
    );
}
```

### 🔹 **Step 3: Run Next.js**
```bash
npm run dev
```

---

## **5️⃣ Deployment with Ngrok**
```bash
ngrok http 8000
```
It generates:
```
https://random-name.ngrok.io
```
Update Next.js API URL:
```tsx
const API_URL = "https://random-name.ngrok.io";
```

---
## **✅ Final Steps**
- **FastAPI**: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **MySQL Check**: `mysql -u new_user -p`
- **Frontend**: `npm run dev`
- **Global Access**: `ngrok http 8000`

🚀 **You’re done!** Let me know if you need further tweaks. 😊