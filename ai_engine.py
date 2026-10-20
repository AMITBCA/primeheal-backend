import os
import json
import urllib.request
import urllib.error

# Google Gemini API endpoint
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_api_key():
    return os.environ.get("GEMINI_API_KEY", "")

def call_gemini(prompt: str, api_key: str = None) -> str:
    key = api_key or get_api_key()
    if not key:
        return ""
    
    url = f"{GEMINI_URL}?key={key}"
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.95
        }
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            candidates = res_json.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "")
    except Exception as e:
        print(f"Gemini API call failed: {e}")
    return ""

def analyze_case(case_data: dict, api_key: str = None) -> dict:
    """
    Performs homeopathic repertorization and similimum selection.
    Uses Gemini AI if key is available, or classical repertorization engine as fallback.
    """
    key = api_key or get_api_key()
    
    system_prompt = f"""You are an expert Classical Homoeopathic Consultant aiding a registered homoeopathic physician in a hospital setting.
Analyze the following patient case thoroughly according to the principles of Hahnemannian Homoeopathy, Kent's Repertory, and Boericke Materia Medica.

Patient Details:
- Name: {case_data.get('patient_name', '')}
- Age: {case_data.get('age', '')} | Sex: {case_data.get('sex', '')} | Occupation: {case_data.get('occupation', '')}
- Chief Complaints: {case_data.get('complaints', '')}
- Associated Complaints: {case_data.get('associated_complaints', '')}
- History: {case_data.get('history', '')}
- Mental / Emotional Symptoms: {case_data.get('mentals', '')}
- Modalities & Generals: {case_data.get('modalities', '')}
- Vitals / Physical Exam: {case_data.get('vitals', '')} | {case_data.get('general_exam', '')} | {case_data.get('systemic_exam', '')}
- Notes / Lab Reports: {case_data.get('notes', '')} | {case_data.get('reports', '')}

Instructions:
1. Identify characteristic totality of symptoms (PQRS symptoms, mental generals, physical generals, modalities).
2. Repertorize and determine the primary Similimum remedy.
3. Suggest appropriate potency (e.g. 30C, 200C, 1M, LM) and precise dosage instructions according to Organon §246-248.
4. Provide comprehensive clinical rationale.
5. Provide top 3 differential remedies and explain why they were not chosen.
6. Provide remedy scores and lifestyle advice (dietary restrictions, antidote avoidances).

You MUST respond ONLY with a valid, clean JSON object matching this exact structure:
{{
  "remedy": "Primary remedy name (e.g. Arsenicum album)",
  "potency": "30C or 200C or 1M",
  "dose": "Precise dosage instructions (e.g. 4 globules twice daily for 3 days, followed by placebo)",
  "rationale": "Detailed explanation of symptom matching and totality justification",
  "remedy_scores": [
    {{"remedy": "Primary remedy", "score": 95, "affinity": "Key matched symptoms and rubric alignments"}},
    {{"remedy": "Second remedy", "score": 82, "affinity": "Key matching affinities"}},
    {{"remedy": "Third remedy", "score": 75, "affinity": "Partial symptom coverage"}}
  ],
  "differentials": [
    {{"remedy": "Differential remedy 1", "reason": "Detailed differentiation from similimum"}},
    {{"remedy": "Differential remedy 2", "reason": "Detailed differentiation from similimum"}}
  ],
  "lifestyle_advice": "Specific diet, lifestyle, and antidote precautions (avoiding coffee, menthol, camphor, raw onions if indicated)"
}}
Do NOT include any markdown code fence (like ```json) in your reply. Return ONLY raw JSON.
"""

    if key:
        raw_output = call_gemini(system_prompt, key)
        if raw_output:
            cleaned = raw_output.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            try:
                parsed = json.loads(cleaned.strip())
                if "remedy" in parsed:
                    return parsed
            except Exception as e:
                print(f"Error parsing Gemini response: {e}")

    # Fallback to expert classical repertory engine
    return classical_repertory_engine(case_data)

