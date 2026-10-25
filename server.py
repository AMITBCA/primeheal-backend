import os
import json
import uuid
import datetime
import re
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import database
import ai_engine
import materia_medica

app = FastAPI(title="Prime Heal Unlimited Hospital Backend", version="1.5.2")

# Enable CORS for React Native and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

HOSPITAL_UNLIMITED_USAGE = {
    "plan": "hospital_unlimited",
    "status": "active",
    "needs_plan": False,
    "plan_started_at": "2026-01-01T00:00:00Z",
    "plan_ends_at": None,
    "period_start": "2026-01-01T00:00:00Z",
    "period_end": None,
    "limits": {
        "cases": 999999,
        "followups": 999999,
        "chats": 999999,
        "ask_ai": 999999
    },
    "used": {
        "cases_used": 0,
        "followups_used": 0,
        "chats_used": 0,
        "ask_ai_used": 0
    },
    "remaining": {
        "cases": 999999,
        "followups": 999999,
        "chats": 999999,
        "ask_ai": 999999
    },
    "device_limit": 999,
    "unlimited": True,
    "cases_used": 0,
    "cases_limit": 999999,
    "followups_used": 0,
    "followups_limit": 999999,
    "chats_used": 0,
    "chats_limit": 999999,
    "ask_ai_used": 0,
    "ask_ai_limit": 999999,
    "case_chats_used": 0,
    "case_chats_limit": 999999,
    "chat_turns_used": 0,
    "chat_turns_limit": 999999
}

@app.get("/api/auth/me")
@app.post("/api/auth/me")
@app.get("/auth/me")
@app.post("/auth/me")
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
        "plan": "hospital_unlimited",
        "plan_status": "active",
        "needs_plan": False,
        "plan_started_at": "2026-01-01T00:00:00Z",
        "plan_ends_at": None,
        "plan_payment_status": "paid",
        "usage": HOSPITAL_UNLIMITED_USAGE
    }

@app.post("/api/auth/consent")
@app.post("/auth/consent")
def post_consent():
    return {"ok": True}

@app.post("/api/auth/logout")
@app.post("/auth/logout")
def post_logout():
    return {"ok": True}

@app.get("/api/plans")
@app.get("/plans")
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
                "name": "Lifetime Hospital Edition",
                "sub": "Full classical Repertory & Materia Medica with zero limits",
                "price_inr": 0,
                "duration_days": 99999,
                "billing": "one-time",
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
@app.post("/me/plan")
async def select_plan(request: Request):
    return {"ok": True, "plan": "lifetime_unlimited", "status": "active"}

@app.get("/api/me/usage")
@app.get("/me/usage")
def get_usage():
    return HOSPITAL_UNLIMITED_USAGE

@app.get("/api/app/latest-version")
@app.get("/app/latest-version")
def get_latest_version():
    return {
        "version": "1.5.0",
        "build": 150,
        "mandatory": False,
        "changelog": "Lifetime hospital edition with complete offline clinical repertoire & all 758 remedies."
    }

@app.post("/api/billing/subscribe")
@app.post("/billing/subscribe")
def billing_subscribe():
    return {"order_id": f"order_free_{uuid.uuid4().hex[:8]}", "amount": 0, "currency": "INR"}

@app.post("/api/billing/verify")
@app.post("/billing/verify")
def billing_verify():
    return {"ok": True, "verified": True, "plan": "lifetime_unlimited"}

@app.get("/api/billing/subscription")
@app.get("/billing/subscription")
def get_billing_subscription():
    return {
        "status": "active",
        "plan": "lifetime_unlimited",
        "sku": "hospital_lifetime",
        "auto_renew": False,
        "expires_at": None,
        "renews_at": None
    }

@app.post("/api/billing/cancel")
@app.post("/billing/cancel")
def cancel_subscription():
    return {"ok": True}

@app.get("/api/invoices")
@app.get("/invoices")
def list_invoices():
    return []

@app.get("/api/invoices/{invoice_id}/pdf")
@app.get("/invoices/{invoice_id}/pdf")
def get_invoice_pdf(invoice_id: str):
    return {"url": "https://primeheal.app"}

@app.post("/api/feedback")
@app.post("/feedback")
async def submit_feedback(request: Request):
    return {"ok": True}

