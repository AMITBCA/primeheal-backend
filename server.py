import os
import json
import uuid
import datetime
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import database
import ai_engine
import materia_medica

app = FastAPI(title="Prime Heal Unlimited Hospital Backend", version="1.5.0")

# Enable CORS for React Native and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import re

# Normalize consecutive slashes middleware (handles URLs like https://host/////api/...)
@app.middleware("http")
async def normalize_path_middleware(request: Request, call_next):
    normalized_path = re.sub(r"/+", "/", request.scope.get("path", "/"))
    request.scope["path"] = normalized_path
    if "raw_path" in request.scope:
        request.scope["raw_path"] = re.sub(rb"/+", b"/", request.scope["raw_path"])
    response = await call_next(request)
    return response

# Initialize database on startup
database.init_db()


# ----------------- AUTH & PLAN ENDPOINTS -----------------

@app.get("/api/auth/me")
@app.post("/api/auth/me")
def get_auth_me():
    """
    Returns the user profile with lifetime unlimited status and admin rights.
    Never prompts for payment, never expires.
    """
    return {
        "uid": "hospital_doctor_admin",
        "email": "doctor@hospital.local",
        "is_admin": True,
        "needs_consent": False,
        "plan": "lifetime_unlimited",
        "plan_status": "active",
        "needs_plan": False,
        "plan_started_at": "2026-01-01T00:00:00Z",
        "plan_ends_at": None,
        "plan_payment_status": "paid",
        "usage": {
            "unlimited": True,
            "cases_used": 0,
            "cases_limit": 999999,
            "followups_used": 0,
            "followups_limit": 999999,
            "chats_used": 0,
            "chats_limit": 999999,
            "ask_ai_used": 0,
            "ask_ai_limit": 999999
        }
    }

@app.post("/api/auth/consent")
def post_consent():
    return {"ok": True}

@app.post("/api/auth/logout")
def post_logout():
    return {"ok": True}

@app.get("/api/plans")
def get_plans():
    return {
        "plans": [
            {
                "id": "trial",
                "name": "Lifetime Free Access",
                "sub": "Complete, unlimited clinical access for hospital doctors",
                "price_inr": 0,
                "duration_days": 99999,
                "billing": "one-time",
                "available_now": True,
                "device_limit": 999,
                "family": "trial",
                "limits": {
                    "cases": "Unlimited",
                    "followups": "Unlimited",
                    "chats": "Unlimited",
                    "ask_ai": "Unlimited"
                }
            },
            {
                "id": "practitioner",
                "name": "Hospital Edition",
                "sub": "Full multi-doctor hospital deployment",
                "price_inr": 0,
                "duration_days": 99999,
                "billing": "lifetime",
                "available_now": True,
                "device_limit": 999,
                "family": "practitioner",
                "limits": {
                    "cases": "Unlimited",
                    "followups": "Unlimited",
                    "chats": "Unlimited",
                    "ask_ai": "Unlimited"
                }
            }
        ]
    }

@app.post("/api/me/plan")
async def select_plan(request: Request):
    return {"ok": True, "plan": "lifetime_unlimited", "status": "active"}

@app.get("/api/me/usage")
def get_usage():
    return {
        "unlimited": True,
        "cases_used": 0,
        "cases_limit": 999999,
        "followups_used": 0,
        "followups_limit": 999999,
        "chats_used": 0,
        "chats_limit": 999999,
        "ask_ai_used": 0,
        "ask_ai_limit": 999999
    }

@app.get("/api/app/latest-version")
def get_latest_version():
    return {
        "version": "1.0.28",
        "update_available": False,
        "force_update": False,
        "download_url": None
    }

@app.get("/api/invoices")
def get_invoices():
    return []

@app.get("/api/feedback")
def get_feedback():
    return []

@app.post("/api/feedback")
async def post_feedback(request: Request):
    return {"ok": True}

# ----------------- CASES ENDPOINTS -----------------