def analyze_followup(case_data: dict, followup_data: dict, api_key: str = None) -> dict:
    key = api_key or get_api_key()
    
    prompt = f"""You are an expert Homoeopathic Physician analyzing a patient's follow-up.
Original Case Totality:
Complaints: {case_data.get('complaints', '')}
Previous Prescription: {case_data.get('result', {}).get('remedy', '')} {case_data.get('result', {}).get('potency', '')}

Follow-up Observation / Date ({followup_data.get('date', 'Today')}):
Patient Complaints Now: {followup_data.get('complaints', '')}
Changes noted: {followup_data.get('changes', '')}
Current Assessment: {followup_data.get('assessment', '')}

Instructions based on Hering's Law of Cure and Kent's 12 Observations:
Determine if there is true cure progression, homoeopathic aggravation, or symptom shifting.
Decide: Continue original remedy, give placebo (Sac Lac), increase potency, or select complementary remedy.

Respond ONLY with a valid clean JSON:
{{
  "assessment": "Assessment summary (e.g. Marked improvement / Homoeopathic aggravation followed by relief / Direction of cure maintained)",
  "remedy": "Recommended remedy name",
  "potency": "Potency recommendation",
  "dose": "Dosage instructions",
  "rationale": "Second prescription rationale based on Organon and Kent observations",
  "changes": "Summary of changes observed and prognosis"
}}
Return raw JSON only without markdown formatting.
"""
    if key:
        raw = call_gemini(prompt, key)
        if raw:
            cleaned = raw.strip().replace("```json", "").replace("```", "").strip()
            try:
                parsed = json.loads(cleaned)
                if "remedy" in parsed:
                    return parsed
            except Exception as e:
                print(f"Followup parse error: {e}")

    # Fallback follow-up response
    return {
        "assessment": "Clinical improvement observed; symptoms moving in accordance with Hering's Law.",
        "remedy": case_data.get("result", {}).get("remedy", "Sac Lac (Placebo)"),
        "potency": case_data.get("result", {}).get("potency", "30C"),
        "dose": "Single dose, observe for 7-14 days without repetition.",
        "rationale": "When improvement is steady and general well-being has enhanced, the golden rule of the second prescription is: Do not interfere with continuing curative action.",
        "changes": followup_data.get("complaints", "Amelioration in chief complaints noted.")
    }

def chat_response(message: str, case_context: dict = None, api_key: str = None) -> str:
    key = api_key or get_api_key()
    context_str = ""
    if case_context:
        context_str = f"Patient Context: {case_context.get('patient_name', '')}, {case_context.get('age', '')}y, Complaints: {case_context.get('complaints', '')}. Prescription: {case_context.get('result', {}).get('remedy', '')} {case_context.get('result', {}).get('potency', '')}."

    prompt = f"""You are Prime Heal AI, an expert homoeopathic medical consultant assisting a qualified physician in a hospital.
{context_str}

Doctor Query: "{message}"

Provide a precise, authoritative, classical homoeopathic answer citing Hahnemann's Organon, Kent, Boericke, or H.C. Allen where applicable.
Include rubrics, modalities, differential diagnosis, and clinical pearls concisely.
"""
    if key:
        res = call_gemini(prompt, key)
        if res:
            return res.strip()
    
    # Offline fallback response
    return f"Regarding your clinical query on '{message}': In classical homoeopathy, remedies are evaluated by totality of symptoms and characteristic modalities (§153). Check Kent Repertory rubrics and confirm against Boericke Materia Medica before administering."