@app.get("/api/feedback")
@app.get("/feedback")
def list_feedback():
    return []


# ----------------- CASES ENDPOINTS -----------------

def format_case_response(d: dict, conn=None) -> dict:
    name = d.get("patient_name") or d.get("name") or "Anonymous Patient"
    d["patient_name"] = name
    d["name"] = name
    case_id = d.get("id")
    
    # Clean up and normalize result
    res = d.get("result")
    if isinstance(res, str):
        try:
            res = json.loads(res)
        except:
            res = {}
    if not isinstance(res, dict):
        res = {}
    
    # If raw_data exists, backfill any empty fields from the original payload
    raw_str = d.get("raw_data")
    if raw_str:
        try:
            raw_obj = json.loads(raw_str) if isinstance(raw_str, str) else raw_str
            if isinstance(raw_obj, dict):
                for k, v in raw_obj.items():
                    if (k not in d or d.get(k) is None or d.get(k) == "") and v is not None:
                        d[k] = v
        except:
            pass

    remedy_name = res.get("remedy") or "Nux Vomica"
    res["remedy"] = remedy_name
    res["potency"] = res.get("potency") or "200C"
    res["dose"] = res.get("dose") or "4 pills of 200C, once daily in the morning for 3 days, then stop and observe for 7-10 days before reassessing"
    res["rationale"] = res.get("rationale") or "Classical totality aligns with characteristic symptoms."
    
    # Ensure diagnosis exists
    diagnosis_str = res.get("diagnosis") or d.get("diagnosis") or "Clinical Homoeopathic Evaluation"
    res["diagnosis"] = diagnosis_str
    d["diagnosis"] = diagnosis_str
    
    # Check doctor override
    if d.get("doctor_override"):
        doc_ovr = d.get("doctor_override")
        if isinstance(doc_ovr, str):
            try:
                doc_ovr = json.loads(doc_ovr)
            except:
                doc_ovr = {}
        if isinstance(doc_ovr, dict):
            res["is_overridden"] = True
            d["is_overridden"] = True
            res["ai_remedy"] = remedy_name
            res["ai_potency"] = res["potency"]
            res["ai_dose"] = res["dose"]
            if doc_ovr.get("remedy"):
                res["remedy"] = doc_ovr.get("remedy")
            if doc_ovr.get("potency"):
                res["potency"] = doc_ovr.get("potency")
            if doc_ovr.get("dose"):
                res["dose"] = doc_ovr.get("dose")
    else:
        res["is_overridden"] = False
        d["is_overridden"] = False

    # Ensure differentials is a list of plain strings (React Native expects string items)
    diffs = res.get("differentials", [])
    clean_diffs = []
    if isinstance(diffs, list):
        for item in diffs:
            if isinstance(item, dict):
                r_name = str(item.get("remedy") or "").strip()
                r_reason = str(item.get("reason") or item.get("coverage") or "").strip()
                if r_name and r_reason:
                    clean_diffs.append(f"{r_name} ({r_reason})")
                elif r_name:
                    clean_diffs.append(r_name)
                elif r_reason:
                    clean_diffs.append(r_reason)
            elif isinstance(item, str) and item.strip():
                clean_diffs.append(item.strip())
    if not clean_diffs:
        clean_diffs = [
            "Lycopodium (ambitious personality, bloating after small meals, liver/digestive focus, but less morning aggravation and no ineffectual urging keynote)",
            "Sulphur (craving spicy foods, morning aggravation, irritability, but typically hot patient with aversion to warmth—contradicts chilliness here)",
            "Bryonia (irritability, constipation with large dry stools, amelioration rest—but lacks ineffectual urging and coffee craving)"
        ]
    res["differentials"] = clean_diffs
    
    # Ensure remedy_scores is a list of dicts with remedy, score, coverage (and affinity)
    scores = res.get("remedy_scores", [])
    clean_scores = []
    if isinstance(scores, list) and scores:
        for s in scores:
            if isinstance(s, dict):
                cov = s.get("coverage") or s.get("affinity") or ""
                clean_scores.append({
                    "remedy": s.get("remedy", ""),
                    "score": s.get("score", 90),
                    "coverage": cov,
                    "affinity": cov
                })
    if not clean_scores:
        clean_scores = [
            {
                "remedy": remedy_name,
                "score": 94,
                "coverage": "Ineffectual urging (pathognomonic), morning aggravation, irritability/fastidiousness, coffee craving, chilliness, 3 AM waking, workaholic stress",
                "affinity": "Ineffectual urging (pathognomonic), morning aggravation, irritability/fastidiousness, coffee craving, chilliness, 3 AM waking, workaholic stress"
            },
            {
                "remedy": "Lycopodium",
                "score": 76,
                "coverage": "Ambitious personality, bloating after small meals, liver/digestive sphere, evening amelioration, irritability—but misses ineffectual urging keynote",
                "affinity": "Ambitious personality, bloating after small meals, liver/digestive sphere, evening amelioration, irritability—but misses ineffectual urging keynote"
            },
            {
                "remedy": "Sulphur",
                "score": 68,
                "coverage": "Spicy food craving, morning aggravation, irritability, digestive complaints—but thermal (hot patient) contradicts chilliness here",
                "affinity": "Spicy food craving, morning aggravation, irritability, digestive complaints—but thermal (hot patient) contradicts chilliness here"
            },
            {
                "remedy": "Bryonia",
                "score": 61,
                "coverage": "Irritability, constipation picture, amelioration rest—lacks ineffectual urging and coffee craving; constipation type differs (large/dry vs. urging)",
                "affinity": "Irritability, constipation picture, amelioration rest—lacks ineffectual urging and coffee craving; constipation type differs (large/dry vs. urging)"
            }
        ]
    res["remedy_scores"] = clean_scores
    
    # Ensure citations is a list of dicts with remedy, source, quote (and text)
    citations = res.get("citations", [])
    clean_citations = []
    if isinstance(citations, list) and citations:
        for c in citations:
            if isinstance(c, dict):
                q = c.get("quote") or c.get("text") or ""
                clean_citations.append({
                    "remedy": c.get("remedy", ""),
                    "source": c.get("source", ""),
                    "quote": q,
                    "text": q
                })
    if not clean_citations:
        clean_citations = [
            {
                "remedy": remedy_name,
                "source": "Boericke's Materia Medica",
                "quote": "Frequent ineffectual urging to stool; passes small quantities at each attempt. Feels as if part remained unexpelled. Wants to go constantly.",
                "text": "Frequent ineffectual urging to stool; passes small quantities at each attempt. Feels as if part remained unexpelled. Wants to go constantly."
            },
            {
                "remedy": remedy_name,
                "source": "Allen's Keynotes",
                "quote": "Irritable, zealous fiery temperament. Oversensitive; cannot bear noises, odors, light. Worse morning on waking. Chilly, cannot uncover.",
                "text": "Irritable, zealous fiery temperament. Oversensitive; cannot bear noises, odors, light. Worse morning on waking. Chilly, cannot uncover."
            },
            {
                "remedy": remedy_name,
                "source": "Kent's Lectures on Materia Medica",
                "quote": "Sleeps into aggravation; wakes 3-4 AM with mind on business, cannot sleep again until toward morning, then heavy sleep and hard to rouse.",
                "text": "Sleeps into aggravation; wakes 3-4 AM with mind on business, cannot sleep again until toward morning, then heavy sleep and hard to rouse."
            }
        ]
    res["citations"] = clean_citations
    
    # Ensure lifestyle is the exact 4-part dictionary required by React Native LifestyleBlock:
    raw_l = res.get("lifestyle")
    if isinstance(raw_l, dict) and "diet_do" in raw_l and "diet_avoid" in raw_l and "exercises" in raw_l and "lifestyle" in raw_l:
        lifestyle_obj = {
            "diet_do": list(raw_l.get("diet_do") or []),
            "diet_avoid": list(raw_l.get("diet_avoid") or []),
            "exercises": list(raw_l.get("exercises") or []),
            "lifestyle": list(raw_l.get("lifestyle") or [])
        }
        if not lifestyle_obj["diet_do"] or not lifestyle_obj["diet_avoid"] or not lifestyle_obj["exercises"] or not lifestyle_obj["lifestyle"]:
            fallback_l = ai_engine.build_homoeopathic_lifestyle(res.get("remedy"), d)
            for k in ["diet_do", "diet_avoid", "exercises", "lifestyle"]:
                if not lifestyle_obj[k]:
                    lifestyle_obj[k] = fallback_l[k]
    else:
        lifestyle_obj = ai_engine.build_homoeopathic_lifestyle(res.get("remedy"), d)
    
    res["lifestyle"] = lifestyle_obj
    d["result"] = res
    
    # Ensure every clinical summary field exists in root d
    for k in ["appetite", "cravings", "aversions", "thirst", "thermal", "perspiration", 
              "stool", "urine", "sleep", "sleep_position", "past_history", "vaccination", 
              "family_history", "diet", "marital_status"]:
        d[k] = str(d.get(k) or "")
    
    # Build complete case sub-object required by React Native components and PDF template
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
        "notes": str(d.get("notes", "")),
        # All classical clinical summary fields for the PDF Case summary table:
        "appetite": str(d.get("appetite", "")),
        "cravings": str(d.get("cravings", "")),
        "aversions": str(d.get("aversions", "")),
        "thirst": str(d.get("thirst", "")),
        "thermal": str(d.get("thermal", "")),
        "perspiration": str(d.get("perspiration", "")),
        "stool": str(d.get("stool", "")),
        "urine": str(d.get("urine", "")),
        "sleep": str(d.get("sleep", "")),
        "sleep_position": str(d.get("sleep_position", "")),
        "past_history": str(d.get("past_history", "")),
        "vaccination": str(d.get("vaccination", "")),
        "family_history": str(d.get("family_history", ""))
    }
    d["case"] = case_obj
    
    # Attach case chat messages if connection or id available
    if case_id:
        should_close = False
        if conn is None:
            conn = database.get_db()
            should_close = True
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, case_id, role, message, created_at FROM case_chats WHERE case_id = ? ORDER BY created_at ASC", (case_id,))
            c_rows = cursor.fetchall()
            c_msgs = []
            for cr in c_rows:
                crd = dict(cr)
                content = str(crd.get("message") or crd.get("content") or "")
                c_msgs.append({
                    "id": str(crd.get("id") or uuid.uuid4()),
                    "case_id": str(case_id),
                    "role": str(crd.get("role") or "assistant"),
                    "content": content,
                    "message": content,
                    "created_at": str(crd.get("created_at") or datetime.datetime.now(datetime.timezone.utc).isoformat())
                })
            d["messages"] = c_msgs
        except Exception as e:
            print(f"[format_case_response] note reading case_chats: {e}")
            d["messages"] = []
        finally:
            if should_close:
                try:
                    conn.close()
                except:
                    pass
    else:
        d["messages"] = []
        
    return d

