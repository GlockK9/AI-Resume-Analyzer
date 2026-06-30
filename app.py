import streamlit as st
from pypdf import PdfReader
from groq import Groq

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

# Groq client (FREE AI)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================
# AI FUNCTION
# =========================
def generate_ai_feedback(resume_text, job_description):
    prompt = f"""
You are an ATS resume reviewer and career coach.

Return:
1. Missing Skills
2. Weak Areas
3. Improvements Needed
4. 2 Improved Bullet Points

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("📄 AI Resume Analyzer")
    st.markdown("---")
    st.write("👨‍💻 Christopher Oghoroju")
    st.markdown("---")

    st.subheader("Features")
    st.write("✅ PDF Upload")
    st.write("✅ ATS Score")
    st.write("✅ AI Feedback")
    st.write("✅ Job Matching")
    st.markdown("---")
    st.info("Upload a resume to begin analysis.")

# =========================
# MAIN APP
# =========================
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume in PDF format.")

uploaded_file = st.file_uploader("Choose a PDF Resume", type=["pdf"])

# =========================
# PROCESS FILE
# =========================
if uploaded_file is not None:

    # ---------- Extract PDF ----------
    reader = PdfReader(uploaded_file)

    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    # ---------- BASIC INFO ----------
    word_count = len(text.split())
    character_count = len(text)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Words", word_count)

    with col2:
        st.metric("Characters", character_count)

    # ---------- SHOW TEXT ----------
    st.subheader("📄 Extracted Resume")
    st.text_area("Resume Text", text, height=300)

    # =========================
    # JOB DESCRIPTION
    # =========================
    st.subheader("📌 Job Description (Optional)")
    job_description = st.text_area("Paste Job Description here", height=200)

    # =========================
    # SKILLS DETECTION
    # =========================
    st.subheader("🛠️ Skills Found")

    skills = [
        "python", "sql", "excel", "power bi",
        "machine learning", "streamlit", "git", "github"
    ]

    text_lower = text.lower()

    found_skills = [s for s in skills if s in text_lower]

    if found_skills:
        st.success(", ".join([s.title() for s in found_skills]))
    else:
        st.warning("No recognized skills found.")

    # =========================
    # ATS SCORE
    # =========================
    skill_score = (len(found_skills) / len(skills)) * 100
    education_score = 10 if ("bachelor" in text_lower or "university" in text_lower) else 0
    experience_score = 10 if "experience" in text_lower else 0
    keyword_score = min(len(text.split()) / 50, 100)

    ats_score = (skill_score + education_score + experience_score + keyword_score) / 4
    ats_score = round(min(ats_score, 100), 2)

    st.subheader("📊 ATS Score Breakdown")

    st.metric("Overall ATS Score", f"{ats_score}/100")
    st.progress(ats_score / 100)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Skills", f"{round(skill_score)}%")

    with col2:
        st.metric("Education", f"{education_score}%")

    with col3:
        st.metric("Experience", f"{experience_score}%")

    with col4:
        st.metric("Keywords", f"{round(keyword_score)}%")

    # =========================
    # RULE-BASED FEEDBACK
    # =========================
    feedback = []

    if len(found_skills) < 4:
        feedback.append("Add more technical skills.")

    if "project" not in text_lower:
        feedback.append("Add project section.")

    if "github" not in text_lower:
        feedback.append("Add GitHub profile.")

    if "linkedin" not in text_lower:
        feedback.append("Add LinkedIn profile.")

    if len(text.split()) < 300:
        feedback.append("Expand resume content.")

    if feedback:
        st.subheader("💡 Suggestions")
        for item in feedback:
            st.write("🔹", item)

    # =========================
    # AI BUTTON
    # =========================
    st.subheader("🤖 AI Career Feedback")

    if st.button("Generate AI Feedback"):
        with st.spinner("Analyzing with AI..."):
            result = generate_ai_feedback(text, job_description)

        st.success("Analysis Complete")
        st.write(result)