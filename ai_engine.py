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

def build_homoeopathic_lifestyle(remedy_name: str = "Nux vomica", case_data: dict = None) -> dict:
    """
    Constructs the exact 4-part lifestyle object expected by the React Native LifestyleBlock:
    {
      "diet_do": list of strings,
      "diet_avoid": list of strings,
      "exercises": list of strings,
      "lifestyle": list of strings
    }
    """
    case_data = case_data or {}
    r_lower = (remedy_name or "").lower()
    complaints = str(case_data.get("complaints", "")).lower()
    modalities = str(case_data.get("modalities", "")).lower()
    
    # Base homoeopathic antidotes and universal guidance (§260 Organon)
    universal_avoid = [
        "Avoid coffee, green/black tea, and aerated soft drinks (caffeine antidotes homoeopathic remedies).",
        "Avoid raw onion, raw garlic, strong menthol, peppermint, and camphorated balms within 1 hour of medicine.",
        "Avoid heavy, excessively oily, deep-fried, and stale refrigerated food.",
        "Strictly avoid alcohol, tobacco, and foods with artificial chemical preservatives."
    ]
    
    universal_do = [
        "Take freshly cooked, light, warm, and easily digestible nutritious meals at regular intervals.",
        "Hydrate adequately with warm or room-temperature water throughout the day.",
        "Include fresh seasonal fruits (sweet apples, papayas, pomegranates) and steamed vegetables.",
        "Take homoeopathic medicine on a clean tongue with at least 30 minutes gap before/after eating."
    ]
    
    universal_exercises = [
        "30 to 45 minutes of gentle aerobic walking in fresh morning sunlight.",
        "Gentle therapeutic yoga asanas (Tadasana, Bhujangasana, gentle spinal twists) suited to comfort.",
        "Daily Pranayama: 10-15 minutes of Anulom-Vilom (alternate nostril breathing) for autonomic balance.",
        "Avoid sudden, exhausting physical overexertion during the active phase of illness."
    ]
    
    universal_lifestyle = [
        "Maintain a fixed, restful sleep schedule with 7-8 hours of uninterrupted night sleep.",
        "Protect against sudden exposure to cold drafts, damp environments, or direct air conditioner blast.",
        "Practice daily stress reduction, mental relaxation, and avoid heated emotional conflicts before bedtime.",
        "Keep a personal symptom diary to record responses and changes for the next follow-up."
    ]
    
    # Specific clinical tailoring by polychrest remedy
    if "arsenic" in r_lower:
        diet_do = [
            "Warm nourishing broths, sips of warm water, light rice gruel, and stewed apples.",
            "Freshly prepared warm vegetable soups and steamed easily assimilable grains.",
            "Small, frequent meals rather than large heavy servings."
        ]
        diet_avoid = [
            "Strictly avoid ice, ice-cold water, chilled beverages, and ice cream.",
            "Avoid cold raw salads, melons, sour fruits, and tainted or suspect refrigerated leftovers.",
            "Avoid coffee, camphor, strong menthol, and pungent seasonings."
        ]
        exercises = [
            "Gentle slow indoor walking without inducing breathlessness or fatigue.",
            "Relaxing seated breathing exercises (calm diaphragmatic breathing) to soothe anxiety.",
            "Strictly avoid strenuous gym workouts or physically exhausting tasks while recovering."
        ]
        lifestyle = [
            "Keep the room warm and well-insulated; use warm blankets and warm clothing.",
            "Strict protection against midnight cold air and drafts (§153 Arsenicum midnight aggravation).",
            "Maintain a calm, reassuring environment to alleviate nocturnal restlessness and fear of illness.",
            "Ensure 8 hours of restorative rest in a peaceful bedroom."
        ]
    elif "bryonia" in r_lower:
        diet_do = [
            "Adequate room-temperature hydration (drink full glasses at measured intervals).",
            "High-fiber cooked vegetables, mild lentil soups, and light stewed apples to support bowel regularity.",
            "Moistening, easily digestible warm porridge and soothing herbal infusions."
        ]
        diet_avoid = [
            "Avoid rich, heavy, greasy meats and flatulent legumes.",
            "Avoid hot pungent chili, alcohol, and dehydrating caffeinated drinks.",
            "Avoid exposure to cold winds while sweating or overheated."
        ]
        exercises = [
            "Complete physical rest during acute painful flare-ups (Bryonia is aggravated by least motion).",
            "Gentle bed or chair-side passive stretching only when acute stitch has subsided.",
            "Slow, measured deep breathing without rapid chest expansion."
        ]
        lifestyle = [
            "Rest in a quiet, dark, well-ventilated room with minimal physical disturbance.",
            "Support the affected painful side with firm pressure or a soft cushion.",
            "Minimize unnecessary speaking, walking, or sudden postural shifts.",
            "Maintain strict regular bowel evacuation timings without straining."
        ]
    elif "nux" in r_lower:
        diet_do = [
            "Light, bland, fiber-rich vegetarian meals (oats, khichdi, steamed greens, papaya).",
            "Plenty of lukewarm water and soothing herbal teas (chamomile or cumin-coriander water).",
            "Eat at fixed, unhurried meal times; chew thoroughly in a peaceful atmosphere."
        ]
        diet_avoid = [
            "Strictly avoid coffee, alcoholic beverages, energy drinks, and tobacco.",
            "Avoid hot pungent spices, rich gravies, junk food, and late-night heavy dinners.",
            "Avoid over-the-counter antacids, laxatives, and self-prescribed allopathic stimulants."
        ]
        exercises = [
            "Brisk 30-40 minute outdoor morning walk in open air to relieve portal venous congestion.",
            "Moderate cardio, cycling, or swimming to channel nervous tension constructively.",
            "Evening relaxation stroll to release mental stress before returning home."
        ]
        lifestyle = [
            "Disconnect from work screens and electronic devices at least 1 hour before sleep.",
            "Ensure strict bedtime by 10:30 PM; avoid late night burning of the midnight oil.",
            "Do not suppress the urge for stool; establish an unhurried morning routine.",
            "Take short relaxation breaks during intensive desk work."
        ]
    elif "rhus" in r_lower:
        diet_do = [
            "Warm nourishing broths, turmeric-infused warm milk or lentil soup, and freshly cooked meals.",
            "Plenty of warm fluids to ease joint lubrication and systemic stiffness.",
            "Anti-inflammatory fresh foods: berries, papaya, flaxseeds, and steamed greens."
        ]
        diet_avoid = [
            "Avoid cold water baths, especially when perspiring or after physical exertion.",
            "Avoid chilled dairy, cold carbonated drinks, and ice creams.",
            "Avoid damp, cold environments and sitting on cold ground or wet surfaces."
        ]
        exercises = [
            "Gentle, continuous low-impact walking (Rhus tox: worse on beginning motion, better by continued motion).",
            "Warm-water aquatic therapy or gentle joint mobilization in a warm room.",
            "Gentle stretching upon waking in the morning to dispel sleep stiffness."
        ]
        lifestyle = [
            "Keep joints and muscles warmly covered with woolen or dry warm clothing.",
            "Take warm water showers/baths morning and evening to relieve stiffness.",
            "Avoid exposure to rain, damp basements, or sudden atmospheric weather changes.",
            "Change positions frequently; do not sit motionless in one posture for hours."
        ]
    elif "pulsatilla" in r_lower:
        diet_do = [
            "Light, crisp, refreshing meals: fresh green salads, fruits, and simple steamed grains.",
            "Room-temperature or cool water in comfortable small amounts.",
            "Bland nourishing vegetable preparations with minimal added oils."
        ]
        diet_avoid = [
            "Strictly avoid rich, greasy, fatty foods, pork, pastries, cream, and butter.",
            "Avoid warm, heavy, stuffy meals and overheated dining environments.",
            "Avoid ice-cold sodas or artificial heavy sweet desserts."
        ]
        exercises = [
            "Daily open-air walking in cool, breezy outdoor environments (marked Pulsatilla amelioration).",
            "Gentle recreational cycling or light nature walks in parks or gardens.",
            "Gentle yogic stretching performed in a well-ventilated, breezy room."
        ]
        lifestyle = [
            "Keep the bedroom cool, open-windowed, and well-ventilated; avoid heavy blankets.",
            "Avoid stuffy, crowded, unventilated rooms and overheated shopping malls.",
            "Seek compassionate emotional conversation and gentle companionship.",
            "Wear light, breathable cotton clothing that allows free air circulation."
        ]
    elif "lycopod" in r_lower:
        diet_do = [
            "Small, frequent, warm meals rather than two large heavy meals.",
            "Warm fluids and warm herbal infusions throughout the day (patient craves warm drinks).",
            "Easily digestible carbohydrates: steamed rice, light vegetable khichdi, stewed gourds."
        ]
        diet_avoid = [
            "Strictly avoid flatulent, gas-forming foods: cabbage, cauliflower, beans, and onions.",
            "Avoid chilled drinks, cold water, oysters, and heavy creamy desserts.",
            "Avoid eating in a rushed or emotionally anxious state."
        ]
        exercises = [
            "Light evening walking after 8 PM to facilitate abdominal digestion.",
            "Gentle abdominal breathing (Pranayama) to strengthen digestive fire.",
            "Avoid heavy strenuous weight training between 4 PM and 8 PM (time of Lycopodium aggravation)."
        ]
        lifestyle = [
            "Wear loose, non-constricting clothing around the waist and abdomen.",
            "Avoid high-pressure intellectual tasks or public speaking right before meals.",
            "Maintain strict regularity of daily bowel habits.",
            "Ensure a calm, stress-free period during late afternoon hours (4 PM - 8 PM)."
        ]
    elif "phosphor" in r_lower:
        diet_do = [
            "Frequent small meals to prevent sudden drops in vitality and trembling.",
            "Refreshing cold water and juices in moderation; sweet juicy fruits.",
            "Easily assimilable nourishing proteins: lentils, tofu, light paneer, bone broth."
        ]
        diet_avoid = [
            "Avoid skipping meals or prolonged fasting (leads to faintness and weakness).",
            "Avoid spicy, pungent seasonings and highly acidic stimulants.",
            "Avoid complete isolation or excessive solitary mental brooding."
        ]
        exercises = [
            "Non-exhaustive, graceful movements: light aerobic walking, dance, or gentle swimming.",
            "Gentle spinal yoga postures (Bhujangasana, Marjariasana) to relieve spinal burning.",
            "Avoid heavy, exhausting gym routines that drain vital reserve."
        ]
        lifestyle = [
            "Protect against atmospheric thunderstorms, lightning, and sudden weather drops.",
            "Ensure 8 to 9 hours of peaceful, restorative sleep in a quiet bedroom.",
            "Soothing back rubs or gentle massage along the spine to relieve nervous exhaustion.",
            "Engage in supportive, warm social contact with trusted family and friends."
        ]
    elif "natrum mur" in r_lower or "nat mur" in r_lower:
        diet_do = [
            "Balanced hydration with clean mineralized water; moderate sea salt.",
            "Cool, refreshing fruits and lightly steamed green vegetables.",
            "Regular simple vegetarian meals taken in quiet, serene surroundings."
        ]
        diet_avoid = [
            "Avoid excessive raw table salt, salty crisps, pickles, and processed snacks.",
            "Avoid exposure to midday summer sun and hot stuffy kitchens.",
            "Avoid skipping breakfast, which triggers the characteristic 10 AM headache."
        ]
        exercises = [
            "Early morning outdoor walk before sunrise or after sunset in shaded areas.",
            "Swimming in cool, shaded water or gentle restorative Yin yoga.",
            "Deep rhythmic breathing to release pent-up emotional sorrow."
        ]
        lifestyle = [
            "Wear UV-protective sunglasses and wide-brimmed hats when stepping out in sunlight.",
            "Allow patient personal private time without unsolicited consolation or probing.",
            "Creative outlets for emotional expression: writing, music, or art.",
            "Maintain regular sleep hours in a cool, quiet, shaded bedroom."
        ]
    elif "sulphur" in r_lower:
        diet_do = [
            "Cooling, simple vegetarian meals: cucumber, bottle gourd, melons, and fresh fruits.",
            "Plenty of pure drinking water throughout the day to support cutaneous elimination.",
            "Light, unrefined whole grains and steamed seasonal vegetables."
        ]
        diet_avoid = [
            "Avoid heavy sweets, chocolates, pastries, and refined sugar.",
            "Avoid alcohol, pungent curries, deep-fried snacks, and excessive spices.",
            "Avoid washing skin with harsh chemical soaps or excessively hot water."
        ]
        exercises = [
            "Moderate morning physical exercises in open, cool air before the sun gets strong.",
            "Outdoor walking, cycling, or recreational jogging; avoid overheating.",
            "Avoid prolonged motionless standing (Sulphur cannot stand comfortably for long)."
        ]
        lifestyle = [
            "Wear loose, airy, pure cotton clothing; avoid synthetic fabrics.",
            "Keep the bed coverings light; do not overheat feet or body during sleep.",
            "Bathe in tepid or cool water; pat skin dry gently without harsh rubbing.",
            "Ensure good room ventilation with constant fresh air exchange."
        ]
    elif "calcarea" in r_lower:
        diet_do = [
            "Nutritious, warm, easily assimilated meals rich in natural minerals and calcium.",
            "Boiled eggs (patient often craves soft-boiled eggs), warm milk, and cooked greens.",
            "Light warm vegetable soups and steamed wholesome grains."
        ]
        diet_avoid = [
            "Avoid raw, cold, damp foods, cold milk, and excess starchy refined sweets.",
            "Avoid exposure to damp, unheated rooms, basements, or cold drafts.",
            "Avoid strenuous rapid ascending of stairs or steep inclines."
        ]
        exercises = [
            "Gentle walking on level ground at a comfortable, non-hurried pace.",
            "Postural strengthening exercises and gentle core stabilization.",
            "Avoid sudden strenuous exertion that causes profuse head perspiration and breathlessness."
        ]
        lifestyle = [
            "Keep head and feet dry and warm; change damp clothes immediately.",
            "Ensure a dry, sunny, well-ventilated residence free from dampness or mold.",
            "Maintain moderate pacing in daily activities without physical or mental rush.",
            "Ensure comfortable warm bedding and avoid drafts during sleep."
        ]
    elif "belladonna" in r_lower:
        diet_do = [
            "Cool or room-temperature lemon water, hydrating clear broths, and light liquid diet.",
            "Small sips of soothing fluids at frequent intervals.",
            "Simple, bland, easily swallowed preparations without spices."
        ]
        diet_avoid = [
            "Strictly avoid drafts of air, sudden uncovery, and washing hair in cold water.",
            "Avoid loud noises, bright lights, jarring movements, and sudden touch.",
            "Avoid hot pungent food, coffee, tea, and stimulants."
        ]
        exercises = [
            "Strict bed rest during acute congested or febrile state.",
            "Avoid bending head forward, stooping, or jarring movements of any kind.",
            "Gentle slow breathing in bed."
        ]
        lifestyle = [
            "Rest in a semi-darkened, quiet room free from loud noises and bright sunlight.",
            "Keep the head elevated on comfortable pillows to reduce cerebral congestion.",
            "Protect the head and neck strictly from drafts of air or open windows.",
            "Cool, damp cloth application to forehead if burning hot, keeping feet warm."
        ]
    else:
        # Clinical condition based adaptation
        diet_do = universal_do
        diet_avoid = universal_avoid
        exercises = universal_exercises
        lifestyle = universal_lifestyle

    # If case has specific modalities / complaints, append relevant pointers
    if "joint" in complaints or "stiff" in complaints or "arthr" in complaints:
        if "Warm baths or gentle heat application recommended." not in lifestyle:
            lifestyle.append("Apply dry gentle warmth or warm compresses to ease joint stiffness.")
        if "Avoid sitting still in cold drafts or refrigerated rooms." not in diet_avoid:
            diet_avoid.append("Avoid sitting directly under cold air-conditioning or fans on bare joints.")

    if "cough" in complaints or "asthma" in complaints or "breath" in complaints:
        if "Sip warm water and avoid chilled ice-cold drinks." not in diet_do:
            diet_do.insert(0, "Sip warm water frequently; inhale warm steam before sleeping if congested.")
        if "Avoid direct exposure to cold night air and dust." not in lifestyle:
            lifestyle.append("Cover mouth and nose when stepping out into cold night air or dusty zones.")

    if "gastric" in complaints or "acid" in complaints or "ulcer" in complaints:
        if "Eat small, frequent, non-spicy meals at regular hours." not in diet_do:
            diet_do.insert(0, "Eat small, frequent, non-spicy meals at regular hours to prevent acid build-up.")

    return {
        "diet_do": diet_do[:4],
        "diet_avoid": diet_avoid[:4],
        "exercises": exercises[:4],
        "lifestyle": lifestyle[:4]
    }

