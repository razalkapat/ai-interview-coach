# groq_helper.py

from groq import Groq
from prompts import (
    resume_match_prompt,
    generate_questions_prompt,
    evaluate_answer_prompt,
    hint_prompt,
    followup_prompt,
)


def setup_groq(api_key: str):
    return Groq(api_key=api_key)


def ask_groq(client, prompt: str, max_tokens: int = 1024) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def analyze_resume_match(client, job_description: str, resume_text: str) -> str:
    return ask_groq(client, resume_match_prompt(job_description, resume_text))


def get_interview_questions(client, job_description: str, resume_text: str) -> list:
    raw = ask_groq(client, generate_questions_prompt(job_description, resume_text)).strip()
    lines = [line.strip() for line in raw.split("\n") if line.strip()]
    questions = []
    for line in lines:
        if line and line[0].isdigit():
            question = line.split(".", 1)[-1].strip()
            questions.append(question)
    return questions[:3]


def evaluate_answer(client, question: str, answer: str, job_description: str) -> str:
    return ask_groq(client, evaluate_answer_prompt(question, answer, job_description))


def get_hint(client, question: str, job_description: str) -> str:
    return ask_groq(client, hint_prompt(question, job_description), max_tokens=256)


def get_followup(client, question: str, answer: str) -> str:
    return ask_groq(client, followup_prompt(question, answer), max_tokens=256)
