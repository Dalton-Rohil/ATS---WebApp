# app/utils.py

print("utils.py is being loaded successfully")  

import base64
import io
import pdf2image
import sqlite3
import spacy
from config.settings import API_KEY
import google.generativeai as genai

# Configure the Google Gemini API using the imported API key
genai.configure(api_key=API_KEY)

# Load or create spaCy model
try:
    nlp = spacy.load("models/spacy_ner_model")
except:
    nlp = spacy.blank("en")

def get_gemini_response(input_text, pdf_content=None, prompt=None):
    """
    Sends a request to the Google Gemini model to get a response based on the input text and prompt.
    Args:
        input_text (str): The input text to be analyzed.
        pdf_content (list): List containing the PDF content in base64 format.
        prompt (str): The prompt to guide the model.
    Returns:
        str: The model's response text.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        if pdf_content:
            response = model.generate_content([input_text, pdf_content[0], prompt])
        else:
            response = model.generate_content([input_text, prompt])
        return response.text
    except Exception as e:
        return f"Error getting response from the model: {e}"

def input_pdf_setup(uploaded_file):
    """
    Converts a PDF file to an image and prepares it for API processing.
    Args:
        uploaded_file (UploadedFile): The uploaded PDF file from Streamlit's file uploader.
    Returns:
        list: List containing the image data in base64 format.
    """
    try:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    except Exception as e:
        raise ValueError(f"Error processing PDF file: {e}")

def calculate_suitability_score(jd_details, resume_details):
    """
    Calculate the suitability score of the resume by comparing it with JD requirements.
    Args:
        jd_details (dict): A dictionary with job description details.
        resume_details (dict): A dictionary with resume details.
    Returns:
        match_percentage (float): Percentage match between JD and resume.
        matching_skills (list): List of skills that match.
        missing_skills (list): List of skills that are missing from the resume.
    """
    if not isinstance(jd_details, dict) or not isinstance(resume_details, dict):
        raise TypeError(f"Expected both jd_details and resume_details to be dictionaries.")

    jd_skills = set(jd_details.get('skills', []))
    resume_skills = set(resume_details.get('skills', []))

    matching_skills = jd_skills.intersection(resume_skills)
    missing_skills = jd_skills.difference(resume_skills)

    match_percentage = (len(matching_skills) / len(jd_skills)) * 100 if len(jd_skills) > 0 else 0

    return round(match_percentage, 2), list(matching_skills), list(missing_skills)

def extract_entities_from_text(text):
    """Extract entities using the spaCy NER model."""
    doc = nlp(text)
    return [ent.text for ent in doc.ents]

def store_data_in_db(document_type, filename, content, extracted_entities):
    """
    Store processed JD/Resume data into the database.
    Args:
        document_type (str): Type of the document (e.g., 'jd' or 'resume').
        filename (str): Name of the file being processed.
        content (str): Raw text content of the document.
        extracted_entities (list): List of extracted entities.
    """
    try:
        conn = sqlite3.connect("data/ats_data.db")
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ats_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_type TEXT,
                filename TEXT,
                content TEXT,
                extracted_entities TEXT
            )
        """)

        # Insert the document details into the table
        cursor.execute("""
            INSERT INTO ats_data (document_type, filename, content, extracted_entities)
            VALUES (?, ?, ?, ?)
        """, (document_type, filename, content, ', '.join(extracted_entities)))

        conn.commit()
    except Exception as e:
        print(f"Error storing data in the database: {e}")
    finally:
        conn.close()