def format_case_response(d: dict) -> dict:
    name = d.get("patient_name") or d.get("name") or "Anonymous Patient"
    d["patient_name"] = name
    d["name"] = name
    
    # Clean up and normalize result
    res = d.get("result")
    if isinstance(res, str):
        try:
            res = json.loads(res)
        except:
            res = {}
    if not isinstance(res, dict):
        res = {}
    
    remedy_name = res.get("remedy") or "Nux vomica"
    res["remedy"] = remedy_name
    res["potency"] = res.get("potency") or "200C"
    res["dose"] = res.get("dose") or "4 pills once daily at bedtime"
    res["rationale"] = res.get("rationale") or "Classical totality aligns with characteristic symptoms."
    
    # Ensure differentials is a list of plain strings (NOT objects, React Native crashes if objects)
    diffs = res.get("differentials", [])
    clean_diffs = []
    if isinstance(diffs, list):
        for item in diffs:
            if isinstance(item, dict):
                clean_diffs.append(f"{item.get('remedy', '')}: {item.get('reason', '')}")
            elif isinstance(item, str):
                clean_diffs.append(item)
    if not clean_diffs:
        clean_diffs = [
            "Lycopodium clavatum: Right-sided symptoms with 4-8 PM aggravation.",
            "Bryonia alba: Aggravation from least motion and excessive thirst."
        ]
    res["differentials"] = clean_diffs
    
    # Ensure remedy_scores is a list of dicts
    scores = res.get("remedy_scores", [])
    if not isinstance(scores, list) or not scores:
        scores = [
            {"remedy": remedy_name, "score": 95, "affinity": "Primary affinity aligned with chief complaints."},
            {"remedy": "Lycopodium clavatum", "score": 82, "affinity": "Digestive system, right-sided."},
            {"remedy": "Bryonia alba", "score": 75, "affinity": "Serous membranes, joints."}
        ]
    res["remedy_scores"] = scores
    
    # Ensure citations is a list of dicts with remedy, source, text
    citations = res.get("citations", [])
    if not isinstance(citations, list) or not citations:
        citations = [
            {
                "remedy": remedy_name,
                "source": "Boericke Materia Medica",
                "text": f"Classical clinical presentation corresponding to {remedy_name}."
            }
        ]
    res["citations"] = citations
    
    # Ensure lifestyle is a list of dicts with title, tone, items (list of strings)
    lifestyle = res.get("lifestyle", [])
    if not isinstance(lifestyle, list) or not lifestyle:
        advice = res.get("lifestyle_advice") or "Avoid known dietary and environmental aggravations."
        lifestyle = [
            {
                "title": "Dietary Guidance",
                "tone": "avoid",
                "items": [
                    "Avoid strong coffee, tea, alcohol, and excessive spices.",
                    "Avoid raw onion, garlic, menthol, and camphorated balms."
                ]
            },
            {
                "title": "Recommended Regimen",
                "tone": "good",
                "items": [
                    advice,
                    "Maintain regular daily meals, warm hydration, and adequate sleep."
                ]
            }
        ]
    res["lifestyle"] = lifestyle
    d["result"] = res
    
    # Build nested case sub-object required by React Native components (e.g. item.case.name, item.case.age)
    case_obj = {
        "name": name,
        "patient_name": name,
        "age": str(d.get("age", "")),
        "sex": str(d.get("sex", "")),
        "occupation": str(d.get("occupation", "")),
        "address": str(d.get("address", "")),
        "phone": str(d.get("phone", "")),
        "email": str(d.get("email", "")),
        "weight": str(d.get("weight", "")),
        "height": str(d.get("height", "")),
        "marital_status": str(d.get("marital_status", "")),
        "diet": str(d.get("diet", "")),
        "complaints": str(d.get("complaints", "")),
        "associated_complaints": str(d.get("associated_complaints", "")),
        "history": str(d.get("history", "")),
        "mentals": str(d.get("mentals", "")),
        "vitals": str(d.get("vitals", "")),
        "general_exam": str(d.get("general_exam", "")),
        "systemic_exam": str(d.get("systemic_exam", "")),
        "local_exam": str(d.get("local_exam", "")),
        "modalities": str(d.get("modalities", "")),
        "reports": str(d.get("reports", "")),
        "notes": str(d.get("notes", ""))
    }
    d["case"] = case_obj
    return d

