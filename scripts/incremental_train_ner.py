import sqlite3
import spacy
from spacy.training import Example

def fetch_data_from_db():
    """Fetch all data from the database for training."""
    conn = sqlite3.connect("data/ats_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content, extracted_entities FROM ats_data")
    data = cursor.fetchall()
    conn.close()
    return [(text, {"entities": [(0, len(ent), "SKILL") for ent in ents.split(", ")]}) for text, ents in data]
