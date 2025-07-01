# Utility to extract text from resume


import uuid
import os
from langchain_community.document_loaders import PyPDFLoader

def extract_resume_text(file_bytes: bytes) -> str:
    # Save file temporarily
    temp_filename = f"/tmp/resume_{uuid.uuid4()}.pdf"
    with open(temp_filename, "wb") as f:
        f.write(file_bytes)

    # Load using PyPDFLoader
    loader = PyPDFLoader(temp_filename)
    docs = loader.load()

    # Cleanup temp file
    os.remove(temp_filename)

    #print("docs:" ,docs)

    # Combine page content
    text = "\n".join(doc.page_content for doc in docs)
    return text



from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

class ResumeSummary(BaseModel):
    skills: List[str] = Field(..., description="['Python', 'React', 'Docker']")
    work_experience: str = Field(..., description="3 years in backend development...")
    education: str  = Field(..., description="B.Tech in Computer Science")
    achievements: List[str] = Field(..., description="['Built an AI chatbot', 'Led a team of 5 engineers']")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
llm = llm.with_structured_output(ResumeSummary)


def summarize_resume(resume_text: str) -> ResumeSummary:
    splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = splitter.split_text(resume_text)

    # Merge all chunks before summarizing to keep output in 1 structure
    merged = "\n".join(chunks)

    prompt = f"""
You are a resume parsing agent.

Extract the following details from the resume text and return a JSON object.

Resume Text:
\"\"\"
{merged}
\"\"\"

Return JSON with this exact format:
{{
  "skills": ["skill1", "skill2", ...],
  "work_experience": "summarized experience in plain text",
  "education": "summarized education in plain text",
  "achievements": ["achievement1", "achievement2", ...]
}}

Only return valid JSON.
"""

    response = llm.invoke(prompt)
    #print("LLM response:", response)  # Add this line
    if not response:
        raise ValueError("LLM returned an empty response. Check your API key and quota.")
    try:
        return response
    except Exception as e:
        print("Failed to parse LLM response:", response)
        raise e
