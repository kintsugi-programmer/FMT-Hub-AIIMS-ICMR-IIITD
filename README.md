# FMT-Hub-AIIMS-ICMR-IIITD
A scalable web platform for the FMT Centre of Excellence, funded by the Indian Council of Medical Research (ICMR) and All India Institute of Medical Sciences (AIIMS), enabling centralized data access and visualizations. Developed under Prof. Dr. Tarini Shankar Ghosh and RA Omprakash at IIIT Delhi.

This is a well-structured plan for the **FMT Hub** project. Given the requirements, here's a breakdown of how the **backend (FastAPI + MySQL) and frontend (Next.js 14 + TypeScript, Tailwind, ShadCN)** can be designed.

---

### **1. User Roles & Authentication**
- **Agents** (Data Entry)
- **Central Readers** (Validation & Scoring)
- **Super Admin** (View & Edit Everything)

#### **Authentication System**
- JWT-based authentication using FastAPI.
- Each user logs in with their **username (Agent ID/Center Code) and password**.
- Access control will be enforced based on roles.

---

### **2. Database Schema (MySQL)**
Here’s an outline of the key tables:
```sql
CREATE DATABASE fmt_hub;
USE fmt_hub;

-- Centers Table: Stores medical center details
CREATE TABLE centers (
    center_code VARCHAR(2) PRIMARY KEY,
    center_name VARCHAR(100) NOT NULL
);

-- Users Table: Stores login credentials and roles (agents, central readers, super admin)
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('agent', 'central_reader', 'super_admin') NOT NULL,
    center_code VARCHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (center_code) REFERENCES centers(center_code) ON DELETE CASCADE
);

-- Tests Table: Stores test data for each patient
CREATE TABLE tests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_mask_id VARCHAR(50) UNIQUE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    trial_id ENUM('ALTER_UC', 'ALTER_CD', 'BOOST_UC', 'BOOST_CD') NOT NULL,
    center_code VARCHAR(2) NOT NULL,
    agent_id INT NOT NULL,
    submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    test_id VARCHAR(50) UNIQUE NOT NULL,
    screening_no INT NOT NULL,
    sample_space_time ENUM('0', '10', '48') NOT NULL,
    collection_time DATETIME NOT NULL,
    agent_score FLOAT NOT NULL,
    final_score FLOAT NULL,
    status ENUM('pending', 'finalized') DEFAULT 'pending',
    endoscopy_media_url TEXT NOT NULL,
    agent_review TEXT NULL,
    FOREIGN KEY (agent_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (center_code) REFERENCES centers(center_code) ON DELETE CASCADE
);

-- Scores Table: Stores scoring done by central readers
CREATE TABLE scores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    test_id INT NOT NULL,
    reader_id INT NOT NULL,
    score FLOAT NOT NULL,
    status ENUM('pending', 'confirmed') DEFAULT 'pending',
    reader_review TEXT NULL,
    FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE,
    FOREIGN KEY (reader_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Score Validation Table: Stores the final decision-making process
CREATE TABLE score_validation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    test_id INT NOT NULL,
    agent_score FLOAT NOT NULL,
    reader1_id INT NOT NULL,
    reader1_score FLOAT NOT NULL,
    reader2_id INT NULL,
    reader2_score FLOAT NULL,
    final_score FLOAT NOT NULL,
    status ENUM('pending', 'finalized') DEFAULT 'pending',
    FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE,
    FOREIGN KEY (reader1_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reader2_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert predefined centers
INSERT INTO centers (center_code, center_name) VALUES
('01', 'AIIMS, New Delhi'),
('02', 'BHU, Varanasi'),
('03', 'DMC, Ludhiana'),
('04', 'Lisie Hospital, Kochi'),
('05', 'LTMGH & LTMMC, Mumbai'),
('06', 'PGI, Chandigarh');

-- Insert predefined users with hashed passwords (passwords need to be hashed in the application before insertion)
INSERT INTO users (username, password_hash, role, center_code) VALUES
('agent01', 'hashed_password_01', 'agent', '01'),
('agent02', 'hashed_password_02', 'agent', '02'),
('agent03', 'hashed_password_03', 'agent', '03'),
('agent04', 'hashed_password_04', 'agent', '04'),
('agent05', 'hashed_password_05', 'agent', '05'),
('agent06', 'hashed_password_06', 'agent', '06'),
('reader01', 'hashed_password_07', 'central_reader', '01'),
('reader02', 'hashed_password_08', 'central_reader', '02'),
('reader03', 'hashed_password_09', 'central_reader', '03'),
('reader04', 'hashed_password_10', 'central_reader', '04'),
('reader05', 'hashed_password_11', 'central_reader', '05'),
('reader06', 'hashed_password_12', 'central_reader', '06'),
('superadmin', 'hashed_superadmin_password', 'super_admin', '01');
```

---

### **3. Backend (FastAPI)**
#### **Key Endpoints**
- **Authentication**
  - `/auth/login`
  - `/auth/register` (Only for super admin)
- **Agent APIs**
  - `/agents/submit-patient`
  - `/agents/submit-test`
- **Central Reader APIs**
  - `/central-reader/get-tests`
  - `/central-reader/submit-score`
- **Super Admin APIs**
  - `/super-admin/get-all-tests`
  - `/super-admin/update-test`

#### **Scoring Algorithm**
- If the **central reader's score** matches the agent's score → **finalized**.
- If not, a second reader scores.
- If two scores match → **finalized**.
- If all three are different → **average score** is used.

---

### **4. Frontend (Next.js 14 + ShadCN + Tailwind)**
#### **Key Pages**
1. **Login Page**: `/login`
2. **Agent Dashboard**: `/agent`
   - Form to enter patient and test data.
   - Upload for endoscopy media.
   - Submit button (data locked after submission).
3. **Central Reader Dashboard**: `/reader`
   - View assigned tests.
   - Review images/videos.
   - Provide scores.
   - Pending list for second opinions.
4. **Super Admin Panel**: `/admin`
   - View all tests.
   - Edit or update test data.

---

### **5. File Storage**
- Store **endoscopy images/videos** in a **local server** or **AWS S3 bucket**.
- Save the file URL in the `tests` table.

---

### **6. Deployment**
- **Backend**: DigitalOcean (FastAPI + MySQL)
- **Frontend**: Vercel (Next.js 14)
- **Database**: Managed MySQL (DigitalOcean or AWS RDS)

---

### **7. Next Steps**
1. **Setup FastAPI authentication & database models**.
2. **Develop API endpoints for patient and test data submission**.
3. **Implement Next.js frontend with role-based access control**.
4. **Integrate scoring validation logic**.
5. **Deploy backend and frontend**.

Would you like me to generate the FastAPI codebase for authentication and data handling first? 🚀