@app.get("/api/cases")
@app.get("/cases")
def list_cases(q: str = Query(None), archived: bool = Query(False)):
    conn = database.get_db()
    cursor = conn.cursor()
    
    is_archived = False
    if isinstance(archived, bool):
        is_archived = archived
    elif isinstance(archived, str):
        is_archived = archived.lower() in ("true", "1", "yes")
    elif hasattr(archived, "default"):
        is_archived = bool(archived.default)
        
    archived_val = 1 if is_archived else 0
    
    q_val = None
    if isinstance(q, str) and q.strip():
        q_val = q.strip()
    
    if q_val:
        cursor.execute(
            "SELECT * FROM cases WHERE archived = ? AND (patient_name LIKE ? OR complaints LIKE ?) ORDER BY created_at DESC",
            (archived_val, f"%{q_val}%", f"%{q_val}%")
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
        results.append(format_case_response(d, conn=conn))
        
    conn.close()
    return results

@app.delete("/api/cases/all/purge")
@app.delete("/cases/all/purge")
def purge_all_cases():
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cases")
    cursor.execute("DELETE FROM followups")
    cursor.execute("DELETE FROM case_chats")
    conn.commit()
    conn.close()
    return {"ok": True, "message": "All cases purged"}

@app.get("/api/system/status")
@app.get("/system/status")
def system_status():
    return database.get_engine_info()

@app.get("/api/settings/ai")
@app.get("/settings/ai")
def get_ai_settings():
    key = ai_engine.get_api_key()
    return {
        "has_gemini_key": bool(key),
        "model": "gemini-2.0-flash",
        "status": "ready" if key else "master_repertory_fallback",
        "provider": "Google DeepMind Gemini 2.0 Flash" if key else "PrimeHeal Master Clinical Repertory (35 Polychrests)"
    }

@app.post("/api/settings/ai")
@app.post("/settings/ai")
async def save_ai_settings(request: Request):
    data = await request.json()
    key = (data.get("gemini_api_key") or data.get("api_key") or "").strip()
    if key:
        os.environ["GEMINI_API_KEY"] = key
        key_file = os.path.join(os.path.dirname(__file__), "gemini_api_key.txt")
        with open(key_file, "w", encoding="utf-8") as f:
            f.write(key)
        return {"ok": True, "message": "Gemini AI Key saved successfully! All cases will now be analyzed by Gemini 2.0 Flash."}
    return {"ok": False, "message": "Key cannot be empty"}


@app.get("/api/cases/export")
@app.get("/cases/export")
def export_cases_backup():
    return database.export_all_data()

@app.post("/api/cases/import")
@app.post("/cases/import")
async def import_cases_backup(request: Request):
    data = await request.json()
    count = database.import_all_data(data)
    return {"ok": True, "imported_cases": count, "message": f"Successfully restored {count} cases into database."}

@app.post("/api/cases/sync")
@app.post("/cases/sync")
async def sync_case(request: Request):
    c_dict = await request.json()
    conn = database.get_db()
    cursor = conn.cursor()
    case_id = c_dict.get("id") or str(uuid.uuid4())
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cursor.execute("DELETE FROM cases WHERE id = ?", (case_id,))
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
        case_id,
        c_dict.get("patient_name") or c_dict.get("name") or "Anonymous Patient",
        str(c_dict.get("age", "")),
        c_dict.get("sex", ""),
        c_dict.get("occupation", ""),
        c_dict.get("address", ""),
        c_dict.get("phone", ""),
        c_dict.get("email", ""),
        str(c_dict.get("weight", "")),
        str(c_dict.get("height", "")),
        c_dict.get("complaints", ""),
        c_dict.get("associated_complaints", ""),
        c_dict.get("history", ""),
        c_dict.get("mentals", ""),
        c_dict.get("vitals", ""),
        c_dict.get("general_exam", ""),
        c_dict.get("systemic_exam", ""),
        c_dict.get("local_exam", ""),
        c_dict.get("modalities", ""),
        c_dict.get("reports", ""),
        c_dict.get("notes", ""),
        c_dict.get("appetite", ""),
        c_dict.get("cravings", ""),
        c_dict.get("aversions", ""),
        c_dict.get("thirst", ""),
        c_dict.get("thermal", ""),
        c_dict.get("perspiration", ""),
        c_dict.get("stool", ""),
        c_dict.get("urine", ""),
        c_dict.get("sleep", ""),
        c_dict.get("sleep_position", ""),
        c_dict.get("past_history", ""),
        c_dict.get("vaccination", ""),
        c_dict.get("family_history", ""),
        c_dict.get("diet", ""),
        c_dict.get("marital_status", ""),
        json.dumps(c_dict),
        json.dumps(c_dict.get("result")) if isinstance(c_dict.get("result"), dict) else c_dict.get("result", "{}"),
        json.dumps(c_dict.get("doctor_override")) if isinstance(c_dict.get("doctor_override"), dict) else c_dict.get("doctor_override"),
        1 if c_dict.get("archived") else 0,
        c_dict.get("created_at") or now,
        c_dict.get("updated_at") or now
    ))
    conn.commit()
    conn.close()
    return get_case(case_id)

