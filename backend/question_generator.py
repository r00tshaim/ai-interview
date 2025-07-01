# Gemini question generation logic

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))


def generate_questions(summary: dict, objective: str):
    prompt = f"""
You are an expert interviewer.

Based on the candidate's resume summary and the interview objective, generate 6 interview questions.

Resume Summary:
Skills: {summary.skills}
Experience: {summary.work_experience}
Education: {summary.education}
Achievements: {summary.achievements}

Objective: {objective}

Return only the questions in a bullet list.
"""

    response = llm.invoke(prompt)
    return response.content.split("\n")

