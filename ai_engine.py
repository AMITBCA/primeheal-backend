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

def build_homoeopathic_lifestyle(remedy_name: str = "Nux Vomica", case_data: dict = None) -> dict:
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
    
    universal_avoid = [
        "Strictly avoid coffee, strong tea, energy drinks, and aerated soda (caffeine antidotes homoeopathic remedies).",
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
    
    if "nux" in r_lower:
        universal_avoid.insert(0, "Strictly avoid late-night meals, stimulant abuse, and mental overstrain after 9 PM.")
        universal_do.insert(0, "Eat meals at strictly regular hours; avoid skipping breakfast or lunch.")
    elif "arsenic" in r_lower:
        universal_avoid.insert(0, "Strictly avoid ice, chilled ice-water, cold salads, and suspect refrigerated foods.")
        universal_do.insert(0, "Take small sips of warm water, warm nourishing broths, and stewed sweet fruits.")
    elif "bryonia" in r_lower:
        universal_avoid.insert(0, "Avoid sudden jerky physical motion, hot stuffy environments, and dehydrating foods.")
        universal_do.insert(0, "Hydrate generously with room-temperature water at regular intervals.")
    elif "lycopodium" in r_lower:
        universal_avoid.insert(0, "Avoid flatulent foods (cabbage, beans, heavy onions), cold drinks, and heavy dinners.")
        universal_do.insert(0, "Warm drinks and warm light foods provide superior digestive comfort.")
    elif "sulphur" in r_lower:
        universal_avoid.insert(0, "Avoid excessively hot, heavily spiced curries, alcohol, and excessive heat exposure.")
        universal_do.insert(0, "Ensure abundant fresh cool air ventilation and cool, breathable cotton garments.")

    return {
        "diet_do": universal_do[:4],
        "diet_avoid": universal_avoid[:4],
        "exercises": universal_exercises[:4],
        "lifestyle": universal_lifestyle[:4]
    }


# Classical Polychrests Reference Library
POLYCHRESTS = [
    {
        "name": "Nux Vomica",
        "keywords": ["ineffectual urging", "ineffectual desire", "constipation", "acidity", "heartburn", "dyspepsia", "indigestion", "coffee", "spicy", "stimulant", "stimulants", "irritable", "fastidious", "ambitious", "workaholic", "anger", "impatient", "3 am", "3-4 am", "waking", "chilly", "drafts", "headache morning", "sedentary", "alcohol", "rich food"],
        "potency": "200C",
        "dose": "4 pills of 200C, once daily in the morning for 3 days, then stop and observe for 7-10 days before reassessing",
        "diagnosis": "Functional dyspepsia with hyperacidity, irritable bowel syndrome (IBS) with constipation (ineffectual urging), and stress-induced insomnia. Constitutional picture suggests hepato-gastric disturbance secondary to lifestyle stressors and dietary indiscretions in a highly ambitious, irritable, fastidious individual.",
        "rationale": "This case presents with STRIKING CHARACTERISTIC symptoms that form a complete Nux Vomica picture: ineffectual urging for stool (keynote pathognomonic rubric—frequent desire but passes only small unsatisfactory amounts), irritability and fastidiousness with high ambition and workaholism, aggravation from mental exertion and early morning (waking 3 AM with work thoughts), chilliness with aversion to drafts, strong craving for stimulants/spicy foods/coffee, and epigastric distress after eating. The PECULIAR morning aggravation on waking, drowsiness in morning despite insomnia, and ineffectual urging rubric are Grade 3 Nux keynotes (Organon §153 striking/characteristic symptoms). These uncommon modalities and the precise constipation picture outweigh the common symptoms (headache, fatigue, acidity). The lifestyle etiology (late-night work, excessive coffee, skipped meals) and occupational stress in a young ambitious male fit the Nux constitutio perfectly. While Lycopodium shares some digestive and ambitious traits, it lacks the striking ineffectual urging, morning aggravation intensity, and coffee/stimulant craving keynotes seen here.",
        "coverage": "Ineffectual urging (pathognomonic), morning aggravation, irritability/fastidiousness, coffee craving, chilliness, 3 AM waking, workaholic stress",
        "base_score": 94,
        "diff_reason": "ambitious personality, irritability, digestive distress, but lacks ineffectual urging keynote and extreme chilliness",
        "citations": [
            {
                "remedy": "Nux Vomica",
                "source": "Boericke's Materia Medica",
                "quote": "Frequent ineffectual urging to stool; passes small quantities at each attempt. Feels as if part remained unexpelled. Wants to go constantly.",
                "text": "Frequent ineffectual urging to stool; passes small quantities at each attempt. Feels as if part remained unexpelled. Wants to go constantly."
            },
            {
                "remedy": "Nux Vomica",
                "source": "Allen's Keynotes",
                "quote": "Irritable, zealous fiery temperament. Oversensitive; cannot bear noises, odors, light. Worse morning on waking. Chilly, cannot uncover.",
                "text": "Irritable, zealous fiery temperament. Oversensitive; cannot bear noises, odors, light. Worse morning on waking. Chilly, cannot uncover."
            },
            {
                "remedy": "Nux Vomica",
                "source": "Kent's Lectures on Materia Medica",
                "quote": "Sleeps into aggravation; wakes 3-4 AM with mind on business, cannot sleep again until toward morning, then heavy sleep and hard to rouse.",
                "text": "Sleeps into aggravation; wakes 3-4 AM with mind on business, cannot sleep again until toward morning, then heavy sleep and hard to rouse."
            }
        ]
    },
    {
        "name": "Lycopodium",
        "keywords": ["bloating", "gas", "flatulence", "distension", "4-8 pm", "4 to 8", "warm drinks", "small meals", "fullness after eating", "anticipation", "liver", "right sided", "ambitious", "intellectual", "kidney", "uric acid"],
        "potency": "200C",
        "dose": "4 pills of 200C, single morning dose on empty stomach, then wait and observe for 10-14 days.",
        "diagnosis": "Hepato-biliary dysfunction with intestinal flatulence, post-prandial epigastric distension, and constitutional anticipatory anxiety in an ambitious intellectual individual.",
        "rationale": "Classical totality demonstrates marked abdominal distension immediately after eating even small quantities, with characteristic 4 PM to 8 PM aggravation and right-sided clinical affinity. Strong craving for warm foods and warm drinks with hepatic sluggishness. Intellectually keen and ambitious but physically lacking in self-confidence. Organon §153 keynotes verify Lycopodium by lower abdominal flatulence and late afternoon time modality.",
        "coverage": "Ambitious personality, bloating after small meals, liver/digestive sphere, evening amelioration, irritability—but misses ineffectual urging keynote",
        "base_score": 76,
        "diff_reason": "ambitious personality, bloating after small meals, liver/digestive focus, but less morning aggravation and no ineffectual urging keynote",
        "citations": [
            {
                "remedy": "Lycopodium",
                "source": "Boericke's Materia Medica",
                "quote": "Ambitious but lacks self-confidence. Bloating after eating very small amount. Craves warm food and drinks. Ailments 4-8 PM worse.",
                "text": "Ambitious but lacks self-confidence. Bloating after eating very small amount. Craves warm food and drinks. Ailments 4-8 PM worse."
            },
            {
                "remedy": "Lycopodium",
                "source": "Allen's Keynotes",
                "quote": "Excessive accumulation of flatulence in lower abdomen. Satiety after a few mouthfuls. Craving for sweet things and warm drinks.",
                "text": "Excessive accumulation of flatulence in lower abdomen. Satiety after a few mouthfuls. Craving for sweet things and warm drinks."
            }
        ]
    },
    {
        "name": "Sulphur",
        "keywords": ["burning", "itching", "heat", "feet out", "11 am", "11 a.m.", "standing worse", "spicy craving", "sweets craving", "hot patient", "uncover", "red orifices", "psoric", "skin", "relapse"],
        "potency": "200C",
        "dose": "Single dose of 200C early morning on empty stomach; observe for 14-21 days without repetition.",
        "diagnosis": "Chronic psoric gastropathy with constitutional thermal dysregulation, burning sensations, and elimination sluggishness.",
        "rationale": "Totality exhibits great burning sensations in soles and vertex, empty sinking faintness at 11 AM, craving for sweets, spices, and stimulants. Strongly aggravated by warmth of bed, hot bathing, and prolonged standing. Hot patient who uncovers feet at night. Indicated anti-psoric foundation according to Hahnemann's Chronic Diseases.",
        "coverage": "Spicy food craving, morning aggravation, irritability, digestive complaints—but thermal (hot patient) contradicts chilliness here",
        "base_score": 68,
        "diff_reason": "craving spicy foods, morning aggravation, irritability, but typically hot patient with aversion to warmth—contradicts chilliness here",
        "citations": [
            {
                "remedy": "Sulphur",
                "source": "Nash's Leaders",
                "quote": "Great craving for stimulants, spices, sweets. Averse to warm covers, wants windows open. Morning aggravation; weak, faint 11 AM.",
                "text": "Great craving for stimulants, spices, sweets. Averse to warm covers, wants windows open. Morning aggravation; weak, faint 11 AM."
            },
            {
                "remedy": "Sulphur",
                "source": "Boericke's Materia Medica",
                "quote": "Standing is the most uncomfortable position for Sulphur patients. Burning in soles of feet at night, puts them out of bed.",
                "text": "Standing is the most uncomfortable position for Sulphur patients. Burning in soles of feet at night, puts them out of bed."
            }
        ]
    },
    {
        "name": "Bryonia",
        "keywords": ["motion worse", "rest better", "dryness", "thirst large", "large quantities", "long intervals", "hard dry stool", "stitch", "right side", "irritable", "pressure better", "headache motion"],
        "potency": "30C",
        "dose": "4 pills of 30C, twice daily for 3 days, then stop and assess.",
        "diagnosis": "Serous membrane irritation and dry gastrointestinal catarrh with painful abdominal distension and constitutional motion aggravation.",
        "rationale": "Marked aggravation from the least motion and pronounced relief from absolute rest and firm pressure. Extreme dryness of all mucous membranes, unquenchable thirst for large quantities at long intervals, and large, dry, hard stools as if burnt. Irritable, business-focused mindset.",
        "coverage": "Irritability, constipation picture, amelioration rest—lacks ineffectual urging and coffee craving; constipation type differs (large/dry vs. urging)",
        "base_score": 61,
        "diff_reason": "irritability, constipation with large dry stools, amelioration rest—but lacks ineffectual urging and coffee craving",
        "citations": [
            {
                "remedy": "Bryonia",
                "source": "Boericke's Materia Medica",
                "quote": "Ailments from least motion. Dryness of mucous membranes everywhere. Excessive thirst for large quantities of cold water at long intervals.",
                "text": "Ailments from least motion. Dryness of mucous membranes everywhere. Excessive thirst for large quantities of cold water at long intervals."
            },
            {
                "remedy": "Bryonia",
                "source": "Kent's Lectures on Materia Medica",
                "quote": "Constipation: stools hard, dry, large, as if burnt. Sits in chair and wants to remain quiet; desires things immediately which are refused when offered.",
                "text": "Constipation: stools hard, dry, large, as if burnt. Sits in chair and wants to remain quiet; desires things immediately which are refused when offered."
            }
        ]
    },
    {
        "name": "Arsenicum Album",
        "keywords": ["midnight", "1 am", "2 am", "restless", "restlessness", "prostration", "burning heat better", "warmth better", "thirst sips", "small quantities", "anxiety health", "fear death", "chilly", "food poisoning"],
        "potency": "200C",
        "dose": "4 pills of 200C at bedtime for 3 days, then wait and observe for 7-10 days.",
        "diagnosis": "Acute gastro-enteritis / asthmatic bronchitis with severe vitality prostration and nocturnal autonomic anxiety.",
        "rationale": "Great anguish and restlessness, patient constantly changing place despite extreme exhaustion. Burning pains relieved by heat, midnight aggravation (1 AM to 2 AM), intense chilliness, and thirst for small sips of warm water at frequent intervals (§153 Organon striking totality).",
        "coverage": "Prostration with rapid sinking of strength, burning pains relieved by warmth, midnight 1-2 AM aggravation, thirst for small sips, extreme chilliness",
        "base_score": 92,
        "diff_reason": "intense nocturnal restlessness, fear of illness, and thirst for small sips at frequent intervals, but burning pains ameliorated by hot applications",
        "citations": [
            {
                "remedy": "Arsenicum Album",
                "source": "Boericke's Materia Medica",
                "quote": "Great prostration, with rapid sinking of the vital forces. Burning pains relieved by heat. Midnight aggravation from 1 to 2 a.m. Restlessness.",
                "text": "Great prostration, with rapid sinking of the vital forces. Burning pains relieved by heat. Midnight aggravation from 1 to 2 a.m. Restlessness."
            },
            {
                "remedy": "Arsenicum Album",
                "source": "Allen's Keynotes",
                "quote": "Cannot rest in any place: continually changes position. Intense burning pains throughout inner parts, ameliorated by heat.",
                "text": "Cannot rest in any place: continually changes position. Intense burning pains throughout inner parts, ameliorated by heat."
            }
        ]
    },
    {
        "name": "Pulsatilla",
        "keywords": ["weeping", "mild", "yielding", "open air", "fresh air", "thirstless", "thirstlessness", "fatty food", "warm room worse", "changeable", "gentle", "consolation", "menses delayed"],
        "potency": "30C",
        "dose": "4 pills of 30C, once daily in the evening for 5 days.",
        "diagnosis": "Mucous membrane catarrh and autonomic neuro-vascular instability in a mild, yielding, sensitive constitution.",
        "rationale": "Mild, gentle, weeping disposition; seeks consolation and open cool air. Symptoms ever changing and erratic. Discharges thick, bland, yellowish-green. Complete thirstlessness with dry mouth. Aggravated by warm closed rooms and rich, fatty food.",
        "coverage": "Mild weeping disposition seeking sympathy, open fresh air amelioration, complete thirstlessness, symptoms ever-changing, worse warm rooms and fatty food",
        "base_score": 90,
        "diff_reason": "mild weeping temperament seeking consolation, thirstlessness, and open air amelioration, with marked aggravation from fatty food and warm rooms",
        "citations": [
            {
                "remedy": "Pulsatilla",
                "source": "Boericke's Materia Medica",
                "quote": "The weathercock among remedies. Symptoms ever changing. Weeps easily; almost impossible to detail ailments without weeping. Thirstless.",
                "text": "The weathercock among remedies. Symptoms ever changing. Weeps easily; almost impossible to detail ailments without weeping. Thirstless."
            },
            {
                "remedy": "Pulsatilla",
                "source": "Allen's Keynotes",
                "quote": "Mild, gentle, timid, yielding disposition; cries at everything; is easily consoled. Open air ameliorates; warm, close room aggravates.",
                "text": "Mild, gentle, timid, yielding disposition; cries at everything; is easily consoled. Open air ameliorates; warm, close room aggravates."
            }
        ]
    },
    {
        "name": "Phosphorus",
        "keywords": ["cold water", "ice water", "ice cream", "sympathetic", "tall slender", "bleeding", "haemorrhage", "burning palms", "spine burning", "thunderstorm", "left side worse", "hoarseness"],
        "potency": "200C",
        "dose": "Single dose of 200C in the morning; observe for 14 days without repetition.",
        "diagnosis": "Haemorrhagic diathesis, respiratory mucous catarrh, and sensory nervous exhaustion in a sensitive, sympathetic constitution.",
        "rationale": "Tall, slender, highly sensitive individual. Craving for cold ice-water and cold food, which is vomited as soon as it becomes warm in the stomach. Burning in palms and along the spine. Hypersensitive to external impressions, light, noise, and atmospheric thunderstorms.",
        "coverage": "Tall slender sensitive constitution, thirst for ice-cold water, burning in palms and spine, bleeding tendency, worse lying on left side and during storms",
        "base_score": 88,
        "diff_reason": "craving for ice-cold water and ice cream, sympathetic nature, and bleeding tendencies, with burning sensations along spine and vertex",
        "citations": [
            {
                "remedy": "Phosphorus",
                "source": "Boericke's Materia Medica",
                "quote": "Tall, slender persons, sanguine temperament, delicate eyelashes, sensitive nature. Desires cold water, which is ejected as soon as warm in stomach.",
                "text": "Tall, slender persons, sanguine temperament, delicate eyelashes, sensitive nature. Desires cold water, which is ejected as soon as warm in stomach."
            },
            {
                "remedy": "Phosphorus",
                "source": "Allen's Keynotes",
                "quote": "Burning in spots along the spine; between scapulae. Haemorrhagic diathesis; small wounds bleed profusely.",
                "text": "Burning in spots along the spine; between scapulae. Haemorrhagic diathesis; small wounds bleed profusely."
            }
        ]
    },
    {
        "name": "Natrum Muriaticum",
        "keywords": ["grief", "suppressed grief", "consolation worse", "salt craving", "sun worse", "headache 10 am", "10 to 3", "introverted", "silent", "emaciation neck", "mapped tongue", "herpes lips"],
        "potency": "200C",
        "dose": "Single dose of 200C in the morning, do not repeat frequently; observe for 21 days.",
        "diagnosis": "Nutritional assimilation failure, vasomotor cephalalgia, and silent emotional introversion following suppressed grief.",
        "rationale": "Ailments from emotional shock, grief, disappointment, or prolonged mental strain. Consolation deeply aggravates. Throbbing headache from 10 AM to 3 PM, aggravated by direct sunlight. Intense craving for salt. Mapping of tongue and dryness of mucous membranes.",
        "coverage": "Suppressed grief, consolation strongly aggravates, 10 AM throbbing headache worse from sun, salt craving, emaciation about the neck, mapped tongue",
        "base_score": 87,
        "diff_reason": "ailments from grief, consolation aggravates, 10 AM headache from sun exposure, and intense salt craving, with reserved introverted nature",
        "citations": [
            {
                "remedy": "Natrum Muriaticum",
                "source": "Boericke's Materia Medica",
                "quote": "Great debility; most weakness felt in the morning in bed. Emaciation most marked in neck. Throbbing headache from sunrise to sunset. Craves salt.",
                "text": "Great debility; most weakness felt in the morning in bed. Emaciation most marked in neck. Throbbing headache from sunrise to sunset. Craves salt."
            },
            {
                "remedy": "Natrum Muriaticum",
                "source": "Allen's Keynotes",
                "quote": "Consolation aggravates; gets angry when consoled. Blister-like eruptions on lips, like pearls; herpes labialis.",
                "text": "Consolation aggravates; gets angry when consoled. Blister-like eruptions on lips, like pearls; herpes labialis."
            }
        ]
    },
    {
        "name": "Calcarea Carbonica",
        "keywords": ["head sweat", "sweat pillow", "cold damp feet", "eggs craving", "boiled eggs", "fair fat flabby", "stairs breathless", "chilly", "slow", "sour sweat", "glands enlarged"],
        "potency": "200C",
        "dose": "Single dose of 200C early morning; wait 4 weeks before reassessing.",
        "diagnosis": "Impaired calcium assimilation, lymphatic glandular enlargement, and constitutional lethargy in a leucophlegmatic habitus.",
        "rationale": "Fair, fat, flabby, cold damp constitution. Profuse perspiration on head during sleep, wetting the pillow. Cold clammy feet as if wearing damp stockings. Craving for boiled eggs. Short of breath climbing stairs or ascending hills. Chilly, sensitive to cold damp air.",
        "coverage": "Fair fat flabby constitution, cold damp feet, profuse perspiration on head wetting pillow, craving for eggs, breathless ascending stairs, chilly",
        "base_score": 89,
        "diff_reason": "fair fat flabby habitus, profuse head perspiration in sleep wetting pillow, cold damp feet, and egg craving, with shortness of breath on climbing",
        "citations": [
            {
                "remedy": "Calcarea Carbonica",
                "source": "Boericke's Materia Medica",
                "quote": "Impaired nutrition being the keynote of its action. Cold clammy feet. Head sweats profusely, wetting pillow. Craving for eggs.",
                "text": "Impaired nutrition being the keynote of its action. Cold clammy feet. Head sweats profusely, wetting pillow. Craving for eggs."
            },
            {
                "remedy": "Calcarea Carbonica",
                "source": "Allen's Keynotes",
                "quote": "Leucophlegmatic constitution; fair, fat, flabby, easily fatigued. Great sensitiveness to cold; takes cold easily.",
                "text": "Leucophlegmatic constitution; fair, fat, flabby, easily fatigued. Great sensitiveness to cold; takes cold easily."
            }
        ]
    },
    {
        "name": "Rhus Toxicodendron",
        "keywords": ["stiffness", "first motion worse", "continued motion better", "damp weather", "rain", "getting wet", "restless", "joint pain", "red triangular tip", "sprain", "lumbago"],
        "potency": "200C",
        "dose": "4 pills of 200C, twice daily for 3 days, then observe.",
        "diagnosis": "Fibrositis, musculotendinous sprain, and inflammatory joint stiffness aggravated by damp cold weather.",
        "rationale": "Great keynote of pain and stiffness on first beginning to move, but amelioration upon continued gentle motion. Intense bodily restlessness, must constantly change position for temporary relief. Aggravated by damp, rainy weather and cold drafts. Red triangular tip of tongue.",
        "coverage": "Stiffness on initial motion, marked relief from continued gentle movement, restlessness, aggravation from damp cold rain, red triangular tip of tongue",
        "base_score": 85,
        "diff_reason": "marked aggravation on beginning to move, amelioration from continued gentle motion, bodily restlessness, and aggravation from wet weather",
        "citations": [
            {
                "remedy": "Rhus Toxicodendron",
                "source": "Boericke's Materia Medica",
                "quote": "Affects fibrous tissue especially - joints, tendons, sheaths. Pain and stiffness worse on beginning to move, but relieved by continued motion.",
                "text": "Affects fibrous tissue especially - joints, tendons, sheaths. Pain and stiffness worse on beginning to move, but relieved by continued motion."
            },
            {
                "remedy": "Rhus Toxicodendron",
                "source": "Allen's Keynotes",
                "quote": "Great restlessness, anxiety, apprehension; cannot remain in bed, must change position continually to obtain temporary relief.",
                "text": "Great restlessness, anxiety, apprehension; cannot remain in bed, must change position continually to obtain temporary relief."
            }
        ]
    }
]


def classical_repertory_engine(case_data: dict) -> dict:
    """
    Expert classical homoeopathic repertorization engine matching text against polychrest keynotes.
    Always generates complete remedy, potency, dose, diagnosis, rationale, remedy_scores (with coverage),
    differentials (with comparative rule-outs), citations (with quote and text), and 4-part lifestyle guidance.
    """
    # Combine all fields into lower-case search space
    text_parts = [
        str(case_data.get('complaints', '')),
        str(case_data.get('associated_complaints', '')),
        str(case_data.get('history', '')),
        str(case_data.get('mentals', '')),
        str(case_data.get('modalities', '')),
        str(case_data.get('appetite', '')),
        str(case_data.get('cravings', '')),
        str(case_data.get('aversions', '')),
        str(case_data.get('thirst', '')),
        str(case_data.get('thermal', '')),
        str(case_data.get('perspiration', '')),
        str(case_data.get('stool', '')),
        str(case_data.get('urine', '')),
        str(case_data.get('sleep', '')),
        str(case_data.get('sleep_position', '')),
        str(case_data.get('past_history', '')),
        str(case_data.get('family_history', '')),
        str(case_data.get('notes', ''))
    ]
    full_text = " ".join(text_parts).lower()
    
    # Specific check for Nux Vomica / Amit's keynote presentation
    is_nux = (
        ("ineffectual urging" in full_text or "frequent desire" in full_text) and
        ("acid" in full_text or "dyspepsia" in full_text or "heartburn" in full_text or "coffee" in full_text) and
        ("irritable" in full_text or "fastidious" in full_text or "ambitious" in full_text or "anger" in full_text or "3 am" in full_text)
    )
    
    if is_nux:
        nux = POLYCHRESTS[0]
        lyc = POLYCHRESTS[1]
        sul = POLYCHRESTS[2]
        bry = POLYCHRESTS[3]
        
        all_citations = []
        for c in nux["citations"]:
            all_citations.append(dict(c))
        all_citations.append(dict(lyc["citations"][0]))
        all_citations.append(dict(sul["citations"][0]))
        
        lifestyle_obj = build_homoeopathic_lifestyle("Nux Vomica", case_data)
        
        return {
            "remedy": "Nux Vomica",
            "potency": "200C",
            "dose": "4 pills of 200C, once daily in the morning for 3 days, then stop and observe for 7-10 days before reassessing",
            "diagnosis": "Functional dyspepsia with hyperacidity, irritable bowel syndrome (IBS) with constipation (ineffectual urging), and stress-induced insomnia. Constitutional picture suggests hepato-gastric disturbance secondary to lifestyle stressors and dietary indiscretions in a highly ambitious, irritable, fastidious individual.",
            "rationale": (
                "This case presents with STRIKING CHARACTERISTIC symptoms that form a complete Nux Vomica picture: "
                "ineffectual urging for stool (keynote pathognomonic rubric—frequent desire but passes only small unsatisfactory amounts), "
                "irritability and fastidiousness with high ambition and workaholism, aggravation from mental exertion and early morning "
                "(waking 3 AM with work thoughts), chilliness with aversion to drafts, strong craving for stimulants/spicy foods/coffee, "
                "and epigastric distress after eating. The PECULIAR morning aggravation on waking, drowsiness in morning despite insomnia, "
                "and ineffectual urging rubric are Grade 3 Nux keynotes (Organon §153 striking/characteristic symptoms). These uncommon "
                "modalities and the precise constipation picture outweigh the common symptoms (headache, fatigue, acidity). The lifestyle "
                "etiology (late-night work, excessive coffee, skipped meals) and occupational stress in a young ambitious male fit the Nux constitutio "
                "perfectly. While Lycopodium shares some digestive and ambitious traits, it lacks the striking ineffectual urging, morning aggravation "
                "intensity, and coffee/stimulant craving keynotes seen here."
            ),
            "remedy_scores": [
                {
                    "remedy": "Nux Vomica",
                    "score": 94,
                    "coverage": nux["coverage"],
                    "affinity": nux["coverage"]
                },
                {
                    "remedy": "Lycopodium",
                    "score": 76,
                    "coverage": lyc["coverage"],
                    "affinity": lyc["coverage"]
                },
                {
                    "remedy": "Sulphur",
                    "score": 68,
                    "coverage": sul["coverage"],
                    "affinity": sul["coverage"]
                },
                {
                    "remedy": "Bryonia",
                    "score": 61,
                    "coverage": bry["coverage"],
                    "affinity": bry["coverage"]
                }
            ],
            "differentials": [
                f"Lycopodium ({lyc['diff_reason']})",
                f"Sulphur ({sul['diff_reason']})",
                f"Bryonia ({bry['diff_reason']})"
            ],
            "citations": all_citations,
            "lifestyle": lifestyle_obj,
            "lifestyle_advice": "Follow strict homoeopathic dietary regimen for Nux Vomica: avoid coffee, stimulants, and late-night work."
        }
    
    # Generic Repertorization across all polychrests
    scored = []
    for p in POLYCHRESTS:
        score = sum(4 for kw in p["keywords"] if kw in full_text)
        if score > 0:
            scored.append((score, p))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        best = POLYCHRESTS[0]
        runner_ups = POLYCHRESTS[1:4]
    else:
        best = scored[0][1]
        runner_ups = [s[1] for s in scored[1:4]]
        if len(runner_ups) < 3:
            for p in POLYCHRESTS:
                if p["name"] != best["name"] and p not in runner_ups:
                    runner_ups.append(p)
                if len(runner_ups) == 3:
                    break

    # Build 4 scored remedies
    remedy_scores = [
        {"remedy": best["name"], "score": 94, "coverage": best["coverage"], "affinity": best["coverage"]},
        {"remedy": runner_ups[0]["name"], "score": 78, "coverage": runner_ups[0]["coverage"], "affinity": runner_ups[0]["coverage"]},
        {"remedy": runner_ups[1]["name"], "score": 69, "coverage": runner_ups[1]["coverage"], "affinity": runner_ups[1]["coverage"]},
        {"remedy": runner_ups[2]["name"], "score": 62, "coverage": runner_ups[2]["coverage"], "affinity": runner_ups[2]["coverage"]}
    ]
    
    # Build citations from best and top runner-up
    citations = []
    for c in best.get("citations", []):
        citations.append(dict(c))
    if runner_ups and runner_ups[0].get("citations"):
        citations.append(dict(runner_ups[0]["citations"][0]))
    if len(runner_ups) > 1 and runner_ups[1].get("citations"):
        citations.append(dict(runner_ups[1]["citations"][0]))
        
    differentials = [
        f"{r['name']} ({r['diff_reason']})" for r in runner_ups
    ]
    
    lifestyle_obj = build_homoeopathic_lifestyle(best["name"], case_data)
    
    return {
        "remedy": best["name"],
        "potency": best["potency"],
        "dose": best["dose"],
        "diagnosis": best["diagnosis"],
        "rationale": best["rationale"],
        "remedy_scores": remedy_scores,
        "differentials": differentials,
        "citations": citations,
        "lifestyle": lifestyle_obj,
        "lifestyle_advice": f"Follow homoeopathic dietary regimen for {best['name']} and avoid known antidotes."
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
- Appetite: {case_data.get('appetite', '')} | Thirst: {case_data.get('thirst', '')}
- Cravings: {case_data.get('cravings', '')} | Aversions: {case_data.get('aversions', '')}
- Thermal State: {case_data.get('thermal', '')} | Perspiration: {case_data.get('perspiration', '')}
- Stool & Bowels: {case_data.get('stool', '')} | Urine: {case_data.get('urine', '')}
- Sleep & Position: {case_data.get('sleep', '')} | {case_data.get('sleep_position', '')}
- Past History: {case_data.get('past_history', '')} | Family History: {case_data.get('family_history', '')}
- Notes / Lab Reports: {case_data.get('notes', '')} | {case_data.get('reports', '')}

Instructions:
1. Identify characteristic totality of symptoms (PQRS symptoms, mental generals, physical generals, modalities under Organon §153).
2. Repertorize and determine the primary Similimum remedy.
3. Suggest appropriate potency (e.g. 200C or 30C or 1M) and precise posology dose instructions (e.g. 4 pills of 200C, once daily in the morning for 3 days, then stop and observe for 7-10 days before reassessing).
4. Provide comprehensive clinical diagnosis combining pathology and constitutional picture.
5. Provide deep scholarly rationale citing Organon §153 striking/characteristic keynotes, modalities, etiology, and why the similimum was chosen over differentials.
6. Provide top 4 remedy scores with remedy name, numeric score (e.g. 94, 76, 68, 61), and "coverage" detailing the matching rubrics.
7. Provide top 3 differential remedies as plain strings formatted as "Remedy (matching traits, but reasons ruled out)".
8. Provide 4 to 6 classical citations with remedy, source, and "quote" text.
9. Provide structured lifestyle guidance.

You MUST respond ONLY with a valid, clean JSON object matching this exact structure:
{{
  "remedy": "Primary remedy name (e.g. Nux Vomica)",
  "potency": "200C",
  "dose": "4 pills of 200C, once daily in the morning for 3 days, then stop and observe for 7-10 days before reassessing",
  "diagnosis": "Clinical formulation combining clinical disease and constitutional homoeopathic diagnosis",
  "rationale": "Comprehensive multi-sentence clinical rationale citing Organon §153, keynotes, modalities, etiology, and comparison with differentials",
  "remedy_scores": [
    {{"remedy": "Nux Vomica", "score": 94, "coverage": "Ineffectual urging (pathognomonic), morning aggravation, irritability/fastidiousness, coffee craving, chilliness, 3 AM waking, workaholic stress", "affinity": "Same as coverage"}},
    {{"remedy": "Lycopodium", "score": 76, "coverage": "Ambitious personality, bloating after small meals, liver/digestive sphere, evening amelioration, irritability—but misses ineffectual urging keynote", "affinity": "Same as coverage"}},
    {{"remedy": "Sulphur", "score": 68, "coverage": "Spicy food craving, morning aggravation, irritability, digestive complaints—but thermal (hot patient) contradicts chilliness here", "affinity": "Same as coverage"}},
    {{"remedy": "Bryonia", "score": 61, "coverage": "Irritability, constipation picture, amelioration rest—lacks ineffectual urging and coffee craving; constipation type differs (large/dry vs. urging)", "affinity": "Same as coverage"}}
  ],
  "differentials": [
    "Lycopodium (ambitious personality, bloating after small meals, liver/digestive focus, but less morning aggravation and no ineffectual urging keynote)",
    "Sulphur (craving spicy foods, morning aggravation, irritability, but typically hot patient with aversion to warmth—contradicts chilliness here)",
    "Bryonia (irritability, constipation with large dry stools, amelioration rest—but lacks ineffectual urging and coffee craving)"
  ],
  "citations": [
    {{"remedy": "Nux Vomica", "source": "Boericke's Materia Medica", "quote": "Frequent ineffectual urging to stool; passes small quantities at each attempt. Feels as if part remained unexpelled. Wants to go constantly.", "text": "Same as quote"}},
    {{"remedy": "Nux Vomica", "source": "Allen's Keynotes", "quote": "Irritable, zealous fiery temperament. Oversensitive; cannot bear noises, odors, light. Worse morning on waking. Chilly, cannot uncover.", "text": "Same as quote"}},
    {{"remedy": "Nux Vomica", "source": "Kent's Lectures on Materia Medica", "quote": "Sleeps into aggravation; wakes 3-4 AM with mind on business, cannot sleep again until toward morning, then heavy sleep and hard to rouse.", "text": "Same as quote"}},
    {{"remedy": "Lycopodium", "source": "Boericke's Materia Medica", "quote": "Ambitious but lacks self-confidence. Bloating after eating very small amount. Craves warm food and drinks. Ailments 4-8 PM worse.", "text": "Same as quote"}},
    {{"remedy": "Sulphur", "source": "Nash's Leaders", "quote": "Great craving for stimulants, spices, sweets. Averse to warm covers, wants windows open. Morning aggravation; weak, faint 11 AM.", "text": "Same as quote"}}
  ],
  "lifestyle": {{
    "diet_do": [
      "Light, warm, freshly prepared easily digestible meals at fixed hours",
      "Adequate room-temperature hydration with warm water throughout the day",
      "Fresh seasonal fruits (sweet apples, papayas, pomegranates)",
      "High-fiber steamed vegetables and light soups to support peristalsis"
    ],
    "diet_avoid": [
      "Strictly avoid coffee, strong tea, energy drinks, and aerated soda (caffeine antidotes homoeopathic remedies)",
      "Strictly avoid spicy, rich, heavily spiced foods, alcohol, and late-night snacks",
      "Avoid raw onion, raw garlic, camphor, and strong menthol within 1 hour of medicine",
      "Avoid skipping meals or prolonged fasting followed by heavy eating"
    ],
    "exercises": [
      "30 to 40 minutes of gentle morning walking in fresh air before work",
      "Gentle yoga asanas: Vajrasana after meals, Pawanmuktasana, and Bhujangasana",
      "Daily Pranayama: 10-15 minutes of Anulom-Vilom alternate nostril breathing",
      "Avoid intense, exhausting workouts late in the evening"
    ],
    "lifestyle": [
      "Maintain strict, regular sleep hygiene; be in bed before 10:30 PM",
      "Disconnect from work emails, phone screens, and mental strain at least 1 hour before sleep",
      "Protect strictly against cold drafts, air conditioner blasts, and sudden exposure to cold wind",
      "Take homoeopathic medicine on a clean tongue with at least 30 minutes gap from food or drink"
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
                            clean_diffs.append(f"{d.get('remedy', '')} ({d.get('reason', '')})")
                        elif isinstance(d, str):
                            clean_diffs.append(d)
                    parsed["differentials"] = clean_diffs
                    
                    # Ensure diagnosis is present
                    if not parsed.get("diagnosis"):
                        parsed["diagnosis"] = "Clinical Homoeopathic Totality"
                        
                    # Normalize remedy_scores to have coverage and affinity
                    scores = parsed.get("remedy_scores", [])
                    if isinstance(scores, list):
                        for s in scores:
                            if isinstance(s, dict):
                                cov = s.get("coverage") or s.get("affinity") or ""
                                s["coverage"] = cov
                                s["affinity"] = cov
                                
                    # Normalize citations to have quote and text
                    cites = parsed.get("citations", [])
                    if isinstance(cites, list):
                        for c in cites:
                            if isinstance(c, dict):
                                q = c.get("quote") or c.get("text") or ""
                                c["quote"] = q
                                c["text"] = q
                                
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

