import sqlite3
import json
import uuid
import datetime
import os
import sys

# Local SQLite DB Path
DB_PATH = os.path.join(os.path.dirname(__file__), "primeheal.db")
PG_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "postgres_url.txt")

try:
    import psycopg2
    import psycopg2.extras
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False


def get_database_url():
    """Retrieve PostgreSQL connection URL from environment or local config."""
    url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or os.environ.get("RENDER_POSTGRES_URL")
    if not url and os.path.exists(PG_CONFIG_FILE):
        try:
            with open(PG_CONFIG_FILE, "r", encoding="utf-8") as f:
                url = f.read().strip()
        except:
            url = None
    if url:
        url = url.strip()
        # Normalize postgres:// to postgresql:// for psycopg2
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
    return url or None


class PgCursorWrapper:
    """Wrapper around psycopg2 cursor to translate '?' parameter placeholders to '%s'."""
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query, params=None):
        clean_query = query.replace("?", "%s")
        if params is not None:
            return self._cursor.execute(clean_query, params)
        return self._cursor.execute(clean_query)

    def executemany(self, query, seq_of_params):
        clean_query = query.replace("?", "%s")
        return self._cursor.executemany(clean_query, seq_of_params)

    def fetchone(self):
        row = self._cursor.fetchone()
        if row is not None:
            return dict(row)
        return None

    def fetchall(self):
        rows = self._cursor.fetchall()
        return [dict(r) for r in rows]

    def __getattr__(self, name):
        return getattr(self._cursor, name)


class PgConnectionWrapper:
    """Wrapper around psycopg2 connection matching sqlite3 connection interface."""
    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return PgCursorWrapper(cur)

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()


def get_db():
    """Get active database connection (PostgreSQL if configured, else SQLite)."""
    db_url = get_database_url()
    if db_url and HAS_PSYCOPG2:
        try:
            pg_conn = psycopg2.connect(db_url)
            return PgConnectionWrapper(pg_conn)
        except Exception as e:
            print(f"[Database] Warning: PostgreSQL connection failed ({e}), falling back to SQLite.", file=sys.stderr)
            
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_engine_info():
    """Returns metadata about the active storage engine."""
    db_url = get_database_url()
    is_pg = bool(db_url and HAS_PSYCOPG2)
    engine = "PostgreSQL (Cloud Persistent)" if is_pg else "SQLite (Local/Tracked)"
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cases")
    cnt_row = cursor.fetchone()
    cases_cnt = list(cnt_row.values())[0] if isinstance(cnt_row, dict) else (cnt_row[0] if cnt_row else 0)
    conn.close()
    
    return {
        "engine": engine,
        "is_postgres": is_pg,
        "persistent": True,
        "cases_count": cases_cnt,
        "database_url_configured": bool(db_url)
    }


def migrate_sqlite_to_pg_if_needed():
    """If connected to PostgreSQL and cases table is empty, auto-migrate cases from SQLite primeheal.db."""
    if not (get_database_url() and HAS_PSYCOPG2 and os.path.exists(DB_PATH)):
        return

    try:
        # Check PG cases count
        pg_conn = get_db()
        cursor = pg_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cases")
        cnt_row = cursor.fetchone()
        pg_cnt = list(cnt_row.values())[0] if isinstance(cnt_row, dict) else (cnt_row[0] if cnt_row else 0)
        
        if pg_cnt == 0:
            print("[Database] Migrating existing cases from local primeheal.db into cloud PostgreSQL...")
            local_conn = sqlite3.connect(DB_PATH)
            local_conn.row_factory = sqlite3.Row
            l_cur = local_conn.cursor()
            
            l_cur.execute("SELECT * FROM cases")
            cases_rows = [dict(r) for r in l_cur.fetchall()]
            for c in cases_rows:
                cursor.execute("""
                INSERT INTO cases (
                    id, patient_name, age, sex, occupation, address, phone, email,
                    weight, height, complaints, associated_complaints, history,
                    mentals, vitals, general_exam, systemic_exam, local_exam,
                    modalities, reports, notes,
                    appetite, cravings, aversions, thirst, thermal, perspiration,
                    stool, urine, sleep, sleep_position, past_history,
                    vaccination, family_history, diet, marital_status, raw_data,
                    result, doctor_override, archived,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (id) DO NOTHING
                """, (
                    c.get("id"), c.get("patient_name"), str(c.get("age", "")), c.get("sex"),
                    c.get("occupation"), c.get("address"), c.get("phone"), c.get("email"),
                    str(c.get("weight", "")), str(c.get("height", "")), c.get("complaints"),
                    c.get("associated_complaints"), c.get("history"), c.get("mentals"),
                    c.get("vitals"), c.get("general_exam"), c.get("systemic_exam"),
                    c.get("local_exam"), c.get("modalities"), c.get("reports"),
                    c.get("notes"),
                    c.get("appetite", ""), c.get("cravings", ""), c.get("aversions", ""),
                    c.get("thirst", ""), c.get("thermal", ""), c.get("perspiration", ""),
                    c.get("stool", ""), c.get("urine", ""), c.get("sleep", ""),
                    c.get("sleep_position", ""), c.get("past_history", ""),
                    c.get("vaccination", ""), c.get("family_history", ""),
                    c.get("diet", ""), c.get("marital_status", ""), c.get("raw_data", ""),
                    c.get("result"), c.get("doctor_override"),
                    1 if c.get("archived") else 0, c.get("created_at"), c.get("updated_at")
                ))
            
            # Followups
            l_cur.execute("SELECT * FROM followups")
            for f in [dict(r) for r in l_cur.fetchall()]:
                cursor.execute("""
                INSERT INTO followups (id, case_id, date, complaints, assessment, remedy, potency, dose, rationale, changes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (id) DO NOTHING
                """, (
                    f.get("id"), f.get("case_id"), f.get("date"), f.get("complaints"),
                    f.get("assessment"), f.get("remedy"), f.get("potency"), f.get("dose"),
                    f.get("rationale"), f.get("changes"), f.get("created_at")
                ))
                
            pg_conn.commit()
            local_conn.close()
            print(f"[Database] Migrated {len(cases_rows)} cases into PostgreSQL successfully!")
        pg_conn.close()
    except Exception as e:
        print(f"[Database] Migration note: {e}")


