import sqlite3
import json
import uuid
import datetime

def seed():
    conn = sqlite3.connect('primeheal.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM cases WHERE patient_name LIKE '%Amit%'")
    existing = cursor.fetchone()

    case_id = existing[0] if existing else str(uuid.uuid4())
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    raw_case = {
        'name': 'Amit',
        'patient_name': 'Amit',
        'age': '25',
        'sex': 'Male',
        'occupation': 'Teacher',
        'address': 'Ahmedabad, Gujarat',
        'phone': '+91 9876543210',
        'email': 'amit.raval@example.com',
        'weight': '64 kg',
        'height': '172 cm',
        'complaints': 'Severe acidity, heartburn after meals, indigestion, ineffectual urging for stool (constipation), irritability and mental stress due to overwork, late night studying and excessive coffee intake',
        'associated_complaints': 'Occasional tension headaches, morning fatigue, gas and bloating',
        'history': 'History of sedentary lifestyle, irregular meals, prolonged mental strain as a teacher, excessive consumption of coffee to stay awake late nights.',
        'mentals': 'Irritable, impatient, fastidious, anxious about health and work performance, easily angered by contradiction',
        'vitals': 'BP: 120/80 mmHg, Pulse: 74 bpm, Temp: 98.4 F',
        'general_exam': 'Anxious facies, mild epigastric tenderness on deep palpation, coated tongue (thick white back half)',
        'systemic_exam': 'GI: Epigastric tenderness without rebound. Respiratory: Clear. CVS: Normal heart sounds.',
        'local_exam': 'No hemorrhoids or fissures visible.',
        'modalities': 'Worse: morning upon waking, after eating spicy food, coffee, mental exertion, cold air. Better: warmth, evening, resting quietly',
        'reports': 'CBC: Normal, USG Abdomen: Mild fatty liver Grade 1, otherwise normal.',
        'notes': 'Classical Nux Vomica constitution. Stress and coffee etiology with ineffectual urging pathognomonic rubric.',
        'appetite': 'Good, but feels full quickly; dyspepsia after eating',
        'cravings': 'Spicy food, coffee, stimulants, fat, rich pungent food',
        'aversions': 'Cold food, milk, meat',
        'thirst': 'Moderate, prefers warm drinks',
        'thermal': 'Chilly (craves heat and warm covers)',
        'perspiration': 'Scanty, mostly on chest and back',
        'stool': 'Hard, dry, unsatisfactory; constant ineffectual urging for stool',
        'urine': 'Normal frequency, pale amber',
        'sleep': 'Disturbed, wakes around 3-4 AM thinking of work difficulties, unrefreshing sleep',
        'sleep_position': 'On back or right side',
        'past_history': 'Frequent gastric troubles, occasional migraine from stress',
        'vaccination': 'Routine vaccinations completed',
        'family_history': 'Father has hypertension, mother has osteoarthritis',
        'diet': 'Vegetarian, irregular timings',
        'marital_status': 'Single'
    }

    result_obj = {
        'remedy': 'Nux Vomica',
        'potency': '200C',
        'dose': '4 pills of 200C, once daily in the morning on an empty stomach for 3 consecutive days, then stop all medicine and observe for 7 to 10 days before follow-up evaluation.',
        'diagnosis': 'Gastroesophageal Reflux Disease (GERD) with Dyspepsia and Dyssynergic Constipation in an overworked individual presenting as classical Nux Vomica constitutional picture',
        'rationale': 'Under Hahnemannian Organon §153, the selection of Nux Vomica is anchored upon striking, singular, uncommon, and peculiar (characteristic) keynotes: pathognomonic frequent ineffectual urging to stool where small quantities pass with persistent sensation of unexpelled feces; sharp aggravation early in the morning and from mental exertion; marked intolerance and chilliness to cold drafts; distinctive sleep disturbance waking at 3 to 4 AM with business cares; and direct toxic etiology from excessive coffee and sedentary lifestyle. Differentials Lycopodium and Sulphur were ruled out due to opposing modalities and absence of the characteristic ineffectual urging.',
        'remedy_scores': [
            {
                'remedy': 'Nux Vomica',
                'score': 94,
                'coverage': 'Ineffectual urging (pathognomonic), morning aggravation, irritability/fastidiousness, coffee craving, chilliness, 3 AM waking, workaholic stress',
                'affinity': 'Ineffectual urging (pathognomonic), morning aggravation, irritability/fastidiousness, coffee craving, chilliness, 3 AM waking, workaholic stress'
            },
            {
                'remedy': 'Lycopodium',
                'score': 76,
                'coverage': 'Ambitious personality, bloating after small meals, liver/digestive sphere, evening amelioration, irritability—but misses ineffectual urging keynote',
                'affinity': 'Ambitious personality, bloating after small meals, liver/digestive sphere, evening amelioration, irritability—but misses ineffectual urging keynote'
            },
            {
                'remedy': 'Sulphur',
                'score': 68,
                'coverage': 'Spicy food craving, morning aggravation, irritability, digestive complaints—but thermal (hot patient) contradicts chilliness here',
                'affinity': 'Spicy food craving, morning aggravation, irritability, digestive complaints—but thermal (hot patient) contradicts chilliness here'
            },
            {
                'remedy': 'Bryonia',
                'score': 61,
                'coverage': 'Irritability, constipation picture, amelioration rest—lacks ineffectual urging and coffee craving; constipation type differs (large/dry vs. urging)',
                'affinity': 'Irritability, constipation picture, amelioration rest—lacks ineffectual urging and coffee craving; constipation type differs (large/dry vs. urging)'
            }
        ],
        'differentials': [
            'Lycopodium (ambitious personality, bloating after small meals, liver/digestive focus, but less morning aggravation and no ineffectual urging keynote)',
            'Sulphur (craving spicy foods, morning aggravation, irritability, but typically hot patient with aversion to warmth—contradicts chilliness here)',
            'Bryonia (irritability, constipation with large dry stools, amelioration rest—but lacks ineffectual urging and coffee craving)'
        ],
        'citations': [
            {
                'remedy': 'Nux Vomica',
                'source': "Boericke's Materia Medica",
                'quote': 'Frequent ineffectual urging to stool; passes small quantities at each attempt. Feels as if part remained unexpelled. Wants to go constantly.',
                'text': 'Frequent ineffectual urging to stool; passes small quantities at each attempt. Feels as if part remained unexpelled. Wants to go constantly.'
            },
            {
                'remedy': 'Nux Vomica',
                'source': "Allen's Keynotes",
                'quote': 'Irritable, zealous fiery temperament. Oversensitive; cannot bear noises, odors, light. Worse morning on waking. Chilly, cannot uncover.',
                'text': 'Irritable, zealous fiery temperament. Oversensitive; cannot bear noises, odors, light. Worse morning on waking. Chilly, cannot uncover.'
            },
            {
                'remedy': 'Nux Vomica',
                'source': "Kent's Lectures on Materia Medica",
                'quote': 'Sleeps into aggravation; wakes 3-4 AM with mind on business, cannot sleep again until toward morning, then heavy sleep and hard to rouse.',
                'text': 'Sleeps into aggravation; wakes 3-4 AM with mind on business, cannot sleep again until toward morning, then heavy sleep and hard to rouse.'
            },
            {
                'remedy': 'Lycopodium',
                'source': "Boericke's Materia Medica",
                'quote': 'Ambitious but lacks self-confidence. Bloating after eating very small amount. Craves warm food and drinks. Ailments 4-8 PM worse.',
                'text': 'Ambitious but lacks self-confidence. Bloating after eating very small amount. Craves warm food and drinks. Ailments 4-8 PM worse.'
            },
            {
                'remedy': 'Sulphur',
                'source': "Nash's Leaders",
                'quote': 'Great craving for stimulants, spices, sweets. Averse to warm covers, wants windows open. Morning aggravation; weak, faint 11 AM.',
                'text': 'Great craving for stimulants, spices, sweets. Averse to warm covers, wants windows open. Morning aggravation; weak, faint 11 AM.'
            }
        ],
        'lifestyle': {
            'diet_do': [
                'Light, warm, freshly prepared easily digestible meals at fixed hours',
                'Adequate room-temperature hydration with warm water throughout the day',
                'Fresh seasonal fruits (sweet apples, papayas, pomegranates)',
                'High-fiber steamed vegetables and light soups to support peristalsis'
            ],
            'diet_avoid': [
                'Strictly avoid coffee, strong tea, energy drinks, and aerated soda (caffeine antidotes homoeopathic remedies)',
                'Strictly avoid spicy, rich, heavily spiced foods, alcohol, and late-night snacks',
                'Avoid raw onion, raw garlic, camphor, and strong menthol within 1 hour of medicine',
                'Avoid skipping meals or prolonged fasting followed by heavy eating'
            ],
            'exercises': [
                '30 to 40 minutes of gentle morning walking in fresh air before work',
                'Gentle yoga asanas: Vajrasana after meals, Pawanmuktasana, and Bhujangasana',
                'Daily Pranayama: 10-15 minutes of Anulom-Vilom alternate nostril breathing',
                'Avoid intense, exhausting workouts late in the evening'
            ],
            'lifestyle': [
                'Maintain strict, regular sleep hygiene; be in bed before 10:30 PM',
                'Disconnect from work emails, phone screens, and mental strain at least 1 hour before sleep',
                'Protect strictly against cold drafts, air conditioner blasts, and sudden exposure to cold wind',
                'Take homoeopathic medicine on a clean tongue with at least 30 minutes gap from food or drink'
            ]
        }
    }

    cursor.execute('DELETE FROM cases WHERE id = ?', (case_id,))
    cursor.execute('''
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
    ''', (
        case_id,
        raw_case['name'],
        raw_case['age'],
        raw_case['sex'],
        raw_case['occupation'],
        raw_case['address'],
        raw_case['phone'],
        raw_case['email'],
        raw_case['weight'],
        raw_case['height'],
        raw_case['complaints'],
        raw_case['associated_complaints'],
        raw_case['history'],
        raw_case['mentals'],
        raw_case['vitals'],
        raw_case['general_exam'],
        raw_case['systemic_exam'],
        raw_case['local_exam'],
        raw_case['modalities'],
        raw_case['reports'],
        raw_case['notes'],
        raw_case['appetite'],
        raw_case['cravings'],
        raw_case['aversions'],
        raw_case['thirst'],
        raw_case['thermal'],
        raw_case['perspiration'],
        raw_case['stool'],
        raw_case['urine'],
        raw_case['sleep'],
        raw_case['sleep_position'],
        raw_case['past_history'],
        raw_case['vaccination'],
        raw_case['family_history'],
        raw_case['diet'],
        raw_case['marital_status'],
        json.dumps(raw_case),
        json.dumps(result_obj),
        None,
        0,
        now,
        now
    ))

    conn.commit()
    print('Successfully saved Amit Raval case with ID:', case_id)

    cursor.execute('SELECT COUNT(*) FROM cases')
    print('Total cases in primeheal.db now:', cursor.fetchone()[0])
    conn.close()

if __name__ == '__main__':
    seed()
