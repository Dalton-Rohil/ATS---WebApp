print("nlp_extraction_new.py is being loaded successfully")

import spacy
import re

# Load or create spaCy model
try:
    nlp = spacy.load("models/spacy_ner_model")
    print("Custom spaCy model loaded successfully.")
except Exception as e:
    print(f"Error loading custom spaCy model: {e}. Falling back to 'en_core_web_sm'.")
    nlp = spacy.load("en_core_web_sm")

def nlp_extraction(text):
    """
    Extract potential skills and keywords from the provided text.
    Args:
        text (str): The input text to analyze (JD or resume content).
    Returns:
        list: List of extracted relevant entities or keywords.
    """
    doc = nlp(text.lower())
    extracted_entities = [ent.text.strip() for ent in doc.ents]

    # Additional regex-based keyword extraction
    keywords = re.findall(r'\b[A-Za-z\-]+\b', text.lower())

    # Combine extracted entities and keywords, remove duplicates
    all_extracted = set(extracted_entities + keywords)

    # Filter out common stopwords or irrelevant terms
    filtered_skills = [
        word for word in all_extracted if len(word) > 2 and word not in {"the", "and", "with", "for", "job"}
    ]
    return filtered_skills

