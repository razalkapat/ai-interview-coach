$content = @'
# 🎯 AI Interview Coach

> **Live Demo 👉 [ai-interview-coachh.streamlit.app](https://ai-interview-coachh.streamlit.app/)**

An AI-powered interview preparation tool built with **Groq API** + **Streamlit**.  
Practice real interview questions, get instant AI feedback, and land your dream job! 🚀

---

## 🤖 What does it do?

Paste any job description + your resume → the app will:

1. **📊 Score your resume** — match score, strengths, gaps, and tips
2. **💬 Generate 3 tailored questions** — technical, behavioral, and situational
3. **💡 Give hints** — how to structure your answer before you type
4. **✅ Evaluate your answers** — rating + what worked + what to improve + sample better answer
5. **🔥 Fire a follow-up question** — just like a real interviewer would
6. **😊 Track your confidence** — rate each answer and review in the summary
7. **📝 Full session summary** — review all questions, answers, and feedback at the end

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Groq](https://groq.com) | Ultra-fast LLM inference API |
| [LLaMA 3.3-70b](https://ai.meta.com/llama/) | Open source language model by Meta |
| [Streamlit](https://streamlit.io) | Python web UI framework |
| [PyPDF2](https://pypdf2.readthedocs.io) | PDF text extraction |

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/razalkapat/ai-interview-coach.git
cd ai-interview-coach
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key
Go to 👉 [console.groq.com](https://console.groq.com) → Sign in → API Keys → Create API Key  
No credit card needed. Works in India! 🇮🇳

### 4. Run the app
```bash
streamlit run app.py
```

---

## ✨ Features

- ✅ Resume vs JD match scoring (out of 10)
- ✅ Strengths & gaps analysis
- ✅ 3 tailored interview questions (technical + behavioral + situational)
- ✅ Hint system before answering
- ✅ AI feedback with rating (Weak / Average / Good / Excellent)
- ✅ Sample better answer provided
- ✅ Follow-up question after each answer
- ✅ Confidence meter per question
- ✅ Full session review at the end
- ✅ PDF resume upload support

---

## 🔮 Future Ideas

- [ ] Voice input for answers
- [ ] Export session as PDF report
- [ ] Difficulty levels (Junior / Senior)
- [ ] Support for multiple job descriptions
- [ ] Ollama support for fully offline mode

---