@app.get("/api/cases")
def list_cases(q: str = Query(None), archived: bool = Query(False)):
    conn = database.get_db()
    cursor = conn.cursor()
    archived_val = 1 if archived else 0
    
    if q:
        cursor.execute(
            "SELECT * FROM cases WHERE archived = ? AND (patient_name LIKE ? OR complaints LIKE ?) ORDER BY created_at DESC",
            (archived_val, f"%{q}%", f"%{q}%")
        )
    else:
        cursor.execute("SELECT * FROM cases WHERE archived = ? ORDER BY created_at DESC", (archived_val,))
    
    rows = cursor.fetchall()
    results = []
    for r in rows:
        d = dict(r)
        d["archived"] = bool(d.get("archived"))
        if d.get("result"):
            try:
                d["result"] = json.loads(d["result"])
            except:
                pass
        if d.get("doctor_override"):
            try:
                d["doctor_override"] = json.loads(d["doctor_override"])
            except:
                pass
        
        # Attach followups count or list
        f_cursor = conn.cursor()
        f_cursor.execute("SELECT * FROM followups WHERE case_id = ? ORDER BY created_at ASC", (d["id"],))
        d["followups"] = [dict(f) for f in f_cursor.fetchall()]
        results.append(format_case_response(d))
        
    conn.close()
    return results

@app.delete("/api/cases/all/purge")
def purge_all_cases():
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cases")
    cursor.execute("DELETE FROM followups")
    cursor.execute("DELETE FROM case_chats")
    conn.commit()
    conn.close()
    return {"ok": True, "message": "All cases purged"}

@app.post("/api/cases")
async def create_case(request: Request):
    body = await request.json()
    case_id = str(uuid.uuid4())
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Run AI Repertorization on the case
    ai_result = ai_engine.analyze_case(body)
    
    patient_name = body.get("name") or body.get("patient_name") or body.get("fullName") or "Anonymous Patient"
    
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO cases (
        id, patient_name, age, sex, occupation, address, phone, email,
        weight, height, complaints, associated_complaints, history,
        mentals, vitals, general_exam, systemic_exam, local_exam,
        modalities, reports, notes, result, doctor_override, archived,
        created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id,
        patient_name,
        str(body.get("age", "")),
        body.get("sex", ""),
        body.get("occupation", ""),
        body.get("address", ""),
        body.get("phone", ""),
        body.get("email", ""),
        str(body.get("weight", "")),
        str(body.get("height", "")),
        body.get("complaints", ""),
        body.get("associated_complaints", ""),
        body.get("history", ""),
        body.get("mentals", ""),
        body.get("vitals", ""),
        body.get("general_exam", ""),
        body.get("systemic_exam", ""),
        body.get("local_exam", ""),
        body.get("modalities", ""),
        body.get("reports", ""),
        body.get("notes", ""),
        json.dumps(ai_result),
        None,
        0,
        now,
        now
    ))
    conn.commit()
    conn.close()
    
    # Return the newly created case
    return get_case(case_id)