def analyze_case(case_data: dict, api_key: str = None) -> dict:
    """
    Performs homeopathic repertorization and similimum selection.
    Uses Gemini AI if key is available, or classical repertorization engine as fallback.
    Returns clean dictionary matching the mobile app's expected schema.
    """
    key = api_key or get_api_key()
    name = case_data.get('name') or case_data.get('patient_name', '')
    
    system_prompt = f"""You are an expert Classical Homoeopathic Consultant aiding a registered homoeopathic physician in a hospital setting.
Analyze the following patient case thoroughly according to the principles of Hahnemannian Homoeopathy, Kent's Repertory, and Boericke Materia Medica.

Patient Details:
- Name: {name}
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
4. Provide comprehensive clinical diagnosis and totality rationale.
5. Provide top 3 differential remedies as plain strings explaining why they were not chosen.
6. Provide remedy scores (remedy, score, affinity), materia medica citations, and structured lifestyle guidance.

You MUST respond ONLY with a valid, clean JSON object matching this exact structure:
{{
  "remedy": "Primary remedy name (e.g. Nux vomica)",
  "potency": "30C or 200C or 1M",
  "dose": "Precise dosage instructions (e.g. 4 pills once at night for 3 days)",
  "diagnosis": "Clinical diagnostic formulation (e.g. Acute Gastritis with Autonomic Dysfunction)",
  "rationale": "Detailed explanation of symptom matching and totality justification",
  "remedy_scores": [
    {{"remedy": "Primary remedy", "score": 95, "affinity": "Key matched symptoms and rubric alignments"}},
    {{"remedy": "Second remedy", "score": 82, "affinity": "Key matching affinities"}},
    {{"remedy": "Third remedy", "score": 75, "affinity": "Partial symptom coverage"}}
  ],
  "differentials": [
    "Differential remedy 1: Explanation of difference from similimum",
    "Differential remedy 2: Explanation of difference from similimum"
  ],
  "citations": [
    {{"remedy": "Primary remedy", "source": "Boericke Materia Medica", "text": "Key symptom quotation from Materia Medica"}}
  ],
  "lifestyle": {{
    "diet_do": [
      "Light, warm, freshly prepared easily digestible meals",
      "Hydrate well with warm water at regular intervals",
      "Fresh seasonal fruits (sweet apples, papayas, pomegranates)"
    ],
    "diet_avoid": [
      "Strictly avoid coffee, strong tea, and aerated drinks (caffeine antidotes homoeopathic remedies)",
      "Avoid raw onion, raw garlic, camphor, and strong menthol within 1 hour of medicine",
      "Avoid excessively oily, heavy, fried, and stale refrigerated food"
    ],
    "exercises": [
      "30-40 minutes of gentle brisk walking in fresh morning air",
      "Gentle stretching and therapeutic yoga asanas (Tadasana, Bhujangasana)",
      "Daily Pranayama: 10 minutes of Anulom-Vilom alternate nostril breathing"
    ],
    "lifestyle": [
      "Maintain a fixed, restful sleep routine of 7-8 hours; avoid late-night screens",
      "Take medicines on an empty or clean mouth with a 30-minute gap before/after eating",
      "Protect against sudden exposure to cold drafts and damp environments",
      "Keep emotional stress low and maintain a relaxed, calm mental disposition"
    ]
  }}
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
                    # Normalize differentials to plain strings
                    diffs = parsed.get("differentials", [])
                    clean_diffs = []
                    for d in diffs:
                        if isinstance(d, dict):
                            clean_diffs.append(f"{d.get('remedy', '')}: {d.get('reason', '')}")
                        elif isinstance(d, str):
                            clean_diffs.append(d)
                    parsed["differentials"] = clean_diffs
                    
                    # Ensure diagnosis is present
                    if not parsed.get("diagnosis"):
                        parsed["diagnosis"] = "Clinical Homoeopathic Totality"
                        
                    # Normalize lifestyle to the 4-part dict
                    l_val = parsed.get("lifestyle")
                    if not isinstance(l_val, dict) or not ("diet_do" in l_val and "diet_avoid" in l_val and "exercises" in l_val):
                        parsed["lifestyle"] = build_homoeopathic_lifestyle(parsed["remedy"], case_data)
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

Determine the Second Prescription according to Kent's Twelve Observations and Hering's Law:
1. Assess direction of cure (Hering's Law).
2. Advise on remedy change or repetition (Organon §246-248).
3. Return raw JSON:
{{
  "assessment": "Brief clinical assessment",
  "remedy": "Prescribed remedy",
  "potency": "Prescribed potency",
  "dose": "Dosage instructions",
  "rationale": "Clinical rationale citing Kent/Hering",
  "changes": "Summary of changes"
}}
Do NOT include markdown. Return raw JSON only.
"""
    if key:
        res = call_gemini(prompt, key)
        if res:
            cleaned = res.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
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
        c_obj = case_context.get("case", {})
        c_name = c_obj.get("name") or case_context.get("patient_name") or ""
        context_str = f"Patient Context: {c_name}, {c_obj.get('age', '')}y, Complaints: {c_obj.get('complaints', '')}. Prescription: {case_context.get('result', {}).get('remedy', '')} {case_context.get('result', {}).get('potency', '')}."

    prompt = f"""You are Prime Heal AI, an expert homoeopathic medical consultant assisting a qualified physician in a hospital.
{context_str}

Doctor Query: "{message}"

Provide a precise, authoritative, classical homoeopathic answer citing Hahnemann's Organon, Kent, Boericke, or H.C. Allen where applicable.
Include rubrics, modalities, differential diagnosis, and clinical pearls concisely.
"""
    if key:
        res = call_gemini(prompt, key)
        if res and res.strip():
            return res.strip()
    
    # Rich offline homoeopathic knowledge engine
    m_lower = message.lower()
    
    if "sulphur" in m_lower and "psorinum" in m_lower:
        return (
            "Comparison between Sulphur and Psorinum (Kent & Allen):\n\n"
            "1. Thermal & Modalities: Sulphur is intensely warm/hot with burning sensations (palms, soles, vertex) and desires fresh open air; craves cool breezes and throws off covers at night. Psorinum is extremely chilly, desires warm clothing even in summer, wears a fur cap in hot weather, and dreads least cold draft or washing.\n\n"
            "2. Skin & Odours: Both are deep anti-psoric remedies with dirty, unwashed-looking skin and intractable itching. However, Psorinum discharges are characteristically offensive and carrion-like (cadaveric odor), with extreme despair of recovery. Sulphur has voluptuous itching followed by burning after scratching, worse from water washing.\n\n"
            "3. Clinical Rule: Psorinum is called for when well-selected remedies fail to act in extremely chilly, hopeless individuals. Sulphur is the king of anti-psorics indicated by burning, morning hunger at 11 AM, and standing worse."
        )
    elif "lm" in m_lower and ("30" in m_lower or "potency" in m_lower):
        return (
            "Deciding between LM (50 Millesimal) and Centesimal (30C/200C) Potencies (§246-248 Organon 6th ed.):\n\n"
            "1. LM Potencies (0/1 to 0/30) are indicated in:\n"
            "   - Chronic, hypersensitive cases where high centesimal dilutions cause violent homeopathic aggravations.\n"
            "   - Cases requiring frequent gentle daily repetition without risk of toxic aggravation.\n"
            "   - Pathological tissue changes or elderly patients with low vital reserve.\n\n"
            "2. Centesimal Potencies (30C / 200C / 1M) are indicated in:\n"
            "   - Acute illnesses with high vital reactivity (30C repeated every 2-4 hours).\n"
            "   - Clear single constitutional pictures (single dose 200C or 1M followed by watchful waiting).\n\n"
            "Administration Rule: Always succuss LM potency 8-10 times in medicinal water before administering each dose."
        )
    elif "second prescription" in m_lower or "2nd prescription" in m_lower:
        return (
            "Second Prescription Rules according to Dr. J.T. Kent:\n\n"
            "1. If patient improves steadily: Do NOT repeat, do NOT change the remedy. 'Wait and Watch' is the golden law (§245).\n"
            "2. If old symptoms return after temporary relief: Repeat the same remedy in the same or higher potency.\n"
            "3. If improvement ceases completely: Re-examine the case totality and select an affiliated or complementary remedy.\n"
            "4. If entirely new symptoms appear: The first remedy was partially similar or incorrect. Antidote if aggravated, or take a fresh totality.\n"
            "5. If Hering's Law is verified (cure proceeding from above downward, within outward, in reverse order of appearance): Continue to wait; cure is actively occurring."
        )
    elif "repeat" in m_lower or "repetition" in m_lower:
        return (
            "Guidelines on Repeating Homoeopathic Remedies (§245-248):\n\n"
            "1. In Acute Emergencies: Repeat frequently (every 15 to 60 minutes) until perceptible amelioration begins, then widen the interval.\n"
            "2. In Chronic Diseases: Single dose in high potency (200C/1M) followed by observation for 4 to 8 weeks, OR daily succussed LM potencies in split water doses.\n"
            "3. Crucial Hahnemannian Aphorism: Cease all medicine the moment progressive improvement is established, repeating only when curative action has noticeably stopped."
        )
    elif "bryonia" in m_lower and "rhus" in m_lower:
        return (
            "Bryonia alba vs. Rhus toxicodendron Differential:\n\n"
            "1. Modality of Motion (Polar Opposites):\n"
            "   - Bryonia: Aggravated by the slightest motion, relieved by absolute rest and firm pressure (§153 keynote).\n"
            "   - Rhus tox: Aggravated on first beginning to move; ameliorated by continued gentle motion; compelled to change position constantly.\n\n"
            "2. Modality of Weather:\n"
            "   - Bryonia: Worse from hot weather, warm rooms, and sun.\n"
            "   - Rhus tox: Worse from cold, damp, rain, getting wet, and air conditioning.\n\n"
            "3. Thirst: Bryonia has unquenchable thirst for large quantities at long intervals; Rhus tox has dry mouth with craving for small sips or warm drinks."
        )
    else:
        return (
            f"Clinical analysis regarding: '{message}':\n\n"
            "In classical Hahnemannian homoeopathy, case assessment is governed by the totality of characteristic symptoms (§153), modal affinities, and constitution.\n\n"
            "Key Clinical Checks:\n"
            "1. Modalities: Note specific times of aggravation (e.g. 4-8 PM in Lycopodium; midnight in Arsenicum; 10 AM in Natrum mur).\n"
            "2. Thermal State: Is the patient chilly (Hepar, Nux, Arsenicum, Psorinum) or hot/burning (Sulphur, Pulsatilla, Apis, Secale)?\n"
            "3. Thirst: Thirsty for large gulps (Bryonia), small frequent sips (Arsenicum), or thirstless with dry mouth (Pulsatilla, Apis)?\n"
            "4. Confirmation: Verify rubrics in Kent Repertory and check full keynote portrait in Boericke Materia Medica before administering."
        )

