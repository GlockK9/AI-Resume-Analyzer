import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

# Sidebar
with st.sidebar:
    st.title("📄 AI Resume Analyzer")
    st.markdown("---")
    st.write("👨‍💻 Christopher Oghoroju")
    st.markdown("---")
    st.subheader("Features")
    st.write("✅ PDF Upload")
    st.write("✅ Resume Analysis")
    st.write("✅ Resume Score")
    st.write("✅ Improvement Suggestions")
    st.markdown("---")
    st.info("Upload a resume to begin analysis.")

# Main Page
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume in PDF format.")

uploaded_file = st.file_uploader(
    "Choose a PDF Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    # Statistics
    word_count = len(text.split())
    character_count = len(text)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Words", word_count)

    with col2:
        st.metric("Characters", character_count)

    # Resume Text
    st.subheader("📄 Extracted Resume")

    st.text_area(
        "Resume Text",
        text,
        height=300
    )

    # Resume Analysis
    st.subheader("📊 Resume Analysis")
    

    score = 0
    feedback = []

    skills = [
        "python",
        "sql",
        "excel",
        "power bi",
        "machine learning",
        "streamlit",
        "git",
        "github"
    ]
    st.subheader("🛠️ Skills Found")

    found_skills = []

    for skill in skills:
        if skill in text.lower():
            found_skills.append(skill.title())

    if found_skills:
        st.success(", ".join(found_skills))
    else:
        st.warning("No recognized skills found.")

    for skill in skills:
        if skill in text.lower():
            score += 10

    if "bachelor" in text.lower() or "university" in text.lower():
        score += 10

    if "experience" in text.lower():
        score += 10

    score = min(score, 100)

    st.progress(score / 100)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Resume Score", f"{score}/100")

    with col2:
        if score >= 80:
            st.metric("Rating", "Excellent")
        elif score >= 60:
            st.metric("Rating", "Good")
        else:
            st.metric("Rating", "Needs Work")

    if score >= 80:
        st.success("Excellent resume! 🎉")
    elif score >= 60:
        st.warning("Good resume, but there is room for improvement.")
    else:
        st.error("Your resume needs more improvements.")

    if "github" not in text.lower():
        feedback.append("🔹 Add your GitHub profile.")

    if "linkedin" not in text.lower():
        feedback.append("🔹 Add your LinkedIn profile.")

    if "projects" not in text.lower():
        feedback.append("🔹 Include a Projects section.")

    if "skills" not in text.lower():
        feedback.append("🔹 Add a Skills section.")

    if feedback:
        st.subheader("💡 Suggestions")
        for item in feedback:
            st.write(item)