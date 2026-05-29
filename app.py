# app.py — AI Interview Coach powered by Groq

import streamlit as st
import PyPDF2
import io
from groq_helper import (
    setup_groq, analyze_resume_match, get_interview_questions,
    evaluate_answer, get_hint, get_followup
)

st.set_page_config(page_title="AI Interview Coach", page_icon="🎯", layout="wide")

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 800; color: #1a1a2e; }
    .subtitle { color: #555; font-size: 1.1rem; margin-bottom: 1rem; }
    .desc-box {
        background: linear-gradient(135deg, #ede9fe, #e0f2fe);
        border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem;
    }
    .desc-box h4 { margin: 0 0 0.5rem 0; color: #4f46e5; }
    .desc-box p { margin: 0; color: #444; font-size: 0.95rem; line-height: 1.6; }
    .feature-grid { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 0.8rem; }
    .feature-pill {
        background: white; border: 1px solid #c4b5fd;
        border-radius: 999px; padding: 4px 14px;
        font-size: 0.82rem; color: #5b21b6; font-weight: 500;
    }
    .section-header {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white; padding: 0.5rem 1rem;
        border-radius: 8px; font-weight: 600; margin-bottom: 1rem;
    }
    .result-box {
        background: #f8f9ff; border-left: 4px solid #4f46e5;
        padding: 1rem 1.5rem; border-radius: 0 8px 8px 0; white-space: pre-wrap;
    }
    .feedback-box {
        background: #f0fdf4; border-left: 4px solid #22c55e;
        padding: 1rem 1.5rem; border-radius: 0 8px 8px 0; white-space: pre-wrap;
    }
    .hint-box {
        background: #fffbeb; border-left: 4px solid #f59e0b;
        padding: 1rem 1.5rem; border-radius: 0 8px 8px 0;
    }
    .followup-box {
        background: #fef2f2; border-left: 4px solid #ef4444;
        padding: 1rem 1.5rem; border-radius: 0 8px 8px 0;
    }
    .question-card {
        background: white; border: 1px solid #e0e0f0; border-radius: 10px;
        padding: 1.2rem 1.5rem; margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(79,70,229,0.07); font-size: 1.05rem;
    }
    .badge {
        display: inline-block; padding: 2px 10px; border-radius: 999px;
        font-size: 0.8rem; font-weight: 600; margin-bottom: 8px;
    }
    .api-info {
        background: #f0f9ff; border: 1px solid #bae6fd;
        border-radius: 8px; padding: 0.8rem 1rem; font-size: 0.85rem; color: #0369a1;
    }
</style>
""", unsafe_allow_html=True)


def extract_pdf_text(uploaded_file) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    return "".join(page.extract_text() or "" for page in reader.pages).strip()


# Session state defaults
defaults = {
    "client": None, "questions": [], "jd": None,
    "current_q": 0, "scores": [], "match_result": None,
    "current_feedback": None, "current_hint": None,
    "current_followup": None, "answer_submitted": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# Header
st.markdown('<div class="main-title">🎯 AI Interview Coach</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your personal AI-powered interview trainer — free, fast, and built for job seekers.</div>', unsafe_allow_html=True)

# Description Box
st.markdown("""
<div class="desc-box">
    <h4>🤖 What does this app do?</h4>
    <p>
        AI Interview Coach helps you prepare for job interviews by analyzing your resume against a job description,
        generating tailored interview questions, and giving you detailed AI feedback on your answers —
        just like a real mock interview with a career coach.
    </p>
    <div class="feature-grid">
        <span class="feature-pill">📊 Resume Match Score</span>
        <span class="feature-pill">💬 3 Tailored Questions</span>
        <span class="feature-pill">💡 Answer Hints</span>
        <span class="feature-pill">✅ AI Feedback</span>
        <span class="feature-pill">🔥 Follow-up Questions</span>
        <span class="feature-pill">😊 Confidence Tracker</span>
        <span class="feature-pill">📝 Session Summary</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
**How to use:**
1. 🔑 Enter your free Groq API key in the sidebar
2. 📋 Paste the job description you are applying for
3. 📄 Upload your resume PDF or paste the text
4. 🔍 Click **Analyze** to get your match score and 3 interview questions
5. 💬 Answer each question and receive instant AI feedback
""")

st.divider()


# Sidebar
with st.sidebar:
    st.header("⚙️ Setup")

    # Auto-load API key from Streamlit secrets if deployed
    default_key = ""
    try:
        default_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    api_key = st.text_input(
        "Groq API Key",
        value=default_key,
        type="password",
        placeholder="gsk_..."
    )

    st.markdown('<div class="api-info">🆓 Get a <b>free</b> Groq API key at <a href="https://console.groq.com" target="_blank">console.groq.com</a><br>No credit card needed. Works in India!</div>', unsafe_allow_html=True)

    if api_key and st.session_state.client is None:
        try:
            st.session_state.client = setup_groq(api_key)
            st.success("✅ Connected to Groq!")
        except Exception as e:
            st.error(f"Failed: {e}")

    st.divider()
    st.markdown("**📌 Features:**")
    st.markdown("📊 Resume match scoring")
    st.markdown("💬 3 tailored questions")
    st.markdown("💡 Hints before answering")
    st.markdown("✅ Detailed answer feedback")
    st.markdown("🔥 Follow-up question drill")
    st.markdown("😊 Confidence tracker")
    st.markdown("📝 Full session summary")
    st.divider()
    st.markdown("**🛠️ Built with:**")
    st.markdown("- [Groq](https://groq.com) — LLM inference")
    st.markdown("- [LLaMA 3.3-70b](https://ai.meta.com/llama/) — Open source LLM")
    st.markdown("- [Streamlit](https://streamlit.io) — UI framework")
    st.divider()
    st.caption("⚡ Powered by Groq — llama-3.3-70b")


# Inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">📋 Job Description</div>', unsafe_allow_html=True)
    jd_input = st.text_area("JD", height=250,
        placeholder="Paste the full job description here...\n\ne.g. We are looking for a Machine Learning Engineer with experience in Python, TensorFlow, model deployment...",
        label_visibility="collapsed")

with col2:
    st.markdown('<div class="section-header">📄 Your Resume</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📁 Upload PDF", "✏️ Paste Text"])
    resume_text = ""
    with tab1:
        uploaded = st.file_uploader("PDF", type=["pdf"], label_visibility="collapsed")
        if uploaded:
            resume_text = extract_pdf_text(uploaded)
            st.success(f"✅ Extracted {len(resume_text)} characters from your resume")
    with tab2:
        pasted = st.text_area("Paste", height=200,
            placeholder="Paste your resume text here...", label_visibility="collapsed")
        if pasted:
            resume_text = pasted

st.divider()

# Analyze Button
if st.button("🔍 Analyze Resume & Generate Interview Questions", use_container_width=True, type="primary"):
    if not st.session_state.client:
        st.warning("⚠️ Please enter your Groq API key in the sidebar to get started.")
    elif not jd_input.strip():
        st.warning("⚠️ Please paste the job description.")
    elif not resume_text.strip():
        st.warning("⚠️ Please upload or paste your resume.")
    else:
        st.session_state.jd = jd_input

        with st.spinner("🤖 Analyzing your resume against the job description..."):
            st.session_state.match_result = analyze_resume_match(
                st.session_state.client, jd_input, resume_text)

        with st.spinner("🎤 Generating 3 tailored interview questions..."):
            st.session_state.questions = get_interview_questions(
                st.session_state.client, jd_input, resume_text)
            st.session_state.current_q = 0
            st.session_state.scores = []
            st.session_state.current_feedback = None
            st.session_state.current_hint = None
            st.session_state.current_followup = None
            st.session_state.answer_submitted = False

# Match Result
if st.session_state.match_result:
    st.markdown('<div class="section-header">📊 Resume Match Analysis</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{st.session_state.match_result}</div>', unsafe_allow_html=True)
    st.divider()

# Interview Practice
if st.session_state.questions:
    total_q = len(st.session_state.questions)
    current = st.session_state.current_q

    st.markdown('<div class="section-header">💬 Interview Practice</div>', unsafe_allow_html=True)
    st.progress(current / total_q, text=f"Question {min(current + 1, total_q)} of {total_q}")

    if current < total_q:
        question = st.session_state.questions[current]

        q_types = ["🔧 Technical", "🌟 Behavioral", "🧠 Situational"]
        badge = q_types[current] if current < len(q_types) else "❓ Question"
        st.markdown(
            f'<div class="question-card"><span class="badge" style="background:#ede9fe;color:#6d28d9">{badge}</span><br><strong>Q{current+1}:</strong> {question}</div>',
            unsafe_allow_html=True)

        # Hint button
        col_hint, _ = st.columns([1, 3])
        with col_hint:
            if st.button("💡 Get a Hint", key=f"hint_{current}"):
                with st.spinner("Getting hint..."):
                    st.session_state.current_hint = get_hint(
                        st.session_state.client, question, st.session_state.jd)

        if st.session_state.current_hint and not st.session_state.answer_submitted:
            st.markdown(f'<div class="hint-box">💡 <strong>Hint:</strong> {st.session_state.current_hint}</div>',
                        unsafe_allow_html=True)
            st.write("")

        # Answer input
        if not st.session_state.answer_submitted:
            user_answer = st.text_area("Your answer:", height=150,
                placeholder="Type your answer here...\nFor behavioral questions use STAR: Situation → Task → Action → Result",
                key=f"answer_{current}")

            confidence = st.select_slider(
                "How confident do you feel about this answer?",
                options=["😰 Not confident", "🤔 Unsure", "🙂 Okay", "😊 Confident", "🔥 Very confident"],
                value="🙂 Okay",
                key=f"conf_{current}"
            )

            if st.button("📩 Submit Answer & Get Feedback", type="primary", key=f"submit_{current}"):
                if not user_answer.strip():
                    st.warning("Please write an answer before submitting.")
                else:
                    with st.spinner("✅ Evaluating your answer..."):
                        feedback = evaluate_answer(
                            st.session_state.client, question,
                            user_answer, st.session_state.jd)

                    with st.spinner("🔥 Generating follow-up question..."):
                        followup = get_followup(
                            st.session_state.client, question, user_answer)

                    st.session_state.current_feedback = feedback
                    st.session_state.current_followup = followup
                    st.session_state.answer_submitted = True
                    st.session_state.scores.append({
                        "q": question, "a": user_answer,
                        "confidence": confidence,
                        "feedback": feedback, "followup": followup,
                    })
                    st.rerun()

        # Feedback after submission
        if st.session_state.answer_submitted and st.session_state.current_feedback:
            st.markdown("**✅ AI Feedback on your answer:**")
            st.markdown(f'<div class="feedback-box">{st.session_state.current_feedback}</div>',
                        unsafe_allow_html=True)
            st.write("")

            if st.session_state.current_followup:
                st.markdown("**🔥 Interviewer Follow-up Question:**")
                st.markdown(f'<div class="followup-box">❓ {st.session_state.current_followup}</div>',
                            unsafe_allow_html=True)
                st.write("")

            if st.button("➡️ Next Question", type="primary", key=f"next_{current}"):
                st.session_state.current_q += 1
                st.session_state.current_feedback = None
                st.session_state.current_hint = None
                st.session_state.current_followup = None
                st.session_state.answer_submitted = False
                st.rerun()

    # Summary Screen
    else:
        st.success(f"🎉 You have completed all {total_q} interview questions!")
        st.balloons()

        st.markdown("### 📊 Confidence Overview")
        conf_cols = st.columns(total_q)
        for i, item in enumerate(st.session_state.scores):
            with conf_cols[i]:
                st.metric(f"Q{i+1}", item.get("confidence", "—"))

        st.divider()
        st.markdown("### 📝 Full Session Review")
        for i, item in enumerate(st.session_state.scores):
            with st.expander(f"Q{i+1}: {item['q'][:70]}..."):
                st.markdown(f"**Your Answer:** {item['a']}")
                st.markdown(f"**Confidence:** {item.get('confidence', '—')}")
                st.divider()
                st.markdown(f"**✅ Feedback:**\n{item['feedback']}")
                if item.get("followup"):
                    st.markdown(f"**🔥 Follow-up Asked:** {item['followup']}")

        st.divider()
        st.info("💡 **Tip:** Share this app URL with recruiters so they can try it live!")

        if st.button("🔄 Start Over with a New Job", use_container_width=True):
            for k in ["questions", "current_q", "scores", "match_result",
                      "jd", "current_feedback", "current_hint",
                      "current_followup", "answer_submitted"]:
                st.session_state[k] = None
            st.session_state.questions = []
            st.session_state.scores = []
            st.session_state.current_q = 0
            st.session_state.answer_submitted = False
            st.rerun()