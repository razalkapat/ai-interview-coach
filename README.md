# 🎯 AI Interview Coach (Groq Edition)

An AI-powered interview preparation tool built with **Groq API** + **Streamlit**.
Uses **llama-3.3-70b** — completely free, works in India, no credit card needed.

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get your free Groq API key
Go to: https://console.groq.com → Sign in → API Keys → Create API Key

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Open in browser
`http://localhost:8501`

## 📁 Project Structure
```
interview-coach/
├── app.py            # Streamlit UI
├── groq_helper.py    # Groq API calls
├── prompts.py        # Prompt templates
├── requirements.txt
└── README.md
```

## 💡 How to Use
1. Enter your **Groq API key** in the sidebar
2. Paste the **job description**
3. Upload your **resume PDF** or paste text
4. Click **Analyze Resume Match**
5. Practice all 5 interview questions and get AI feedback