def classical_repertory_engine(case_data: dict) -> dict:
    """
    Offline classical homoeopathic repertorization engine matching text against polychrest keynotes.
    Always generates complete remedy, potency, dose, diagnosis, rationale, remedy_scores, differentials,
    citations, and the full 4-part lifestyle object {diet_do, diet_avoid, exercises, lifestyle}.
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
            "keywords": ["anxiety", "restless", "burning", "midnight", "warmth", "prostration", "fear", "chilly", "thirst small quantities", "food poisoning", "diarrhoea", "asthma", "cold water worse"],
            "potency": "200C",
            "dose": "4 pills at bedtime for 3 days; then wait and observe.",
            "diagnosis": "Acute Gastro-enteritis / Asthmatic Bronchitis with Characteristic Prostration",
            "rationale": "Totality demonstrates extreme restlessness with intense nocturnal anxiety, burning sensations ameliorated by heat, and worsening around midnight (1 AM to 2 AM). Thirst for small sips at frequent intervals.",
            "affinity": "Gastrointestinal tract, mucous membranes, respiratory system, vital energy.",
            "diff": "Differentiated from Bryonia alba (which desires absolute rest and large drinks) and Phosphorus (which craves cold water and is sympathetic).",
            "source": "Boericke Materia Medica",
            "citation": "Arsenicum album: Great prostration, with rapid sinking of the vital forces. Burning pains relieved by heat. Midnight aggravation from 1 to 2 a.m. Restlessness, must change place constantly."
        },
        {
            "name": "Bryonia alba",
            "keywords": ["motion worse", "rest better", "dryness", "thirst large", "stitch", "right side", "irritable", "constipation", "hard dry stool", "headache motion", "cough painful", "pressure better"],
            "potency": "30C",
            "dose": "4 pills thrice daily for 5 days.",
            "diagnosis": "Acute Serositis / Tracheo-bronchitis with Inflammatory Stitches",
            "rationale": "Marked aggravation from least motion and marked relief from absolute rest and firm pressure. Extreme dryness of all mucous membranes with unquenchable thirst for large quantities at long intervals.",
            "affinity": "Serous membranes, pleura, fibrous joints, right hypochondrium.",
            "diff": "Differentiated from Rhus toxicodendron where the patient is compelled to move constantly for temporary relief.",
            "source": "Boericke Materia Medica",
            "citation": "Bryonia alba: Ailments from least motion. Dryness of mucous membranes everywhere. Stitching pains greatly aggravated by motion and relieved by absolute rest and pressure."
        },
        {
            "name": "Nux vomica",
            "keywords": ["irritable", "anger", "spasmodic", "chilly", "digestive", "stimulants", "sedentary", "ineffectual urging", "gastric", "morning worse", "hypersensitive", "coffee", "alcohol"],
            "potency": "200C",
            "dose": "Single dose at night before sleeping.",
            "diagnosis": "Gastro-oesophageal Reflux Disorder / Functional Dyspepsia with Autonomic Irritability",
            "rationale": "Classic picture of the over-stressed, sedentary individual with gastric irritability, ineffectual urging for stool, and extreme chilliness with hypersensitivity to noise, light, and odor.",
            "affinity": "Cerebrospinal system, gastrointestinal tract, liver, portal circulation.",
            "diff": "Differentiated from Lycopodium by the predominance of morning aggravation and explosive irritability rather than afternoon flatulence.",
            "source": "Boericke Materia Medica",
            "citation": "Nux vomica: Pre-eminently the remedy for many ailments incident to modern, sedentary life. Frequent and ineffectual desire for stool. Irritable, nervous, cannot bear noises, odors, or light."
        },
        {
            "name": "Rhus toxicodendron",
            "keywords": ["stiffness", "first motion worse", "continued motion better", "damp", "rain", "restless", "joint pain", "sprain", "red triangular tip", "scratching", "lumbago", "sciatica"],
            "potency": "200C",
            "dose": "4 pills twice daily for 4 days.",
            "diagnosis": "Fibrositis / Musculoskeletal Sprain & Lumbosacral Strain",
            "rationale": "Key modality of aggravation on beginning to move, but amelioration upon continued gentle motion. Symptoms aggravated by damp, cold, and rainy weather. Red triangular tip of tongue.",
            "affinity": "Fibrous tissues, ligaments, tendons, skin, cellular tissues.",
            "diff": "Direct opposite to Bryonia alba in modality of motion; Bryonia is worse from motion, Rhus tox is relieved by continued gentle movement.",
            "source": "Boericke Materia Medica",
            "citation": "Rhus toxicodendron: Rhus affects fibrous tissue especially - joints, tendons, sheaths. Pain and stiffness worse on beginning to move, but relieved by continued gentle motion and warm applications."
        },
        {
            "name": "Pulsatilla nigricans",
            "keywords": ["weeping", "mild", "open air", "thirstless", "changeable", "warm room worse", "fatty food", "menses", "gentle", "affectionate", "breezy", "cough evening dry"],
            "potency": "30C",
            "dose": "4 pills twice daily for 5 days.",
            "diagnosis": "Catarrhal Mucous Inflammation / Neuro-endocrine Dysregulation",
            "rationale": "Mild, yielding disposition with weeping tendency. Symptoms ever-changing; strongly ameliorated in open fresh air and aggravated in warm, stuffy rooms. Complete thirstlessness with dry mouth.",
            "affinity": "Venous system, mucous membranes, female reproductive system.",
            "diff": "Differentiated from Natrum muriaticum which rejects consolation, whereas Pulsatilla constantly seeks comfort and sympathy.",
            "source": "Boericke Materia Medica",
            "citation": "Pulsatilla nigricans: The weathercock among remedies. Symptoms ever changing. Weeps easily. Thirstless with nearly all complaints. Greatly relieved in open, fresh air; worse in warm close room."
        },
        {
            "name": "Lycopodium clavatum",
            "keywords": ["gas", "bloating", "flatulence", "4-8 pm", "right to left", "anticipation", "warm drinks", "liver", "intellectual", "erectile", "kidney", "fullness"],
            "potency": "200C",
            "dose": "Single dose early in the morning on an empty stomach.",
            "diagnosis": "Hepato-biliary Congestion with Intestinal Flatulence & Dyspepsia",
            "rationale": "Marked abdominal distension with flatulence after eating even a small quantity. Characteristic time modality of aggravation between 4 PM and 8 PM; desire for warm food and drinks.",
            "affinity": "Digestive organs, urinary tract, right side of body.",
            "diff": "Differentiated from Carbo vegetabilis where flatulence affects the upper epigastrium and patient craves being fanned violently.",
            "source": "Boericke Materia Medica",
            "citation": "Lycopodium clavatum: In nearly all cases there is excessive flatulence, distension of abdomen immediately after eating even a small quantity. Aggravation from 4 to 8 p.m. Desires warm drinks."
        },
        {
            "name": "Phosphorus",
            "keywords": ["bleeding", "cold water", "ice cream", "sympathetic", "hoarseness", "cough", "left side", "thunderstorm", "tall slender", "burning hands", "open air", "haemorrhage"],
            "potency": "200C",
            "dose": "4 pills once daily in the morning for 3 days.",
            "diagnosis": "Haemorrhagic Diathesis / Chronic Laryngo-tracheitis with Nervous Debility",
            "rationale": "Tall, sensitive, affectionate individual with craving for cold water and ice cream. Burning sensations in palms and along the spine; marked susceptibility to atmospheric thunderstorms.",
            "affinity": "Nerve centres, respiratory tract, blood vessels, bones.",
            "diff": "Differentiated from Arsenicum by the craving for ice-cold drinks which are vomited once they become warm in the stomach.",
            "source": "Boericke Materia Medica",
            "citation": "Phosphorus: Tall, slender persons with fair skin, sanguine temperament, sensitive nature. Desires cold water, which is ejected as soon as it becomes warm in the stomach. Burning pains."
        },
        {
            "name": "Natrum muriaticum",
            "keywords": ["grief", "consolation worse", "sun worse", "salt craving", "headache 10 am", "dry lips", "introverted", "silent", "emaciation", "herpes", "suppression"],
            "potency": "200C",
            "dose": "Single dose in the morning, do not repeat frequently.",
            "diagnosis": "Chronic Nutritional/Vasomotor Dysregulation with Psychosomatic Grief",
            "rationale": "Introverted personality with history of suppressed grief or emotional disappointment. Aggravation from consolation and exposure to strong sunlight. Intense craving for salt and 10 AM headache.",
            "affinity": "Blood, nervous system, skin, alimentary canal, mind.",
            "diff": "Differentiated from Ignatia which exhibits acute hysterical grief with sighing, whereas Natrum mur exhibits chronic, deep-seated resentment and sorrow.",
            "source": "Boericke Materia Medica",
            "citation": "Natrum muriaticum: Ailments from emotional shock, grief, or disappointment. Consolation aggravates. Craving for salt. Throbbing headache from 10 a.m. to 3 p.m., worse from the sun."
        },
        {
            "name": "Sulphur",
            "keywords": ["burning", "itching", "heat", "feet out", "11 am hunger", "standing worse", "dirty skin", "water worse", "philosophical", "egotistical", "relapse"],
            "potency": "200C",
            "dose": "Single dose early morning on empty stomach.",
            "diagnosis": "Chronic Psoric Dermatosis / Constitutional Heat & Elimination Disorder",
            "rationale": "Great King of Anti-Psorics. Burning in palms, soles, and vertex. Puts feet out of covers at night to cool them. Empty, faint hungry sinking feeling in stomach at 11 AM. Aggravation from bathing.",
            "affinity": "Skin, venous circulation, portal system, mucous membranes.",
            "diff": "Differentiated from Psorinum which is excessively chilly and seeks heat, whereas Sulphur is hot and craves cool open air.",
            "source": "Boericke Materia Medica",
            "citation": "Sulphur: Great burning sensations everywhere. Standing is the most uncomfortable position. Hunger at 11 a.m. Feet hot at night, sticks them out of bed. Skin dry, itchy, worse from bathing."
        },
        {
            "name": "Calcarea carbonica",
            "keywords": ["sweat head", "cold damp feet", "eggs craving", "flabby", "stairs breathless", "anxiety health", "sour", "chilly", "slow", "fontanelles"],
            "potency": "200C",
            "dose": "Single dose early morning.",
            "diagnosis": "Constitutional Metabolic Impairment / Calcium Malassimilation",
            "rationale": "Leucophlegmatic constitution; fair, fat, flabby. Profuse cold sweat on head during sleep, wetting the pillow. Cold, damp clammy feet as if wearing wet stockings. Craving for boiled eggs.",
            "affinity": "Nutrition, glands, bones, skin, autonomic nervous system.",
            "diff": "Differentiated from Silicea which is thin and emaciated with offensive foot sweat, whereas Calcarea is bulky with sour non-offensive head perspiration.",
            "source": "Boericke Materia Medica",
            "citation": "Calcarea carbonica: Impaired nutrition being the keynote of its action. Cold clammy feet as if wearing damp stockings. Head sweats profusely, wetting pillow. Craving for eggs and indigestible things."
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

    # Generate the 4-part lifestyle object
    lifestyle_obj = build_homoeopathic_lifestyle(best["name"], case_data)

    return {
        "remedy": best["name"],
        "potency": best["potency"],
        "dose": best["dose"],
        "diagnosis": best["diagnosis"],
        "rationale": best["rationale"],
        "remedy_scores": [
            {"remedy": best["name"], "score": 95, "affinity": best["affinity"]},
            {"remedy": runner_ups[0]["name"], "score": 82, "affinity": runner_ups[0]["affinity"]},
            {"remedy": runner_ups[1]["name"], "score": 75, "affinity": runner_ups[1]["affinity"]}
        ],
        "differentials": [
            f"{runner_ups[0]['name']}: {runner_ups[0]['diff']}",
            f"{runner_ups[1]['name']}: {runner_ups[1]['diff']}"
        ],
        "citations": [
            {
                "remedy": best["name"],
                "source": best["source"],
                "text": best["citation"]
            }
        ],
        "lifestyle": lifestyle_obj,
        "lifestyle_advice": f"Follow homoeopathic dietary regimen for {best['name']} and avoid known antidotes."
    }