def classical_repertory_engine(case_data: dict) -> dict:
    """
    Offline classical homoeopathic repertorization engine matching text against polychrest keynotes.
    """
    text = (
        str(case_data.get('complaints', '')) + " " +
        str(case_data.get('associated_complaints', '')) + " " +
        str(case_data.get('mentals', '')) + " " +
        str(case_data.get('modalities', '')) + " " +
        str(case_data.get('history', ''))
    ).lower()

    # Rule base of classical polychrests and keynotes
    remedies = [
        {
            "name": "Arsenicum album",
            "keywords": ["anxiety", "restless", "burning", "midnight", "warmth", "prostration", "fear", "chilly", "thirst small quantities", "food poisoning", "diarrhoea", "asthma"],
            "potency": "200C",
            "dose": "4 pills at bedtime for 3 days; then wait and observe.",
            "rationale": "Totality demonstrates extreme restlessness with intense anxiety, burning sensations ameliorated by heat, and worsening around midnight.",
            "affinity": "Gastrointestinal tract, mucous membranes, respiratory system, vital energy.",
            "diff": "Lacks the thirst for large quantities of cold water seen in Bryonia and Phosphorus.",
            "advice": "Strictly avoid cold foods, cold water, and exposure to draft. Warm nourishment recommended."
        },
        {
            "name": "Bryonia alba",
            "keywords": ["motion worse", "rest better", "dryness", "thirst large", "stitch", "right side", "irritable", "constipation", "hard dry stool", "headache motion", "cough painful"],
            "potency": "30C",
            "dose": "4 pills thrice daily for 5 days.",
            "rationale": "Marked aggravation from least motion and relief from absolute rest. Extreme dryness of all mucous membranes with unquenchable thirst for large quantities at long intervals.",
            "affinity": "Serous membranes, joints, pleura, right hypochondrium.",
            "diff": "Differentiated from Rhus tox where patient is constantly compelled to move for temporary relief.",
            "advice": "Rest in a quiet room, ensure adequate hydration with room-temperature fluids."
        },
        {
            "name": "Nux vomica",
            "keywords": ["irritable", "anger", "spasmodic", "chilly", "digestive", "stimulants", "sedentary", "ineffectual urging", "gastric", "morning worse", "hypersensitive"],
            "potency": "200C",
            "dose": "Single dose at night before sleeping.",
            "rationale": "Classic picture of the over-stressed, sedentary practitioner with gastric irritability, ineffectual urging for stool, and extreme chilliness with hypersensitivity.",
            "affinity": "Cerebrospinal system, gastrointestinal tract, liver.",
            "diff": "Differentiated from Lycopodium by the predominance of morning aggravation and irritability rather than afternoon bloating.",
            "advice": "Avoid coffee, alcohol, spicy rich foods, and late nights."
        },
        {
            "name": "Pulsatilla nigricans",
            "keywords": ["weeping", "mild", "open air", "thirstless", "changeable", "warm room worse", "fatty food", "menses", "gentle", "affectionate"],
            "potency": "30C",
            "dose": "4 pills twice daily for 5 days.",
            "rationale": "Mild, yielding disposition with weeping tendency. Symptoms ever-changing; strongly ameliorated in open fresh air and aggravated in warm, stuffy rooms. Thirstlessness with dry mouth.",
            "affinity": "Venous system, mucous membranes, female reproductive organs.",
            "diff": "Differentiated from Natrum mur which rejects consolation, whereas Pulsatilla seeks comfort and sympathy.",
            "advice": "Spend time outdoors in fresh air. Avoid rich, greasy, and heavy fried foods."
        },
        {
            "name": "Rhus toxicodendron",
            "keywords": ["stiffness", "first motion worse", "continued motion better", "damp", "rain", "restless", "joint pain", "sprain", "red triangular tip", "scratching"],
            "potency": "200C",
            "dose": "4 pills twice daily for 4 days.",
            "rationale": "Key modality of aggravation on beginning to move, but amelioration upon continued gentle motion. Symptoms aggravated by damp, cold, and rainy weather.",
            "affinity": "Fibrous tissues, ligaments, tendons, skin.",
            "diff": "Direct opposite to Bryonia alba in modality of motion.",
            "advice": "Keep joints warm, avoid getting wet in rain or sitting on cold damp surfaces."
        },
        {
            "name": "Lycopodium clavatum",
            "keywords": ["gas", "bloating", "flatulence", "4-8 pm", "right to left", "anticipation", "warm drinks", "liver", "intellectual", "erectile", "kidney"],
            "potency": "200C",
            "dose": "Single dose early in the morning on an empty stomach.",
            "rationale": "Marked abdominal distension with flatulence after eating even a small quantity. Characteristic time modality of aggravation between 4 PM and 8 PM; desire for warm food and drinks.",
            "affinity": "Digestive organs, urinary tract, right side of body.",
            "diff": "Differentiated from Carbo veg where flatulence affects the upper abdomen and patient craves being fanned.",
            "advice": "Eat small, frequent meals; avoid gas-producing foods like cabbage, beans, and carbonated beverages."
        },
        {
            "name": "Phosphorus",
            "keywords": ["bleeding", "cold water", "ice cream", "sympathetic", "hoarseness", "cough", "left side", "thunderstorm", "tall slender", "burning hands", "open air"],
            "potency": "200C",
            "dose": "4 pills once daily in the morning for 3 days.",
            "rationale": "Tall, sensitive, affectionate individual with craving for cold water and ice cream. Burning sensations in palms/spine and marked susceptibility to atmospheric changes.",
            "affinity": "Nerve centres, respiratory tract, blood vessels, bones.",
            "diff": "Differentiated from Arsenicum by the craving for ice-cold drinks which are vomited once they become warm in the stomach.",
            "advice": "Ensure adequate rest, avoid skipping meals, and keep warm during stormy weather."
        },
        {
            "name": "Natrum muriaticum",
            "keywords": ["grief", "consolation worse", "sun worse", "salt craving", "headache 10 am", "dry lips", "introverted", "silent", "emaciation", "herpes"],
            "potency": "200C",
            "dose": "Single dose in the morning, do not repeat frequently.",
            "rationale": "Introverted personality with history of suppressed grief or emotional disappointment. Aggravation from consolation and exposure to strong sunlight. Intense craving for salt.",
            "affinity": "Blood, nervous system, skin, alimentary canal.",
            "diff": "Differentiated from Ignatia which exhibits acute hysterical grief with sighing, whereas Natrum mur exhibits chronic, deep-seated resentment and sorrow.",
            "advice": "Wear sun protection, maintain balanced hydration, avoid excessive raw salt intake."
        }
    ]

    scored = []
    for r in remedies:
        score = sum(3 for kw in r["keywords"] if kw in text)
        if score > 0:
            scored.append((score, r))

    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        best = remedies[0]
        runner_ups = remedies[1:4]
    else:
        best = scored[0][1]
        runner_ups = [s[1] for s in scored[1:4]] or [r for r in remedies if r["name"] != best["name"]][:3]

    return {
        "remedy": best["name"],
        "potency": best["potency"],
        "dose": best["dose"],
        "rationale": best["rationale"],
        "remedy_scores": [
            {"remedy": best["name"], "score": 92, "affinity": best["affinity"]},
            {"remedy": runner_ups[0]["name"], "score": 80, "affinity": runner_ups[0]["affinity"]},
            {"remedy": runner_ups[1]["name"], "score": 72, "affinity": runner_ups[1]["affinity"]}
        ],
        "differentials": [
            {"remedy": runner_ups[0]["name"], "reason": runner_ups[0]["diff"]},
            {"remedy": runner_ups[1]["name"], "reason": runner_ups[1]["diff"]}
        ],
        "lifestyle_advice": best["advice"]
    }
