# Running the project with Docker

- In order to run the project, you first must have docker installed on your machine

- Next, ensure the docker application is running

- Navigate to the root directory of the project and run 'docker-compose up --build' if first time or 'docker-compose up' if running again

- Please note: If you get a package not found issue in the frontend, try doing npm install inside the frontend folder to get all dependencies. Then rerun the docker build command.

- This command will build the docker containers as well as any needed dependencies for the project as specified in requirements.txt

- Once the build finishes it will be running automatically

- Use ^C to stop the application running

---
# Running the project without Docker
- **Frontend**
 - Naviagte to frontend folder
 - Once you are in the frontend folder run 'npm install'
 - Run 'npm start'after previous step complete
 

 - **Backend**
 - Open a new terminal
 - Navigate to the backend folder
 - Once you are in the backend foldr run 'pip install -r requirements.txt'
 - Wait for it to finish, then run 'python -m uvicorn app:app --reload'

 ---

# Running frontend unit tests
1. Open new terminal that is in root directory
2. Run 'docker exec -it resume_analyzer_490_outsiders-frontend-1 sh'
3. You are now in shell of frontend container
4. Now run 'npm test'
5. Wait for results to show up 
 
---

# Running frontend E2E tests with Playwright
1. Open new terminal that is in root directory
2. Run 'docker exec -it resume_analyzer_490_outsiders-frontend-1 sh'
3. You are now in shell of frontend container
4. Now run 'npx playwright test'
5. Wait for results to show up 

---

# Running the backend only
python3 -m uvicorn app:app --reload to run the api
http://127.0.0.1:8000/docs for easy testing of the api - use try it out button

Backend API Documentation
### **1. GET /**
- **Description**: Root endpoint.
- Response:
```json

{
  "Hello": "World"
}
```

### **2. GET /api**
- **Description**: API status check.
- Response:
```json
{
  "Hello": "API"
}
```

### **3. POST /api/register**
- **Description**: Registers a new user.
- Request Body (JSON):
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "username": "username"
}
```

- Response:
```json
{
  "message": "User registered successfully"
}
```

### **4. POST /api/login**
- **Description** : Logs in an existing user.
- Request Body (JSON):
``` json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```
- Response:
```json
{
  "token": "<JWT_token>"
}
```
### **5. POST /api/resume-upload**
- **Description**: Uploads and processes a resume file.
- Request:
- File upload: Accepts application/pdf or application/vnd.openxmlformats-officedocument.wordprocessingml.document.
- Response:
```json
{
  "message": "Resume uploaded and processed successfully.",
  "extracted_text": "<Extracted text from the resume>"
}
```

### **6. POST /api/job-description**
- **Description**: Submits a job description.
- Request Body (JSON):
```json
{
  "text": "Job description text"
}
```
- Response:
```json
{
  "message": "Text submitted successfully",
  "character_count": 123
}
```

### **7. POST /api/fit-score**
- **Description**: Calculates fit score between a resume and job description.
- Request Body (JSON):
```json
{
  "resume_text": "Extracted resume text",
  "job_description": "Job description text"
}
```
- Response:
```json
{
  "similarity_score": 85.0,
  "keywords_matched": ["skill1", "skill2"],
  "feedback_raw": ["feedback1", "feedback2"]
}
```
### **8. POST /api/analyze**
- **Description**: Performs detailed analysis of a resume and job description.
- Request Body (JSON):
```json
{
  "resume_text": "Extracted resume text",
  "job_description": "Job description text"
}
```
- Response:
```json
{
  "similarity_score": 85.0,
  "keywords_matched": ["skill1", "skill2"],
  "feedback_raw": ["feedback1", "feedback2"]
}
```
