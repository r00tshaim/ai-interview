from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Use environment variable or default to localhost
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["interviews"]
collection = db["sessions"]

def save_interview_session(session_id: str, summary: dict, objective: str, questions: list):
    doc = {
        "session_id": session_id,
        "summary": summary,
        "objective": objective,
        "questions": questions,
        "interview_started": False,
        "answers": []
    }
    collection.insert_one(doc)


def get_questions_by_session(session_id: str):
    doc = collection.find_one({"session_id": session_id})
    if doc:
        return doc.get("questions", [])
    return None
