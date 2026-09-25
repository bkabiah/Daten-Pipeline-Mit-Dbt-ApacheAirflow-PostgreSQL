import os
import psycopg2
from pypdf import PdfReader
from fpdf import FPDF
from datetime import datetime
import uuid

# 1. Dummy PDFs generieren (für die Demo)
def generate_dummy_pdfs(output_dir="/opt/airflow/dags/data"):
    os.makedirs(output_dir, exist_ok=True)
    texts = [
        "Dies ist ein Vertragsdokument. Der Vertrag wird zwischen Partei A und Partei B geschlossen.",
        "Rechnung Nr. 12345. Bitte überweisen Sie den Betrag innerhalb von 14 Tagen.",
        "Vertrag über Dienstleistungen. Laufzeit 12 Monate. Kündigung ist möglich."
    ]
    paths = []
    for i, text in enumerate(texts):
        path = os.path.join(output_dir, f"doc_{i+1}.pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(path)
        paths.append(path)
    return paths

# 2. PDFs extrahieren und in Postgres (Raw Layer) speichern
def extract_and_load_to_postgres(**kwargs):
    paths = generate_dummy_pdfs()
    
    conn = psycopg2.connect(
        dbname="airflow", user="airflow", password="airflow", host="postgres", port="5432"
    )
    cur = conn.cursor()
    
    # Raw Tabelle erstellen
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS raw; CREATE TABLE IF NOT EXISTS raw.documents (
            id VARCHAR PRIMARY KEY,
            file_name VARCHAR,
            page_count INT,
            word_count INT,
            extracted_text TEXT,
            created_at TIMESTAMP
        );
    """)
    conn.commit()

    for path in paths:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            
        doc_id = str(uuid.uuid4())
        file_name = os.path.basename(path)
        page_count = len(reader.pages)
        word_count = len(text.split())
        
        cur.execute("""
            INSERT INTO raw.documents (id, file_name, page_count, word_count, extracted_text, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (doc_id, file_name, page_count, word_count, text, datetime.now()))
        
    conn.commit()
    cur.close()
    conn.close()
    print(f"Erfolgreich {len(paths)} Dokumente extrahiert und geladen.")