NEW_CASE_COLUMNS = [
    ("appetite", "TEXT"),
    ("cravings", "TEXT"),
    ("aversions", "TEXT"),
    ("thirst", "TEXT"),
    ("thermal", "TEXT"),
    ("perspiration", "TEXT"),
    ("stool", "TEXT"),
    ("urine", "TEXT"),
    ("sleep", "TEXT"),
    ("sleep_position", "TEXT"),
    ("past_history", "TEXT"),
    ("vaccination", "TEXT"),
    ("family_history", "TEXT"),
    ("diet", "TEXT"),
    ("marital_status", "TEXT"),
    ("raw_data", "TEXT"),
    ("upstream_case_id", "TEXT")
]


def ensure_case_columns(conn):
    """Ensures all clinical and case summary columns exist in SQLite or PostgreSQL."""
    try:
        cursor = conn.cursor()
        existing_cols = set()
        
        # Try SQLite pragma first
        try:
            cursor.execute("PRAGMA table_info(cases)")
            rows = cursor.fetchall()
            for r in rows:
                if isinstance(r, dict):
                    existing_cols.add(r.get("name", "").lower())
                else:
                    existing_cols.add(r[1].lower())
        except:
            pass
            
        # If no columns found from PRAGMA, try PostgreSQL information_schema
        if not existing_cols:
            try:
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'cases'")
                rows = cursor.fetchall()
                for r in rows:
                    if isinstance(r, dict):
                        existing_cols.add(r.get("column_name", "").lower())
                    else:
                        existing_cols.add(r[0].lower())
            except:
                pass
                
        for col_name, col_type in NEW_CASE_COLUMNS:
            if col_name.lower() not in existing_cols:
                try:
                    cursor.execute(f"ALTER TABLE cases ADD COLUMN {col_name} {col_type}")
                    print(f"[Database] Added column '{col_name}' to cases table.")
                except Exception as ex:
                    # Ignore if column already exists
                    pass
        conn.commit()
    except Exception as e:
        print(f"[Database] Column migration note: {e}")


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
        appetite TEXT,
        cravings TEXT,
        aversions TEXT,
        thirst TEXT,
        thermal TEXT,
        perspiration TEXT,
        stool TEXT,
        urine TEXT,
        sleep TEXT,
        sleep_position TEXT,
        past_history TEXT,
        vaccination TEXT,
        family_history TEXT,
        diet TEXT,
        marital_status TEXT,
        raw_data TEXT,
        result TEXT,
        doctor_override TEXT,
        archived INTEGER DEFAULT 0,
        created_at TEXT,
        updated_at TEXT
    )
    """)
    conn.commit()
    
    # Ensure any missing columns in pre-existing DB are added
    ensure_case_columns(conn)
    
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
        created_at TEXT
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
    
    # Run auto-migration if PG is active
    migrate_sqlite_to_pg_if_needed()
    
    # Ensure all golden reference cases exist
    try:
        import seed_cases
        c_seed = get_db()
        seed_cases.seed(c_seed)
        c_seed.close()
    except Exception as e:
        print(f"[Database] Golden seeding note: {e}")


def export_all_data():
    """Exports entire database as a portable JSON structure for 1-click lifetime backup."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cases ORDER BY created_at DESC")
    cases = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM followups ORDER BY created_at ASC")
    followups = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM case_chats ORDER BY created_at ASC")
    case_chats = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM general_chats ORDER BY created_at ASC")
    general_chats = [dict(r) for r in cursor.fetchall()]
    
    conn.close()
    
    return {
        "version": "1.0",
        "exported_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "cases": cases,
        "followups": followups,
        "case_chats": case_chats,
        "general_chats": general_chats
    }


