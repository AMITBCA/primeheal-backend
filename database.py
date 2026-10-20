import sqlite3
import json
import uuid
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "primeheal.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Cases table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id TEXT PRIMARY KEY,
        patient_name TEXT,
        age TEXT,
        sex TEXT,
        occupation TEXT,
        address TEXT,
        phone TEXT,
        email TEXT,
        weight TEXT,
        height TEXT,
        complaints TEXT,
        associated_complaints TEXT,
        history TEXT,
        mentals TEXT,
        vitals TEXT,
        general_exam TEXT,
        systemic_exam TEXT,
        local_exam TEXT,
        modalities TEXT,
        reports TEXT,
        notes TEXT,
        result TEXT,
        doctor_override TEXT,
        archived INTEGER DEFAULT 0,
        created_at TEXT,
        updated_at TEXT
    )
    """)
    
    # Followups table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followups (
        id TEXT PRIMARY KEY,
        case_id TEXT,
        date TEXT,
        complaints TEXT,
        assessment TEXT,
        remedy TEXT,
        potency TEXT,
        dose TEXT,
        rationale TEXT,
        changes TEXT,
        created_at TEXT,
        FOREIGN KEY (case_id) REFERENCES cases (id)
    )
    """)
    
    # Case chats table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS case_chats (
        id TEXT PRIMARY KEY,
        case_id TEXT,
        role TEXT,
        message TEXT,
        created_at TEXT
    )
    """)
    
    # General chats table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS general_chats (
        id TEXT PRIMARY KEY,
        session_id TEXT,
        role TEXT,
        message TEXT,
        created_at TEXT
    )
    """)
    
    # App Settings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized at", DB_PATH)
