# main.py
print("main.py is being loaded successfully")  

import streamlit as st
import pandas as pd
from app.prompts import create_prompts
from app.utils import get_gemini_response, calculate_suitability_score, input_pdf_setup, extract_entities_from_text
from scripts.nlp_extraction_new import nlp_extraction
from config.settings import API_KEY 
import google.generativeai as genai
import sqlite3

# Configure the Google Generative AI API
genai.configure(api_key=API_KEY)

# Streamlit Application Configuration
st.set_page_config(page_title="ATS - Resume Evaluation System", layout="wide")
st.title("ATS - Resume Evaluation System")

# Job description input and file uploader
input_text = st.text_area("Job Description:", key="input")
uploaded_files = st.file_uploader("Upload one or more resumes (PDFs)...", type=["pdf"], accept_multiple_files=True)

# Button to start the evaluation
submit = st.button("Evaluate Resumes")

# Placeholder for storing resume evaluations
evaluation_results = []

# Main evaluation process
if submit and input_text and uploaded_files:
    st.write("Evaluating resumes, please wait...")

    # Extract key requirements from the JD (Place it here)
    jd_requirements = nlp_extraction(input_text)

    # Ensure the extraction returns a valid list
    if jd_requirements:
        jd_requirements = {"skills": jd_requirements}
    else:
        st.warning("No valid skills extracted from the job description. Please check the input.")
        jd_requirements = {"skills": []}

    # Generate prompts dynamically based on the provided JD
    jd_analysis_prompt, resume_analysis_prompt, comparison_prompt = create_prompts(input_text)

    # Process each resume
    for uploaded_file in uploaded_files:
        pdf_content = input_pdf_setup(uploaded_file)

        # Use the Gemini AI model to analyze the resume
        resume_text = get_gemini_response(input_text, pdf_content, resume_analysis_prompt)

        # Extract skills from the resume
        resume_details = {"skills": nlp_extraction(resume_text)}

        # Calculate suitability score
        match_percentage, matching_skills, missing_skills = calculate_suitability_score(jd_requirements, resume_details)

        # Create a one-line verdict for each resume
        verdict = "Strong match" if match_percentage > 75 else \
                  "Moderate match, missing some skills" if match_percentage > 50 else \
                  "Low match, many key skills missing"

        # Append results to the list
        evaluation_results.append({
            "Resume Name": uploaded_file.name,
            "Match Percentage": match_percentage,
            "Top Skills": ', '.join(matching_skills) if matching_skills else "None",
            "Missing Skills": ', '.join(missing_skills[:10]) + '...' if len(missing_skills) > 10 else ', '.join(missing_skills) if missing_skills else "None",
            "Verdict": verdict
        })

    # Convert evaluation results into a DataFrame and sort by match percentage
    df_results = pd.DataFrame(evaluation_results).sort_values(by="Match Percentage", ascending=False)

    # Display the evaluation results as a table
    st.subheader("Resume Evaluation Results")
    st.dataframe(df_results[['Resume Name', 'Match Percentage', 'Top Skills', 'Missing Skills', 'Verdict']])

    # Best candidate based on highest match percentage
    best_candidate = df_results.iloc[0]

    # Display the best candidate's final assessment
    st.subheader(f"Best Candidate: {best_candidate['Resume Name']}")
    st.write(f"Match Percentage: {best_candidate['Match Percentage']}%")
    st.write(f"Top Skills: {best_candidate['Top Skills']}")
    st.write(f"Missing Skills: {best_candidate['Missing Skills']}")
    st.write(f"Final Verdict: {best_candidate['Verdict']}")

    # Provide a final concise assessment for the best candidate
    st.subheader("Final Assessment:")
    if best_candidate['Match Percentage'] > 75:
        st.write(f"{best_candidate['Resume Name']} is the top candidate for the given job description with a {best_candidate['Match Percentage']}% match.")
        st.write(f"The candidate shows proficiency in {best_candidate['Top Skills']} but is missing key skills like {best_candidate['Missing Skills']}.")
        st.write(f"Overall, this candidate is a strong contender for the position based on the match score.")
        st.write("It is recommended to evaluate the candidate further in areas where skills are missing to ensure a complete fit for the role.")
    elif best_candidate['Match Percentage'] > 50:
        st.write(f"{best_candidate['Resume Name']} is a moderate candidate for the given job description with a {best_candidate['Match Percentage']}% match.")
        st.write(f"The candidate has important skills like {best_candidate['Top Skills']}, but is missing key skills such as {best_candidate['Missing Skills']}.")
        st.write("The candidate could be considered, but further evaluation of the missing skills is needed.")
        st.write("It is recommended to focus on improving the missing skills to ensure a full match.")
    else:
        st.write(f"{best_candidate['Resume Name']} is not a strong match for the given job description, with only a {best_candidate['Match Percentage']}% match.")
        st.write(f"The candidate is missing many important skills like {best_candidate['Missing Skills']}.")
        st.write("It is recommended to focus on candidates with a higher match percentage.")
        st.write("Consider further evaluation only if no other strong candidates are available.")

else:
    st.write("Please upload resumes and provide a job description.")

# Database connection function
def store_data_in_db(document_type, filename, content, extracted_entities):
    """Store processed JD/Resume data into the database."""
    conn = sqlite3.connect("data/ats_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ats_data (document_type, filename, content, extracted_entities)
        VALUES (?, ?, ?, ?)
    """, (document_type, filename, content, ', '.join(extracted_entities)))

    conn.commit()
    conn.close()
