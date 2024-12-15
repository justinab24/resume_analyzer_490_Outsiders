from pydantic import BaseModel

class TextSubmission(BaseModel):
    text: str

class FeedbackItem(BaseModel):
            message: str
            feedback_type: str

class NLPInput(BaseModel):
    resume_text: str
    job_description: str

class NLPOutput(BaseModel):
    similarity_score: float
    keywords_matched: list[str]
    feedback_raw: list[str]
