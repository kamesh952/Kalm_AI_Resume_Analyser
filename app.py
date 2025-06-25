import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# Set Gemini API Key directly in the code (not recommended for production)
GOOGLE_API_KEY = "AIzaSyC_XUGoW6ZsvTJwag-qwXNUhL5IQL0JsDM"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_resume_percentage(text, job_description):
    prompt = f"""
    Analyze this resume and compare it with the following job description:

    Job Description:
    {job_description}

    Resume Content:
    {text}

    Provide the following:
    1. Provide a percentage match between the resume and job description.
    2. Follow with a clear justification of why you gave that percentage.
    3. Then give suggestions on how to improve the resume to get a better match.
    4. Keep it short and straigh to the point.
    """
    response = model.generate_content(prompt)
    return response.text

def analyze_resume_missing_skills(text, job_description):
    prompt = f"""
    Analyze this resume and compare it with the following job description:

    Job Description:
    {job_description}

    Resume Content:
    {text}

    Provide the following:
    Highlight all the skills that are listed in the job description but are missing from the resume. Do not follow up with a justification or explanation.
    """
    response = model.generate_content(prompt)
    return response.text

def generate_cover_letter(text, job_description):
    prompt = f"""
    Analyze this resume and job description, and draft a convincing cover letter:

    Job Description:
    {job_description}

    Resume Content:
    {text}

    Provide the following:
    Draft a cover letter that considers both the resume and the job description.The tone of the letter drafted must be convincing and ambitious.
    """
    response = model.generate_content(prompt)
    return response.text

def generate_about_me(text, job_description):
    prompt = f"""
    Analyze this resume and job description, and draft an "About Me" section for an interview:

    Job Description:
    {job_description}

    Resume Content:
    {text}

    Provide the following:
    Draft a first-person narrative "About Me" section that the user can use to introduce themselves in an interview. Consider both the resume and the job description to give the best possible introduction.
    """
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.set_page_config(page_title="KALM AI Resume Analyzer", page_icon="📝")
st.title("📝 KALM AI Resume Analyzer")
st.write("Upload a resume (PDF) and a job description to get a detailed analysis.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_description = st.text_area("Paste Job Description Here")

analysis = ""

if uploaded_file is not None and job_description:
    text = extract_text_from_pdf(uploaded_file)

    if st.button("Show Percentage Match"):
        with st.spinner("Calculating percentage match..."):
            analysis = analyze_resume_percentage(text, job_description)
            st.subheader("✅ Percentage Match")
            st.write(analysis)

    if st.button("Show Missing Skills"):
        with st.spinner("Identifying missing skills..."):
            analysis = analyze_resume_missing_skills(text, job_description)
            st.subheader("❗ Missing Skills or Experiences")
            st.write(analysis)

    if st.button("Generate Cover Letter"):
        with st.spinner("Generating cover letter..."):
            analysis = generate_cover_letter(text, job_description)
            st.subheader("📄 Cover Letter")
            st.write(analysis)

    if st.button("Generate About Me"):
        with st.spinner("Generating 'About Me'..."):
            analysis = generate_about_me(text, job_description)
            st.subheader("🗣️ About Me for Interview")
            st.write(analysis)

    if analysis:
        st.download_button(
            label="Download Analysis",
            data=analysis,
            file_name="resume_analysis.txt",
            mime="text/plain"
        )