#Running the Project Locally

To run the project locally, follow the steps below:

1. Install Docker
Ensure Docker is installed and running on your machine.  

2. 
Navigate to your desired directory in the terminal and clone the project repository:  
git clone https://github.com/justinab24/resume-analyzer.git
cd resume-analyzer

3. Environment Configuration
Navigate to the backend folder and create a `.env` file:
HUGGINGFACE_API_KEY= API Key
JWT_SECRET_KEY= Secret Key
OPENAI_API_KEY= Secret Key

4. Build and run with Docker
Navigate to the root directory of the project and run 'docker-compose up --build' if first time or 'docker-compose up' if running again

5. Trouble shooting
Please note: If you get a package not found issue in the frontend, try doing npm install inside the frontend folder to get all dependencies. Then rerun the docker build command.

This command will build the docker containers as well as any needed dependencies for the project as specified in requirements.txt

Once the build finishes it will be running automatically

Use ^C to stop the application running

Application Access:
Backend: The backend API runs at `http://127.0.0.1:8000`.
Frontend: Access the frontend application at `http://127.0.0.1:3000`.  
API Documentation: View Swagger UI at `http://127.0.0.1:8000/docs`.

# Running the backend only
python3 -m uvicorn app:app --reload to run the api
http://127.0.0.1:8000/docs for easy testing of the api - use try it out button

Backend API Documentation
1. GET /
Description: Root endpoint.
Response:
json

{
  "Hello": "World"
}
2. GET /api
Description: API status check.
Response:
json
{
  "Hello": "API"
}
3. POST /api/register
Description: Registers a new user.
Request Body (JSON):
json
{
  "email": "user@example.com",
  "password": "securepassword",
  "username": "username"
}
Response:
json
{
  "message": "User registered successfully"
}
4. POST /api/login
Description: Logs in an existing user.
Request Body (JSON):
json
{
  "email": "user@example.com",
  "password": "securepassword"
}
Response:
json
{
  "token": "<JWT_token>"
}
5. POST /api/resume-upload
Description: Uploads and processes a resume file.
Request:
File upload: Accepts application/pdf or application/vnd.openxmlformats-officedocument.wordprocessingml.document.
Response:
json
{
  "message": "Resume uploaded and processed successfully.",
  "extracted_text": "<Extracted text from the resume>"
}
6. POST /api/job-description
Description: Submits a job description.
Request Body (JSON):
json
{
  "text": "Job description text"
}
Response:
json
{
  "message": "Text submitted successfully",
  "character_count": 123
}
7. POST /api/fit-score
Description: Calculates fit score between a resume and job description.
Request Body (JSON):
json
{
  "resume_text": "Extracted resume text",
  "job_description": "Job description text"
}
Response:
json
{
  "similarity_score": 85.0,
  "keywords_matched": ["skill1", "skill2"],
  "feedback_raw": ["feedback1", "feedback2"]
}
8. POST /api/analyze
Description: Performs detailed analysis of a resume and job description.
Request Body (JSON):
json
{
  "resume_text": "Extracted resume text",
  "job_description": "Job description text"
}
Response:
json
{
  "similarity_score": 85.0,
  "keywords_matched": ["skill1", "skill2"],
  "feedback_raw": ["feedback1", "feedback2"]
}
