import sqlite3

def create_database():
    """Create a SQLite database and table for ATS data."""
    conn = sqlite3.connect("data/ats_data.db")
    cursor = conn.cursor()

    # Create table for storing JD and Resume data
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ats_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_type TEXT,  -- 'jd' or 'resume'
        filename TEXT,
        content TEXT,
        extracted_entities TEXT
    )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database initialized and table created successfully.")