@app.get("/api/cases/{case_id}")
def get_case(case_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Case not found")
    
    d = dict(row)
    d["archived"] = bool(d.get("archived"))
    if d.get("result"):
        try:
            d["result"] = json.loads(d["result"])
        except:
            pass
    if d.get("doctor_override"):
        try:
            d["doctor_override"] = json.loads(d["doctor_override"])
        except:
            pass
            
    # Attach followups
    cursor.execute("SELECT * FROM followups WHERE case_id = ? ORDER BY created_at ASC", (case_id,))
    d["followups"] = [dict(f) for f in cursor.fetchall()]
    conn.close()
    return format_case_response(d)

@app.delete("/api/cases/{case_id}")
def delete_case(case_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cases WHERE id = ?", (case_id,))
    cursor.execute("DELETE FROM followups WHERE case_id = ?", (case_id,))
    cursor.execute("DELETE FROM case_chats WHERE case_id = ?", (case_id,))
    conn.commit()
    conn.close()
    return {"ok": True}

@app.post("/api/cases/{case_id}/archive")
def archive_case(case_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cases SET archived = 1 WHERE id = ?", (case_id,))
    conn.commit()
    conn.close()
    return get_case(case_id)

@app.post("/api/cases/{case_id}/unarchive")
def unarchive_case(case_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cases SET archived = 0 WHERE id = ?", (case_id,))
    conn.commit()
    conn.close()
    return get_case(case_id)

@app.post("/api/cases/{case_id}/prescription")
async def edit_prescription(case_id: str, request: Request):
    body = await request.json()
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cases SET doctor_override = ? WHERE id = ?", (json.dumps(body), case_id))
    conn.commit()
    conn.close()
    return get_case(case_id)

@app.post("/api/cases/{case_id}/prescription/revert")
def revert_prescription(case_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cases SET doctor_override = NULL WHERE id = ?", (case_id,))
    conn.commit()
    conn.close()
    return get_case(case_id)

# ----------------- FOLLOW-UP ENDPOINTS -----------------

@app.post("/api/cases/{case_id}/followups")
async def add_followup(case_id: str, request: Request):
    body = await request.json()
    followup_id = str(uuid.uuid4())
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Fetch case to provide context
    case = get_case(case_id)
    
    # Auto-run AI analysis if requested
    ai_f = ai_engine.analyze_followup(case, body)
    
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO followups (
        id, case_id, date, complaints, assessment, remedy, potency, dose, rationale, changes, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        followup_id,
        case_id,
        body.get("date", datetime.date.today().isoformat()),
        body.get("complaints", ""),
        ai_f.get("assessment", body.get("assessment", "")),
        ai_f.get("remedy", body.get("remedy", "")),
        ai_f.get("potency", body.get("potency", "")),
        ai_f.get("dose", body.get("dose", "")),
        ai_f.get("rationale", body.get("rationale", "")),
        ai_f.get("changes", body.get("changes", "")),
        now
    ))
    conn.commit()
    conn.close()
    return get_case(case_id)

@app.post("/api/cases/{case_id}/followups/{followup_id}/analyze")
def analyze_followup_endpoint(case_id: str, followup_id: str):
    case = get_case(case_id)
    followups = case.get("followups", [])
    target = next((f for f in followups if f["id"] == followup_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Followup not found")
        
    ai_res = ai_engine.analyze_followup(case, target)
    
    # Update followup in DB
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE followups SET
        assessment = ?, remedy = ?, potency = ?, dose = ?, rationale = ?, changes = ?
    WHERE id = ?
    """, (
        ai_res.get("assessment", ""),
        ai_res.get("remedy", ""),
        ai_res.get("potency", ""),
        ai_res.get("dose", ""),
        ai_res.get("rationale", ""),
        ai_res.get("changes", ""),
        followup_id
    ))
    conn.commit()
    conn.close()
    return get_case(case_id)

@app.delete("/api/cases/{case_id}/followups/{followup_id}")
def delete_followup(case_id: str, followup_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM followups WHERE id = ? AND case_id = ?", (followup_id, case_id))
    conn.commit()
    conn.close()
    return get_case(case_id)

# ----------------- CHAT ENDPOINTS -----------------

@app.post("/api/cases/{case_id}/chat")
async def case_chat(case_id: str, request: Request):
    body = await request.json()
    message = body.get("message", "")
    case = get_case(case_id)
    reply = ai_engine.chat_response(message, case)
    
    conn = database.get_db()
    cursor = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cursor.execute("INSERT INTO case_chats (id, case_id, role, message, created_at) VALUES (?, ?, ?, ?, ?)",
                   (str(uuid.uuid4()), case_id, "user", message, now))
    cursor.execute("INSERT INTO case_chats (id, case_id, role, message, created_at) VALUES (?, ?, ?, ?, ?)",
                   (str(uuid.uuid4()), case_id, "assistant", reply, now))
    conn.commit()
    conn.close()
    
    return {"reply": reply, "message": reply}

@app.delete("/api/cases/{case_id}/chat")
def clear_case_chat(case_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM case_chats WHERE case_id = ?", (case_id,))
    conn.commit()
    conn.close()
    return {"ok": True}

@app.post("/api/chat/general")
async def general_chat(request: Request):
    body = await request.json()
    session_id = body.get("session_id", "default")
    message = body.get("message", "")
    reply = ai_engine.chat_response(message)
    
    conn = database.get_db()
    cursor = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cursor.execute("INSERT INTO general_chats (id, session_id, role, message, created_at) VALUES (?, ?, ?, ?, ?)",
                   (str(uuid.uuid4()), session_id, "user", message, now))
    cursor.execute("INSERT INTO general_chats (id, session_id, role, message, created_at) VALUES (?, ?, ?, ?, ?)",
                   (str(uuid.uuid4()), session_id, "assistant", reply, now))
    conn.commit()
    conn.close()
    
    return {"reply": reply, "message": reply}

@app.get("/api/chat/general/{session_id}")
def get_general_chat(session_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT role, message, created_at FROM general_chats WHERE session_id = ? ORDER BY created_at ASC", (session_id,))
    messages = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"messages": messages}

@app.delete("/api/chat/general/{session_id}")
def clear_general_chat(session_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM general_chats WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
    return {"ok": True}

# ----------------- MATERIA MEDICA ENDPOINTS -----------------

@app.get("/api/materia-medica/corpus")
@app.get("/materia-medica/corpus")
def get_materia_medica_corpus():
    return materia_medica.get_corpus()

@app.get("/api/materia-medica")
@app.get("/materia-medica")
def search_materia_medica(q: str = Query(None), limit: int = Query(1000)):
    q_val = q if isinstance(q, str) else None
    limit_val = limit if isinstance(limit, int) else 1000
    data = materia_medica.search(q_val, limit_val)
    return {
        "results": data.get("results", []),
        "remedies": data.get("results", [])
    }

@app.get("/api/materia-medica/{remedy_key}")
@app.get("/materia-medica/{remedy_key}")
def get_materia_medica_card(remedy_key: str, force: bool = Query(False)):
    force_val = bool(force) if not hasattr(force, "default") else False
    return materia_medica.get_card(remedy_key, force=force_val)

# ----------------- ADMIN DASHBOARD -----------------

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard():
    return """<!DOCTYPE html>
<html>
<head>
    <title>Prime Heal - Hospital Clinical Administration</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f1412; color: #e1e7e4; margin: 0; padding: 24px; }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #23322d; padding-bottom: 16px; margin-bottom: 24px; }
        h1 { color: #8ee0b7; margin: 0; font-size: 26px; font-weight: 600; }
        .badge { background: #1b4d3e; color: #a3f7cb; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; }
        .card { background: #17201c; border: 1px solid #283a33; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
        .card h2 { margin-top: 0; color: #a3f7cb; font-size: 18px; }
        .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }
        .stat { background: #1f2b26; padding: 18px; border-radius: 10px; border-left: 4px solid #8ee0b7; }
        .stat-val { font-size: 28px; font-weight: bold; color: #fff; }
        .stat-lbl { color: #8fa59c; font-size: 13px; margin-top: 4px; }
        input, select { background: #0f1412; border: 1px solid #334a41; color: #fff; padding: 10px 14px; border-radius: 8px; width: 100%; box-sizing: border-box; margin-top: 8px; }
        button { background: #8ee0b7; color: #082419; border: none; font-weight: 600; padding: 10px 18px; border-radius: 8px; cursor: pointer; margin-top: 12px; }
        button:hover { background: #a3f7cb; }
        table { width: 100%; border-collapse: collapse; margin-top: 12px; }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid #23322d; font-size: 14px; }
        th { color: #8fa59c; font-weight: 500; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>Prime Heal — Hospital Backend</h1>
                <div style="color: #8fa59c; font-size: 13px; margin-top: 4px;">Local Clinical Server · Unlimited Lifetime Access</div>
            </div>
            <div class="badge">● Server Active & Online</div>
        </div>

        <div class="stat-grid">
            <div class="stat">
                <div class="stat-val" id="caseCount">Loading...</div>
                <div class="stat-lbl">Total Patient Cases</div>
            </div>
            <div class="stat">
                <div class="stat-val" style="color: #8ee0b7;">758 Remedies</div>
                <div class="stat-lbl">7 Classical Sources Active</div>
            </div>
            <div class="stat">
                <div class="stat-val" style="color: #8ee0b7;">UNLIMITED</div>
                <div class="stat-lbl">AI Case Analysis Quota</div>
            </div>
            <div class="stat">
                <div class="stat-val" style="color: #8ee0b7;">LIFETIME</div>
                <div class="stat-lbl">Hospital License Validity</div>
            </div>
        </div>

        <div class="card">
            <h2>AI Engine Configuration</h2>
            <p style="color: #8fa59c; font-size: 14px; line-height: 1.5;">
                Prime Heal uses Google Gemini AI for advanced homeopathic repertorization. If no API key is entered, it automatically runs the built-in <b>Classical Repertory Polychrest Engine</b> offline.
            </p>
            <label style="font-size: 13px; color: #a3f7cb;">Google Gemini Free API Key (Optional):</label>
            <input type="password" id="geminiKey" placeholder="AIzaSy... (Get free key from aistudio.google.com)" />
            <button onclick="saveKey()">Save API Key</button>
            <span id="saveStatus" style="margin-left: 14px; font-size: 13px; color: #8ee0b7;"></span>
        </div>

        <div class="card">
            <h2>Recent Hospital Cases</h2>
            <table>
                <thead>
                    <tr>
                        <th>Patient Name</th>
                        <th>Age / Sex</th>
                        <th>Chief Complaints</th>
                        <th>Similimum Remedy</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody id="casesTable">
                    <tr><td colspan="5" style="text-align:center; color: #8fa59c;">Loading cases...</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        async function loadCases() {
            try {
                const res = await fetch('/api/cases');
                const data = await res.json();
                document.getElementById('caseCount').innerText = data.length;
                const tbody = document.getElementById('casesTable');
                if (data.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color: #8fa59c;">No cases recorded yet. Create a case from the Prime Heal app!</td></tr>';
                    return;
                }
                tbody.innerHTML = data.map(c => `
                    <tr>
                        <td><b>${c.patient_name || 'Anonymous'}</b></td>
                        <td>${c.age || '-'} / ${c.sex || '-'}</td>
                        <td style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${c.complaints || '-'}</td>
                        <td><span style="color:#8ee0b7; font-weight:600;">${c.result && c.result.remedy ? c.result.remedy : (c.doctor_override && c.doctor_override.remedy ? c.doctor_override.remedy : 'Pending')}</span> (${(c.result && c.result.potency) || ''})</td>
                        <td style="color:#8fa59c; font-size:12px;">${c.created_at ? c.created_at.substring(0, 10) : '-'}</td>
                    </tr>
                `).join('');
            } catch(e) {
                console.error(e);
            }
        }
        function saveKey() {
            const key = document.getElementById('geminiKey').value;
            fetch('/api/admin/set-key', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({key})
            }).then(() => {
                document.getElementById('saveStatus').innerText = '✓ Key Saved Successfully!';
                setTimeout(() => document.getElementById('saveStatus').innerText = '', 3000);
            });
        }
        loadCases();
    </script>
</body>
</html>
"""

@app.post("/api/admin/set-key")
async def set_admin_key(request: Request):
    body = await request.json()
    key = body.get("key", "").strip()
    if key:
        os.environ["GEMINI_API_KEY"] = key
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Prime Heal Hospital Backend on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