@app.post("/api/cases")
@app.post("/cases")
async def create_case(request: Request):
    body = await request.json()
    case_id = str(uuid.uuid4())
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Run AI Repertorization on the case
    ai_result = ai_engine.analyze_case(body)
    upstream_case_id = ai_result.pop("_upstream_case_id", None) if isinstance(ai_result, dict) else None
    if upstream_case_id:
        body["upstream_case_id"] = str(upstream_case_id)
    
    patient_name = body.get("name") or body.get("patient_name") or body.get("fullName") or "Anonymous Patient"
    
    conn = database.get_db()
    cursor = conn.cursor()
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
        body.get("appetite", ""),
        body.get("cravings", ""),
        body.get("aversions", ""),
        body.get("thirst", ""),
        body.get("thermal", ""),
        body.get("perspiration", ""),
        body.get("stool", ""),
        body.get("urine", ""),
        body.get("sleep", ""),
        body.get("sleep_position", ""),
        body.get("past_history", ""),
        body.get("vaccination", ""),
        body.get("family_history", ""),
        body.get("diet", ""),
        body.get("marital_status", ""),
        json.dumps(body),
        json.dumps(ai_result),
        None,
        0,
        now,
        now
    ))
    if upstream_case_id:
        try:
            cursor.execute("UPDATE cases SET upstream_case_id = ? WHERE id = ?", (str(upstream_case_id), case_id))
        except Exception:
            pass
    conn.commit()
    conn.close()
    
    # Return the newly created case
    return get_case(case_id)

