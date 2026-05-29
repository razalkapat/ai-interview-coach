# prompts.py

def resume_match_prompt(job_description: str, resume_text: str) -> str:
    return f"""
You are an expert career coach and recruiter.

Analyze how well this resume matches the job description below.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Give your response in this exact format:

MATCH SCORE: [X/10]

STRENGTHS (what matches well):
- [point 1]
- [point 2]
- [point 3]

GAPS (what's missing or weak):
- [point 1]
- [point 2]
- [point 3]

QUICK TIP:
[One actionable suggestion to improve the resume for this role]
"""


def generate_questions_prompt(job_description: str, resume_text: str) -> str:
    return f"""
You are an experienced technical interviewer.

Based on the job description and the candidate's resume, generate exactly 3 interview questions.
- 1 technical/skill-based question
- 1 behavioral question (STAR format)
- 1 tricky/situational question

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY a numbered list of 3 questions. No extra text. No preamble.
"""


def evaluate_answer_prompt(question: str, answer: str, job_description: str) -> str:
    return f"""
You are a friendly but honest interview coach.

The candidate was asked this interview question:
QUESTION: {question}

Their answer was:
ANSWER: {answer}

The role they are applying for:
JOB CONTEXT: {job_description[:300]}

Evaluate their answer and respond EXACTLY in this format (do not skip any section):

RATING: [Weak / Average / Good / Excellent]

WHAT WORKED:
[1-2 sentences on what was good about their answer]

WHAT TO IMPROVE:
[1-2 sentences on what was missing or could be stronger]

SAMPLE BETTER ANSWER:
[Write a short improved version of their answer in 3-4 sentences]
"""


def hint_prompt(question: str, job_description: str) -> str:
    return f"""
You are a helpful interview coach giving a quick tip before the candidate answers.

QUESTION: {question}
JOB CONTEXT: {job_description[:200]}

Give a 2-3 sentence hint on HOW to approach answering this question well.
Focus on structure and what to include. Do NOT answer the question for them.
Keep it concise and actionable.
"""


def followup_prompt(question: str, answer: str) -> str:
    return f"""
You are a tough interviewer. The candidate just answered this question:

QUESTION: {question}
THEIR ANSWER: {answer}

Ask ONE sharp follow-up question that digs deeper into their answer or challenges a weak point.
Return ONLY the follow-up question. No preamble.
"""