def import_all_data(data: dict) -> int:
    """Restores all cases and related data from a JSON backup. Returns count of cases imported."""
    cases = data.get("cases", [])
    followups = data.get("followups", [])
    case_chats = data.get("case_chats", [])
    general_chats = data.get("general_chats", [])
    
    conn = get_db()
    cursor = conn.cursor()
    
    count = 0
    for c in cases:
        c_dict = dict(c)
        cursor.execute("DELETE FROM cases WHERE id = ?", (c_dict.get("id"),))
        cursor.execute("""
        INSERT INTO cases (
            id, patient_name, age, sex, occupation, address, phone, email,
            weight, height, complaints, associated_complaints, history,
            mentals, vitals, general_exam, systemic_exam, local_exam,
            modalities, reports, notes,
            appetite, cravings, aversions, thirst, thermal, perspiration,
            stool, urine, sleep, sleep_position, past_history,
            vaccination, family_history, diet, marital_status, raw_data,
            result, doctor_override, archived,
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c_dict.get("id"), c_dict.get("patient_name") or c_dict.get("name"), str(c_dict.get("age", "")),
            c_dict.get("sex", ""), c_dict.get("occupation", ""), c_dict.get("address", ""),
            c_dict.get("phone", ""), c_dict.get("email", ""), str(c_dict.get("weight", "")),
            str(c_dict.get("height", "")), c_dict.get("complaints", ""), c_dict.get("associated_complaints", ""),
            c_dict.get("history", ""), c_dict.get("mentals", ""), c_dict.get("vitals", ""),
            c_dict.get("general_exam", ""), c_dict.get("systemic_exam", ""), c_dict.get("local_exam", ""),
            c_dict.get("modalities", ""), c_dict.get("reports", ""), c_dict.get("notes", ""),
            c_dict.get("appetite", ""), c_dict.get("cravings", ""), c_dict.get("aversions", ""),
            c_dict.get("thirst", ""), c_dict.get("thermal", ""), c_dict.get("perspiration", ""),
            c_dict.get("stool", ""), c_dict.get("urine", ""), c_dict.get("sleep", ""),
            c_dict.get("sleep_position", ""), c_dict.get("past_history", ""),
            c_dict.get("vaccination", ""), c_dict.get("family_history", ""),
            c_dict.get("diet", ""), c_dict.get("marital_status", ""), c_dict.get("raw_data", ""),
            json.dumps(c_dict.get("result")) if isinstance(c_dict.get("result"), dict) else c_dict.get("result", "{}"),
            json.dumps(c_dict.get("doctor_override")) if isinstance(c_dict.get("doctor_override"), dict) else c_dict.get("doctor_override"),
            1 if c_dict.get("archived") else 0,
            c_dict.get("created_at") or datetime.datetime.now(datetime.timezone.utc).isoformat(),
            c_dict.get("updated_at") or datetime.datetime.now(datetime.timezone.utc).isoformat()
        ))
        count += 1
        
    for f in followups:
        f_dict = dict(f)
        cursor.execute("DELETE FROM followups WHERE id = ?", (f_dict.get("id"),))
        cursor.execute("""
        INSERT INTO followups (id, case_id, date, complaints, assessment, remedy, potency, dose, rationale, changes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f_dict.get("id"), f_dict.get("case_id"), f_dict.get("date"), f_dict.get("complaints"),
            f_dict.get("assessment"), f_dict.get("remedy"), f_dict.get("potency"), f_dict.get("dose"),
            f_dict.get("rationale"), f_dict.get("changes"), f_dict.get("created_at")
        ))
        
    for ch in case_chats:
        ch_dict = dict(ch)
        cursor.execute("DELETE FROM case_chats WHERE id = ?", (ch_dict.get("id"),))
        cursor.execute("INSERT INTO case_chats (id, case_id, role, message, created_at) VALUES (?, ?, ?, ?, ?)",
                       (ch_dict.get("id"), ch_dict.get("case_id"), ch_dict.get("role"), ch_dict.get("message") or ch_dict.get("content"), ch_dict.get("created_at")))
                       
    for gc in general_chats:
        gc_dict = dict(gc)
        cursor.execute("DELETE FROM general_chats WHERE id = ?", (gc_dict.get("id"),))
        cursor.execute("INSERT INTO general_chats (id, session_id, role, message, created_at) VALUES (?, ?, ?, ?, ?)",
                       (gc_dict.get("id"), gc_dict.get("session_id"), gc_dict.get("role"), gc_dict.get("message") or gc_dict.get("content"), gc_dict.get("created_at")))
                       
    conn.commit()
    conn.close()
    return count


if __name__ == "__main__":
    init_db()
    info = get_engine_info()
    print("Database initialized successfully!")
    print(f"Active Engine: {info['engine']}")
    print(f"Total Cases: {info['cases_count']}")