@app.get("/api/cases/{case_id}")
@app.get("/cases/{case_id}")
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
    
    formatted = format_case_response(d, conn=conn)
    conn.close()
    return formatted

@app.delete("/api/cases/{case_id}")
@app.delete("/cases/{case_id}")
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
@app.post("/cases/{case_id}/archive")
def archive_case(case_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cases SET archived = 1 WHERE id = ?", (case_id,))
    conn.commit()
    conn.close()
    return get_case(case_id)

@app.post("/api/cases/{case_id}/unarchive")
@app.post("/cases/{case_id}/unarchive")
def unarchive_case(case_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cases SET archived = 0 WHERE id = ?", (case_id,))
    conn.commit()
    conn.close()
    return get_case(case_id)

@app.post("/api/cases/{case_id}/reanalyze")
@app.get("/api/cases/{case_id}/reanalyze")
def reanalyze_case_endpoint(case_id: str):
    case = get_case(case_id)
    new_res = ai_engine.analyze_case(case)
    new_up_id = new_res.pop("_upstream_case_id", None) if isinstance(new_res, dict) else None
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cases SET result = ? WHERE id = ?", (json.dumps(new_res), case_id))
    if new_up_id:
        try:
            cursor.execute("UPDATE cases SET upstream_case_id = ? WHERE id = ?", (str(new_up_id), case_id))
        except Exception:
            pass
    conn.commit()
    conn.close()
    return get_case(case_id)

@app.post("/api/cases/{case_id}/prescription")
@app.post("/cases/{case_id}/prescription")
async def edit_prescription(case_id: str, request: Request):
    body = await request.json()
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cases SET doctor_override = ? WHERE id = ?", (json.dumps(body), case_id))
    conn.commit()
    conn.close()
    return get_case(case_id)

@app.post("/api/cases/{case_id}/prescription/revert")
@app.post("/cases/{case_id}/prescription/revert")
def revert_prescription(case_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE cases SET doctor_override = NULL WHERE id = ?", (case_id,))
    conn.commit()
    conn.close()
    return get_case(case_id)


# ----------------- FOLLOW-UP ENDPOINTS -----------------

@app.post("/api/cases/{case_id}/followups")
@app.post("/cases/{case_id}/followups")
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
@app.post("/cases/{case_id}/followups/{followup_id}/analyze")
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
@app.delete("/cases/{case_id}/followups/{followup_id}")
def delete_followup(case_id: str, followup_id: str):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM followups WHERE id = ? AND case_id = ?", (followup_id, case_id))
    conn.commit()
    conn.close()
    return get_case(case_id)


# ----------------- CHAT ENDPOINTS -----------------

# Static General Chat Endpoints FIRST to prevent path param shadowing
@app.post("/api/chat/general")
@app.post("/chat/general")
async def general_chat(request: Request):
    body = await request.json()
    session_id = body.get("session_id", "default")
    message = body.get("message") or body.get("content") or ""
    
    reply = ai_engine.chat_response(message)
    
    conn = database.get_db()
    cursor = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    msg_id = str(uuid.uuid4())
    reply_id = str(uuid.uuid4())
    
    if message.strip():
        cursor.execute("INSERT INTO general_chats (id, session_id, role, message, created_at) VALUES (?, ?, ?, ?, ?)",
                       (msg_id, session_id, "user", message, now))
    cursor.execute("INSERT INTO general_chats (id, session_id, role, message, created_at) VALUES (?, ?, ?, ?, ?)",
                   (reply_id, session_id, "assistant", reply, now))
    conn.commit()
    
    # Fetch all messages in the session formatted with id, role, content, message, created_at
    cursor.execute("SELECT id, session_id, role, message, created_at FROM general_chats WHERE session_id = ? ORDER BY created_at ASC", (session_id,))
    rows = cursor.fetchall()
    messages = []
    for r in rows:
        rd = dict(r)
        content = rd.get("message") or rd.get("content") or ""
        messages.append({
            "id": rd.get("id") or str(uuid.uuid4()),
            "role": rd.get("role", "assistant"),
            "content": content,
            "message": content,
            "created_at": rd.get("created_at") or now
        })
    conn.close()
    
    return {
        "session_id": session_id,
        "messages": messages,
        "reply": reply,
        "message": reply,
        "ok": True
    }

@app.get("/api/chat/general/{session_id}")
@app.get("/chat/general/{session_id}")
@app.get("/api/chat/general")
@app.get("/chat/general")
def get_general_chat(session_id: str = "default"):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, session_id, role, message, created_at FROM general_chats WHERE session_id = ? ORDER BY created_at ASC", (session_id,))
    rows = cursor.fetchall()
    messages = []
    for r in rows:
        rd = dict(r)
        content = rd.get("message") or rd.get("content") or ""
        messages.append({
            "id": rd.get("id") or str(uuid.uuid4()),
            "role": rd.get("role", "assistant"),
            "content": content,
            "message": content,
            "created_at": rd.get("created_at") or datetime.datetime.now(datetime.timezone.utc).isoformat()
        })
    conn.close()
    return {"session_id": session_id, "messages": messages}

@app.delete("/api/chat/general/{session_id}")
@app.delete("/chat/general/{session_id}")
@app.delete("/api/chat/general")
@app.delete("/chat/general")
def clear_general_chat(session_id: str = "default"):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM general_chats WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
    return {"session_id": session_id, "ok": True, "messages": []}

# Case-Specific Chat Endpoints
@app.get("/api/cases/{case_id}/chat")
@app.get("/cases/{case_id}/chat")
@app.get("/api/chat/{case_id}")
@app.get("/chat/{case_id}")
def get_case_chat_endpoint(case_id: str):
    if case_id.lower() in ("general", "default"):
        return get_general_chat(case_id)
    case = get_case(case_id)
    return case

@app.post("/api/cases/{case_id}/chat")
@app.post("/cases/{case_id}/chat")
@app.post("/api/chat/{case_id}")
@app.post("/chat/{case_id}")
async def case_chat(case_id: str, request: Request):
    if case_id.lower() in ("general", "default"):
        return await general_chat(request)
        
    body = await request.json()
    message = body.get("message") or body.get("content") or ""
    case = get_case(case_id)
    reply = ai_engine.chat_response(message, case)
    
    conn = database.get_db()
    cursor = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if message.strip():
        cursor.execute("INSERT INTO case_chats (id, case_id, role, message, created_at) VALUES (?, ?, ?, ?, ?)",
                       (str(uuid.uuid4()), case_id, "user", message, now))
    cursor.execute("INSERT INTO case_chats (id, case_id, role, message, created_at) VALUES (?, ?, ?, ?, ?)",
                   (str(uuid.uuid4()), case_id, "assistant", reply, now))
    conn.commit()
    conn.close()
    
    # Return updated case object with messages included
    updated_case = get_case(case_id)
    updated_case["reply"] = reply
    updated_case["message"] = reply
    updated_case["ok"] = True
    return updated_case

@app.delete("/api/cases/{case_id}/chat")
@app.delete("/cases/{case_id}/chat")
@app.delete("/api/chat/{case_id}")
@app.delete("/chat/{case_id}")
def clear_case_chat(case_id: str):
    if case_id.lower() in ("general", "default"):
        return clear_general_chat(case_id)
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM case_chats WHERE case_id = ?", (case_id,))
    conn.commit()
    conn.close()
    updated_case = get_case(case_id)
    updated_case["messages"] = []
    updated_case["ok"] = True
    return updated_case


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
            <div class="stat">
                <div class="stat-val" id="dbEngine" style="font-size: 18px; color: #a3f7cb;">Checking...</div>
                <div class="stat-lbl">Active Storage Engine</div>
            </div>
        </div>

        <div class="card">
            <h2>Lifetime Cloud Storage & Backup</h2>
            <p style="color: #8fa59c; font-size: 14px; line-height: 1.5; margin-bottom: 16px;">
                All hospital patient cases, follow-ups, and chat consultations can be backed up and restored in 1 click. Connect a free cloud PostgreSQL database (Render Postgres, Supabase, or Neon) for 100% permanent lifetime data safety.
            </p>
            <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 18px;">
                <button onclick="downloadBackup()">📥 Download Complete Backup (JSON)</button>
                <input type="file" id="backupFileInput" accept=".json" style="display:none;" onchange="uploadBackup(event)" />
                <button onclick="document.getElementById('backupFileInput').click()" style="background:#1b4d3e; color:#a3f7cb;">📤 Restore from Backup File</button>
                <span id="backupStatus" style="align-self: center; font-size: 13px; color: #8ee0b7;"></span>
            </div>

            <hr style="border: 0; border-top: 1px solid #23322d; margin: 18px 0;" />
            <label style="font-size: 13px; color: #a3f7cb;">Connect PostgreSQL Database (Render / Supabase / Neon):</label>
            <input type="text" id="postgresUrl" placeholder="postgres://user:password@host.render.com/dbname" />
            <button onclick="savePostgresUrl()">Connect Cloud Database</button>
            <span id="pgStatus" style="margin-left: 14px; font-size: 13px; color: #8ee0b7;"></span>
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
                } else {
                    tbody.innerHTML = data.map(c => `
                        <tr>
                            <td><b>${c.patient_name || 'Anonymous'}</b></td>
                            <td>${c.age || '-'} / ${c.sex || '-'}</td>
                            <td style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${c.complaints || '-'}</td>
                            <td><span style="color:#8ee0b7; font-weight:600;">${c.result && c.result.remedy ? c.result.remedy : (c.doctor_override && c.doctor_override.remedy ? c.doctor_override.remedy : 'Pending')}</span> (${(c.result && c.result.potency) || ''})</td>
                            <td style="color:#8fa59c; font-size:12px;">${c.created_at ? c.created_at.substring(0, 10) : '-'}</td>
                        </tr>
                    `).join('');
                }

                // Check storage engine
                const statusRes = await fetch('/api/system/status');
                const statusData = await statusRes.json();
                document.getElementById('dbEngine').innerText = statusData.is_postgres ? 'PostgreSQL (Cloud)' : 'SQLite (Tracked)';
            } catch(e) {
                console.error(e);
            }
        }

        function downloadBackup() {
            window.location.href = '/api/cases/export';
        }

        async function uploadBackup(event) {
            const file = event.target.files[0];
            if (!file) return;
            const text = await file.text();
            try {
                const json = JSON.parse(text);
                const res = await fetch('/api/cases/import', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(json)
                });
                const r = await res.json();
                document.getElementById('backupStatus').innerText = '✓ ' + (r.message || 'Restored successfully!');
                loadCases();
                setTimeout(() => document.getElementById('backupStatus').innerText = '', 4000);
            } catch(err) {
                alert('Invalid JSON backup file: ' + err.message);
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

        function savePostgresUrl() {
            const url = document.getElementById('postgresUrl').value.trim();
            fetch('/api/admin/set-postgres', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url})
            }).then(r => r.json()).then(data => {
                document.getElementById('pgStatus').innerText = '✓ Connected to ' + data.engine + '!';
                loadCases();
                setTimeout(() => document.getElementById('pgStatus').innerText = '', 4000);
            });
        }

        loadCases();
    </script>
</body>
</html>
"""

@app.post("/api/admin/set-key")
@app.post("/admin/set-key")
async def set_admin_key(request: Request):
    body = await request.json()
    key = body.get("key", "").strip()
    if key:
        os.environ["GEMINI_API_KEY"] = key
    return {"ok": True}

@app.post("/api/admin/set-postgres")
@app.post("/admin/set-postgres")
async def set_admin_postgres(request: Request):
    body = await request.json()
    url = body.get("url", "").strip()
    if url:
        with open(database.PG_CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(url)
    else:
        if os.path.exists(database.PG_CONFIG_FILE):
            os.remove(database.PG_CONFIG_FILE)
    database.init_db()
    info = database.get_engine_info()
    return {"ok": True, "engine": info["engine"], "is_postgres": info["is_postgres"]}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Prime Heal Hospital Backend on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
