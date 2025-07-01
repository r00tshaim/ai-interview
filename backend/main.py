# FastAPI entrypoint

from fastapi import FastAPI, UploadFile, Form
from resume_parser import extract_resume_text, summarize_resume
from question_generator import generate_questions
from db import save_interview_session
import uuid

app = FastAPI()

@app.post("/upload-resume")
async def upload_resume(file: UploadFile, objective: str = Form(...)):
    content = await file.read()
    resume_text = extract_resume_text(content)  # Convert bytes to string
    summary = summarize_resume(resume_text)

    questions = generate_questions(summary, objective)

    session_id = str(uuid.uuid4())

    # Save to MongoDB
    save_interview_session(session_id, summary.dict(), objective, questions)

    return {
        "session_id": session_id,
        "questions": questions,
        "summary": summary
    }
