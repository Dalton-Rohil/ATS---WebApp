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

def incremental_train_ner(output_dir="models/spacy_ner_model"):
    """Train or update the spaCy NER model using database data."""
    nlp = spacy.blank("en") if not spacy.util.is_package("models/spacy_ner_model") else spacy.load("models/spacy_ner_model")
    ner = nlp.add_pipe("ner", last=True)

    training_data = fetch_data_from_db()
    for _, annotations in training_data:
        for ent in annotations["entities"]:
            ner.add_label(ent[2])

    optimizer = nlp.resume_training()
    for i in range(5):
        losses = {}
        examples = [Example.from_dict(nlp.make_doc(text), ann) for text, ann in training_data]
        nlp.update(examples, sgd=optimizer, drop=0.35, losses=losses)
        print(f"Iteration {i+1}, Losses: {losses}")

    nlp.to_disk(output_dir)
    print(f"Model saved to {output_dir}")

if __name__ == "__main__":
    incremental_train_ner()

