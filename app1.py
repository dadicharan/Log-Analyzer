import os
import re
import numpy as np
import streamlit as st
import fitz  # PyMuPDF
from docx import Document
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
import plotly.express as px
from sentence_transformers import SentenceTransformer
import ollama
from joblib import Memory

# ---------------------- Load Config and Styles ----------------------
from config import BERT_MODEL_NAME, INDUSTRY_PROFILES
from styles import CUSTOM_CSS

# ---------------------- Page Setup ----------------------
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.title("🧠 ResumeIQ Pro")

# ---------------------- Model and Cache ----------------------
memory = Memory(location=".", verbose=0)
model = SentenceTransformer(BERT_MODEL_NAME)

def get_ai_feedback(text):
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Analyze this resume and provide 3 specific improvement suggestions:\n"
                        "- Focus on quantifiable achievements\n"
                        "- Suggest better action verbs\n"
                        "- Identify missing sections"
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"AI Feedback Error: {str(e)}"

# ---------------------- Utility Functions ----------------------
@memory.cache
def calculate_similarity(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text])
    return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0] * 100

def extract_text(file):
    if file.type == "application/pdf":
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            return " ".join([page.get_text() for page in doc]).lower()
    elif file.type == "text/plain":
        return file.read().decode().lower()
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return " ".join([para.text for para in doc.paragraphs]).lower()
    return ""

def analyze_sections(text):
    section_patterns = {
        "Skills": r"(skills|technical skills)(.*?)(experience|education)",
        "Experience": r"(experience|work history)(.*?)(education|projects)",
        "Education": r"(education|academic background)(.*?)(skills|certifications)"
    }
    return {
        section: 1 if re.search(pattern, text, re.IGNORECASE | re.DOTALL) else 0
        for section, pattern in section_patterns.items()
    }

# ---------------------- Streamlit UI ----------------------
def main():
    with st.sidebar:
        st.header("⚙️ Configuration")
        jd_input = st.text_area("📝 Job Description:", height=300)
        industry = st.selectbox("🏭 Industry Focus:", list(INDUSTRY_PROFILES.keys()))
        min_score = st.slider("🎯 Minimum Match Score (%):", 0, 100, 60)
        analysis_mode = st.radio("🔧 Analysis Mode:", ["Basic", "Advanced AI"])
        show_wordcloud = st.checkbox("☁️ Word Cloud", True)
        show_skill_gap = st.checkbox("🔍 Skill Gap Analysis", True)

    uploaded_files = st.file_uploader(
        "📤 Upload Resumes (PDF/DOCX/TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if st.button("🚀 Start Comprehensive Analysis", use_container_width=True):
        if not all([jd_input, uploaded_files]):
            st.error("⚠️ Please provide both job description and resumes")
            return

        with st.spinner("🔍 Analyzing resumes..."):
            jd_text = re.sub(r'\W+', ' ', jd_input).lower()
            profile_keywords = INDUSTRY_PROFILES[industry]["keywords"]
            jd_keywords = set(re.findall(r'\b[a-z]{4,15}\b', jd_text)).union(profile_keywords)

            results = []
            for file in uploaded_files:
                with st.expander(f"📄 {file.name}", expanded=False):
                    col1, col2, col3 = st.columns([4, 2, 2])

                    with col1:
                        resume_text = extract_text(file)
                        resume_clean = re.sub(r'\W+', ' ', resume_text).lower()

                        similarity = calculate_similarity(resume_clean, jd_text)
                        section_scores = analyze_sections(resume_text)

                        found_keywords = [kw for kw in jd_keywords if kw in resume_clean]
                        missing_keywords = list(jd_keywords - set(found_keywords))

                        feedback = get_ai_feedback(resume_text) if analysis_mode == "Advanced AI" else ""
                        results.append((file.name, similarity, set(found_keywords), feedback))

                    with col2:
                        st.markdown("### 📊 Metrics")
                        st.metric("Semantic Match", f"{similarity:.1f}%")
                        st.metric("Keywords Found", f"{len(found_keywords)}/{len(jd_keywords)}")

                        st.markdown("### 📑 Sections")
                        for section, score in section_scores.items():
                            st.progress(score, text=section)

                    with col3:
                        if feedback:
                            st.markdown("### 💡 AI Suggestions")
                            st.markdown(f"```\n{feedback}\n```")

                        st.download_button(
                            "💾 Download Analysis",
                            data=file,
                            file_name=f"analysis_{file.name}",
                            mime="application/octet-stream"
                        )

            st.markdown("---")
            st.header("📈 Executive Dashboard")

            top_candidates = sorted(results, key=lambda x: x[1], reverse=True)[:3]
            cols = st.columns(3)
            for idx, (name, score, keywords, _) in enumerate(top_candidates):
                with cols[idx]:
                    st.markdown(f"### 🥇 #{idx+1} {name}")
                    st.metric("Composite Score", f"{score:.1f}%")
                    st.write(f"**Keywords Found:** {len(keywords)}")

            if show_skill_gap:
                st.subheader("🔍 Industry Skill Gap")
                missing_counts = {kw: sum(1 for _, _, kws, _ in results if kw not in kws) for kw in jd_keywords}
                fig = px.treemap(
                    names=list(missing_counts.keys()),
                    parents=[""] * len(missing_counts),
                    values=list(missing_counts.values()),
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                st.plotly_chart(fig, use_container_width=True)

            if show_wordcloud:
                st.subheader("☁️ Keyword Frequency Cloud")
                wordcloud = WordCloud().generate(" ".join(jd_keywords))
                st.image(wordcloud.to_array(), use_column_width=True)

if __name__ == "__main__":
    main()
