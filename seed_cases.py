import sqlite3
import json
import uuid
import datetime

GOLDEN_CASES = [
    {
        "id": "7e8c9c35-27da-46cd-a54c-2ff10c405183",
        "name": "Amit",
        "age": "25",
        "sex": "Male",
        "occupation": "Teacher",
        "address": "Ahmedabad, Gujarat",
        "phone": "+91 9876543210",
        "email": "amit.raval@example.com",
        "weight": "64 kg",
        "height": "172 cm",
        "complaints": "Severe acidity, heartburn after meals, indigestion, ineffectual urging for stool (constipation), irritability and mental stress due to overwork, late night studying and excessive coffee intake",
        "associated_complaints": "Occasional tension headaches, morning fatigue, gas and bloating",
        "history": "History of sedentary lifestyle, irregular meals, prolonged mental strain as a teacher, excessive consumption of coffee to stay awake late nights.",
        "mentals": "Irritable, impatient, fastidious, anxious about health and work performance, easily angered by contradiction",
        "vitals": "BP: 120/80 mmHg, Pulse: 74 bpm, Temp: 98.4 F",
        "general_exam": "Anxious facies, mild epigastric tenderness on deep palpation, coated tongue (thick white back half)",
        "systemic_exam": "GI: Epigastric tenderness without rebound. Respiratory: Clear. CVS: Normal heart sounds.",
        "local_exam": "No hemorrhoids or fissures visible.",
        "modalities": "Worse: morning upon waking, after eating spicy food, coffee, mental exertion, cold air. Better: warmth, evening, resting quietly",
        "reports": "CBC: Normal, USG Abdomen: Mild fatty liver Grade 1, otherwise normal.",
        "notes": "Classical Nux Vomica constitution. Stress and coffee etiology with ineffectual urging pathognomonic rubric.",
        "appetite": "Good, but feels full quickly; dyspepsia after eating",
        "cravings": "Spicy food, coffee, stimulants, fat, rich pungent food",
        "aversions": "Cold food, milk, meat",
        "thirst": "Moderate, prefers warm drinks",
        "thermal": "Chilly (craves heat and warm covers)",
        "perspiration": "Scanty, mostly on chest and back",
        "stool": "Hard, dry, unsatisfactory; constant ineffectual urging for stool",
        "urine": "Normal frequency, pale amber",
        "sleep": "Disturbed, wakes around 3-4 AM thinking of work difficulties, unrefreshing sleep",
        "sleep_position": "On back or right side",
        "past_history": "Frequent gastric troubles, occasional migraine from stress",
        "vaccination": "Routine vaccinations completed",
        "family_history": "Father has hypertension, mother has osteoarthritis",
        "diet": "Vegetarian, irregular timings",
        "marital_status": "Single",
        "result": {
            "remedy": "Nux Vomica",
            "potency": "200C",
            "dose": "4 pills of 200C, once daily in the morning on an empty stomach for 3 consecutive days, then stop all medicine and observe for 7 to 10 days before follow-up evaluation.",
            "diagnosis": "Gastroesophageal Reflux Disease (GERD) with Dyspepsia and Dyssynergic Constipation in an overworked individual presenting as classical Nux Vomica constitutional picture",
            "rationale": "Under Hahnemannian Organon §153, the selection of Nux Vomica is anchored upon striking, singular, uncommon, and peculiar (characteristic) keynotes: pathognomonic frequent ineffectual urging to stool where small quantities pass with persistent sensation of unexpelled feces; sharp aggravation early in the morning and from mental exertion; marked intolerance and chilliness to cold drafts; distinctive sleep disturbance waking at 3 to 4 AM with business cares; and direct toxic etiology from excessive coffee and sedentary lifestyle. Differentials Lycopodium and Sulphur were ruled out due to opposing modalities and absence of the characteristic ineffectual urging.",
            "remedy_scores": [
                {"remedy": "Nux Vomica", "score": 94, "coverage": "Ineffectual urging (pathognomonic), morning aggravation, irritability/fastidiousness, coffee craving, chilliness, 3 AM waking, workaholic stress", "affinity": "Ineffectual urging (pathognomonic), morning aggravation, irritability/fastidiousness, coffee craving, chilliness, 3 AM waking, workaholic stress"},
                {"remedy": "Lycopodium", "score": 76, "coverage": "Ambitious personality, bloating after small meals, liver/digestive sphere, evening amelioration, irritability—but misses ineffectual urging keynote", "affinity": "Ambitious personality, bloating after small meals, liver/digestive sphere, evening amelioration, irritability—but misses ineffectual urging keynote"},
                {"remedy": "Sulphur", "score": 68, "coverage": "Spicy food craving, morning aggravation, irritability, digestive complaints—but thermal (hot patient) contradicts chilliness here", "affinity": "Spicy food craving, morning aggravation, irritability, digestive complaints—but thermal (hot patient) contradicts chilliness here"},
                {"remedy": "Bryonia", "score": 61, "coverage": "Irritability, constipation picture, amelioration rest—lacks ineffectual urging and coffee craving; constipation type differs (large/dry vs. urging)", "affinity": "Irritability, constipation picture, amelioration rest—lacks ineffectual urging and coffee craving; constipation type differs (large/dry vs. urging)"}
            ],
            "differentials": [
                "Lycopodium (ambitious personality, bloating after small meals, liver/digestive focus, but less morning aggravation and no ineffectual urging keynote)",
                "Sulphur (craving spicy foods, morning aggravation, irritability, but typically hot patient with aversion to warmth—contradicts chilliness here)",
                "Bryonia (irritability, constipation with large dry stools, amelioration rest—but lacks ineffectual urging and coffee craving)"
            ],
            "citations": [
                {"remedy": "Nux Vomica", "source": "Boericke's Materia Medica", "quote": "Frequent ineffectual urging to stool; passes small quantities at each attempt. Feels as if part remained unexpelled. Wants to go constantly.", "text": "Frequent ineffectual urging to stool; passes small quantities at each attempt. Feels as if part remained unexpelled. Wants to go constantly."},
                {"remedy": "Nux Vomica", "source": "Allen's Keynotes", "quote": "Irritable, zealous fiery temperament. Oversensitive; cannot bear noises, odors, light. Worse morning on waking. Chilly, cannot uncover.", "text": "Irritable, zealous fiery temperament. Oversensitive; cannot bear noises, odors, light. Worse morning on waking. Chilly, cannot uncover."},
                {"remedy": "Nux Vomica", "source": "Kent's Lectures on Materia Medica", "quote": "Sleeps into aggravation; wakes 3-4 AM with mind on business, cannot sleep again until toward morning, then heavy sleep and hard to rouse.", "text": "Sleeps into aggravation; wakes 3-4 AM with mind on business, cannot sleep again until toward morning, then heavy sleep and hard to rouse."}
            ]
        }
    },
    {
        "id": "d0af8489-71d9-4c6b-a18f-bd0261beccef",
        "name": "Rohan Patel",
        "age": "32",
        "sex": "Male",
        "occupation": "Software engineer",
        "address": "Ahemdabad",
        "phone": "9638143173",
        "email": "amitravalpunsari@gmail.com",
        "weight": "70",
        "height": "175",
        "complaints": "Severe right-sided acute throat pain and difficulty swallowing. Worse from swallowing saliva or cold drinks. Warm tea provides temporary relief. Sensation of a splinter or fishbone in the throat.",
        "associated_complaints": "Chilliness and mild fever with headache.",
        "history": "",
        "mentals": "Irritable, extremely sensitive to pain, wants to be kept warm.",
        "vitals": "",
        "general_exam": "",
        "systemic_exam": "",
        "local_exam": "",
        "modalities": "Aggravation: Cold air, uncovering, cold drinks, swallowing. Amelioration: Warm drinks, wrapping up head and neck warmly.",
        "reports": "",
        "notes": "",
        "appetite": "",
        "cravings": "",
        "aversions": "",
        "thirst": "Thirst for warm liquids in small quantities",
        "thermal": "Extremely chilly, cannot bear least uncovering",
        "perspiration": "",
        "stool": "",
        "urine": "",
        "sleep": "",
        "sleep_position": "",
        "past_history": "",
        "vaccination": "",
        "family_history": "",
        "diet": "",
        "marital_status": "",
        "upstream_case_id": "82948ef6-3989-40e7-ab84-1b1c2335ded1",
        "result": {
            "remedy": "Hepar Sulphuris Calcareum",
            "potency": "30C",
            "dose": "4 pills every 4 hours for the first day, then thrice daily for 2 days, then reassess. Stop on significant improvement.",
            "diagnosis": "Acute right-sided pharyngitis/tonsillitis with characteristic splinter sensation, marked chilliness, and warm drink amelioration. Likely bacterial pharyngitis requiring close monitoring.",
            "rationale": "The PECULIAR CHARACTERISTIC symptom of a splinter/fishbone sensation in throat is a pathognomonic keynote for Hepar Sulph, carrying primary prescribing weight per Organon §153. The EXTREME CHILLINESS with hypersensitivity to uncovering, cold air, and cold drinks—combined with amelioration from warm applications and warm drinks—forms the characteristic thermal modality cluster unique to Hepar. The HYPERSENSITIVITY TO PAIN with marked irritability completes the triad. Right-sidedness and acute suppurative tendency align perfectly. While Arsenicum Album shares chilliness and warm drink desire, it lacks the splinter sensation and has anxiety/restlessness (absent here). The striking PQR keynotes (splinter sensation, extreme chill-sensitivity, irritability with pain hypersensitivity) decisively indicate Hepar over broader polycrests.",
            "remedy_scores": [
                {
                    "remedy": "Hepar Sulphuris Calcareum",
                    "score": 94,
                    "coverage": "Splinter sensation (pathognomonic), extreme chilliness, warm amelioration, hypersensitivity to pain, irritability, right-sided acute throat inflammation",
                    "affinity": "Splinter sensation (pathognomonic), extreme chilliness, warm amelioration, hypersensitivity to pain, irritability, right-sided acute throat inflammation"
                },
                {
                    "remedy": "Arsenicum Album",
                    "score": 72,
                    "coverage": "Extreme chilliness, warm drinks in sips, burning pains, but missing splinter keynote and shows more anxiety than present",
                    "affinity": "Extreme chilliness, warm drinks in sips, burning pains, but missing splinter keynote and shows more anxiety than present"
                },
                {
                    "remedy": "Nitric Acid",
                    "score": 61,
                    "coverage": "Splinter/fishbone sensation in throat, but thermal relationship opposite (worse warmth, better cold)",
                    "affinity": "Splinter/fishbone sensation in throat, but thermal relationship opposite (worse warmth, better cold)"
                },
                {
                    "remedy": "Lachesis",
                    "score": 48,
                    "coverage": "Throat pain worse swallowing, but LEFT-sided predominance, worse warm drinks, purple discoloration — opposite modalities",
                    "affinity": "Throat pain worse swallowing, but LEFT-sided predominance, worse warm drinks, purple discoloration — opposite modalities"
                }
            ],
            "differentials": [
                "Arsenicum Album — chilliness, thirst for warm sips, but lacks splinter sensation and shows more anxiety/restlessness",
                "Lachesis — left-sided throat complaints worse swallowing liquids, but this is RIGHT-sided and better from warm drinks",
                "Nitric Acid — splinter sensation present but less chilly, worse from warmth"
            ],
            "citations": [
                {
                    "remedy": "Hepar Sulphuris Calcareum",
                    "source": "Boericke's Materia Medica",
                    "quote": "Sensation of splinter or fish-bone in throat. Great sensitiveness to cold air and slightest draft. Cannot bear to be uncovered.",
                    "text": "Sensation of splinter or fish-bone in throat. Great sensitiveness to cold air and slightest draft. Cannot bear to be uncovered."
                },
                {
                    "remedy": "Hepar Sulphuris Calcareum",
                    "source": "Allen's Keynotes",
                    "quote": "Oversensitive physically and mentally. Pains like splinters sticking in parts. Extreme sensitiveness to cold, wants head wrapped up warmly.",
                    "text": "Oversensitive physically and mentally. Pains like splinters sticking in parts. Extreme sensitiveness to cold, wants head wrapped up warmly."
                },
                {
                    "remedy": "Hepar Sulphuris Calcareum",
                    "source": "Kent's Lectures on Materia Medica",
                    "quote": "Hepar patient is the most sensitive of all patients to cold air. Wants warm food and drink. Sensation as if a splinter or fish bone in throat.",
                    "text": "Hepar patient is the most sensitive of all patients to cold air. Wants warm food and drink. Sensation as if a splinter or fish bone in throat."
                },
                {
                    "remedy": "Arsenicum Album",
                    "source": "Boericke's Materia Medica",
                    "quote": "Great thirst for small quantities at short intervals. Cannot bear the sight or smell of food. Great restlessness and anguish. Chilly; worse cold.",
                    "text": "Great thirst for small quantities at short intervals. Cannot bear the sight or smell of food. Great restlessness and anguish. Chilly; worse cold."
                },
                {
                    "remedy": "Nitric Acid",
                    "source": "Nash's Leaders in Homoeopathic Therapeutics",
                    "quote": "Sensation as of a splinter in the throat. Pains appear and disappear suddenly. Very irritable and vindictive.",
                    "text": "Sensation as of a splinter in the throat. Pains appear and disappear suddenly. Very irritable and vindictive."
                }
            ]
        }
    },
    {
        "id": "6cfe14dd-1512-46b6-abee-d17b58702210",
        "name": "Test 25_10",
        "age": "30",
        "sex": "M",
        "occupation": "Teacher",
        "address": "Modasa",
        "phone": "1234567890",
        "email": "test@gmail.com",
        "weight": "68",
        "height": "172",
        "complaints": "Complete painless hoarseness and loss of voice (aphonia) after singing concert yesterday. Constant tickling in larynx provoking dry hacking cough",
        "associated_complaints": "",
        "history": "",
        "mentals": "Anxious about performance, otherwise calm",
        "vitals": "",
        "general_exam": "",
        "systemic_exam": "",
        "local_exam": "",
        "modalities": "Aggravation: Using voice, singing, talking, evening. Amelioration: Sips of cold water, resting vocal cords",
        "reports": "",
        "notes": "",
        "appetite": "",
        "cravings": "",
        "aversions": "",
        "thirst": "Thirst for cold water",
        "thermal": "",
        "perspiration": "",
        "stool": "",
        "urine": "",
        "sleep": "",
        "sleep_position": "",
        "past_history": "",
        "vaccination": "",
        "family_history": "",
        "diet": "",
        "marital_status": "",
        "upstream_case_id": "e8249720-d41e-47ea-be31-f60f414e993b",
        "result": {
            "remedy": "Argentum Metallicum",
            "potency": "30C",
            "dose": "4 pills every 3 hours for 4 doses on day 1, then 4 pills thrice daily for 2 days, reassess on day 3",
            "diagnosis": "Acute laryngitis with complete aphonia following vocal strain (oversinging). Sudden painless loss of voice with laryngeal tickling and reflex dry cough, likely muscular and mucosal irritation of vocal apparatus.",
            "rationale": "This case hinges on STRIKING and PECULIAR symptoms that point away from common laryngitis remedies. The keynote combination of complete painless aphonia (not hoarseness but total loss of voice) after vocal overuse (singing concert), constant laryngeal tickling with dry hacking cough, and amelioration from sips of cold water is characteristic of Argentum Metallicum. The etiology (oversinging in a professional singer/teacher) and the specific modalities (< using voice, evening; > cold water sips, rest) are highly characteristic. While Arum Triphyllum, Causticum, and Phosphorus are common laryngitis remedies, none match the precise cluster of painless total aphonia + tickling + cold water amelioration as precisely as Argentum Metallicum does in classical materia medica. The remedy has specific affinity for vocal cords in professional voice users.",
            "remedy_scores": [
                {
                    "remedy": "Argentum Metallicum",
                    "score": 88,
                    "coverage": "Complete painless aphonia after vocal strain, laryngeal tickling, dry cough, amelioration cold water, professional voice user etiology",
                    "affinity": "Complete painless aphonia after vocal strain, laryngeal tickling, dry cough, amelioration cold water, professional voice user etiology"
                },
                {
                    "remedy": "Arum Triphyllum",
                    "score": 72,
                    "coverage": "Hoarseness from overuse (singers/speakers), laryngeal irritation, but lacks the complete painless aphonia keynote",
                    "affinity": "Hoarseness from overuse (singers/speakers), laryngeal irritation, but lacks the complete painless aphonia keynote"
                },
                {
                    "remedy": "Causticum",
                    "score": 65,
                    "coverage": "Aphonia with laryngeal rawness, but typically gradual paralytic weakness, not acute post-strain onset",
                    "affinity": "Aphonia with laryngeal rawness, but typically gradual paralytic weakness, not acute post-strain onset"
                },
                {
                    "remedy": "Phosphorus",
                    "score": 61,
                    "coverage": "Laryngitis < talking, > cold drinks, but usually has painful burning sensation, not painless aphonia",
                    "affinity": "Laryngitis < talking, > cold drinks, but usually has painful burning sensation, not painless aphonia"
                }
            ],
            "differentials": [
                "Arum Triphyllum — hoarseness from overuse with rawness, but typically with pain and voice changes more than complete aphonia",
                "Causticum — paralytic aphonia with rawness, but usually chronic progressive onset, not sudden after single event",
                "Phosphorus — laryngitis with hoarseness < talking, > cold drinks, but typically with burning pain and more constitutional symptoms"
            ],
            "citations": [
                {
                    "remedy": "Argentum Metallicum",
                    "source": "Clarke's Dictionary of Materia Medica",
                    "quote": "Complete aphonia of singers and public speakers; loss of voice from overuse; larynx feels sore with constant tickling provoking cough",
                    "text": "Complete aphonia of singers and public speakers; loss of voice from overuse; larynx feels sore with constant tickling provoking cough"
                },
                {
                    "remedy": "Argentum Metallicum",
                    "source": "Boericke's Materia Medica",
                    "quote": "Hoarseness and aphonia of professional singers. Cough excited by tickling in the throat-pit. Laughing produces cough with copious mucus",
                    "text": "Hoarseness and aphonia of professional singers. Cough excited by tickling in the throat-pit. Laughing produces cough with copious mucus"
                },
                {
                    "remedy": "Argentum Metallicum",
                    "source": "Allen's Keynotes",
                    "quote": "Great weakness of voice in singers and public speakers; painless hoarseness; rawness in larynx with constant desire to clear throat",
                    "text": "Great weakness of voice in singers and public speakers; painless hoarseness; rawness in larynx with constant desire to clear throat"
                },
                {
                    "remedy": "Arum Triphyllum",
                    "source": "Boericke's Materia Medica",
                    "quote": "Hoarseness; voice uncertain, uncontrollable. Singers and speakers use it for clergyman's sore throat; voice breaks when singing",
                    "text": "Hoarseness; voice uncertain, uncontrollable. Singers and speakers use it for clergyman's sore throat; voice breaks when singing"
                },
                {
                    "remedy": "Phosphorus",
                    "source": "Kent's Lectures on Materia Medica",
                    "quote": "Larynx very painful; rawness and burning. Hoarseness worse evenings, worse talking. Great thirst for cold water which relieves",
                    "text": "Larynx very painful; rawness and burning. Hoarseness worse evenings, worse talking. Great thirst for cold water which relieves"
                }
            ]
        }
    },
    {
        "id": "2ac920c0-c1b6-4c40-8fa2-832c2c99ef3b",
        "name": "Pooja Sharma",
        "age": "29",
        "sex": "F",
        "occupation": "Vocalist",
        "address": "",
        "phone": "",
        "email": "",
        "weight": "",
        "height": "",
        "complaints": "Complete painless hoarseness and loss of voice (aphonia) after singing concert yesterday. Constant tickling in larynx provoking dry hacking cough",
        "associated_complaints": "",
        "history": "",
        "mentals": "Anxious about performance, otherwise calm",
        "vitals": "",
        "general_exam": "",
        "systemic_exam": "",
        "local_exam": "",
        "modalities": "Aggravation: Using voice, singing, talking, evening. Amelioration: Sips of cold water, resting vocal cords",
        "reports": "",
        "notes": "",
        "appetite": "",
        "cravings": "",
        "aversions": "",
        "thirst": "Thirst for cold water",
        "thermal": "",
        "perspiration": "",
        "stool": "",
        "urine": "",
        "sleep": "",
        "sleep_position": "",
        "past_history": "",
        "vaccination": "",
        "family_history": "",
        "diet": "",
        "marital_status": "",
        "upstream_case_id": "b8f0f990-330d-447f-80a9-18d0259be352",
        "result": {
            "remedy": "Arum Triphyllum",
            "potency": "30C",
            "dose": "4 pills every 3-4 hours while awake for 2 days, then reassess. Stop on improvement.",
            "diagnosis": "Acute aphonia (complete painless hoarseness with loss of voice) following vocal strain from singing concert, with laryngeal tickling and dry cough. Probable acute laryngitis from overuse of vocal cords.",
            "rationale": "This case presents STRIKING, CHARACTERISTIC symptoms of a vocal professional with COMPLETE PAINLESS aphonia after singing concert — a precise etiology (overuse of voice) with a rare keynote (total voice loss without pain). Arum Triphyllum is THE specific remedy for hoarseness and aphonia in singers, speakers, and clergymen from vocal overuse (Allen, Boericke, Clarke all emphasize this). The PECULIAR modality — amelioration from sips of cold water — is a strong confirming keynote for Arum-t (craves cold drinks despite sore throat, voice improves temporarily with cold sips). Constant laryngeal tickling with dry hacking cough fits Arum-t's irritative laryngeal picture. The aggravation from talking/using voice and amelioration from resting vocal cords are pathognomonic for voice-strain remedies, but Arum-t's PAINLESS aphonia (vs. Rhus-t's painful hoarseness, Causticum's paralytic weakness) and the cold water amelioration are PRESCRIBING-WEIGHT peculiarities that override consideration of broader polycrests. This is a textbook Arum Triphyllum acute prescription based on etiology + PQR keynotes.",
            "remedy_scores": [
                {
                    "remedy": "Arum Triphyllum",
                    "score": 94,
                    "coverage": "Painless aphonia from vocal overuse (PQR etiology), amelioration cold water sips (rare modality), laryngeal tickling, dry cough, singer/speaker keynote",
                    "affinity": "Painless aphonia from vocal overuse (PQR etiology), amelioration cold water sips (rare modality), laryngeal tickling, dry cough, singer/speaker keynote"
                },
                {
                    "remedy": "Rhus Toxicodendron",
                    "score": 68,
                    "coverage": "Hoarseness from overuse/strain, worse beginning to speak, but lacks painless quality and cold water amelioration",
                    "affinity": "Hoarseness from overuse/strain, worse beginning to speak, but lacks painless quality and cold water amelioration"
                },
                {
                    "remedy": "Causticum",
                    "score": 62,
                    "coverage": "Aphonia/paralytic voice weakness, chronic in singers, but worse cold air, lacks sudden onset and cold water modality",
                    "affinity": "Aphonia/paralytic voice weakness, chronic in singers, but worse cold air, lacks sudden onset and cold water modality"
                },
                {
                    "remedy": "Argentum Metallicum",
                    "score": 58,
                    "coverage": "Chronic hoarseness in singers/speakers, worse singing, but more gradual, with rawness/soreness lacking here",
                    "affinity": "Chronic hoarseness in singers/speakers, worse singing, but more gradual, with rawness/soreness lacking here"
                }
            ],
            "differentials": [
                "Rhus Toxicodendron — hoarseness from overuse, but typically PAINFUL on first speaking with amelioration from continued use",
                "Causticum — paralytic aphonia, progressive weakness of voice, worse cold air, but lacks the cold water amelioration keynote",
                "Argentum Metallicum — chronic aphonia in professional singers, worse singing, but more gradual onset and sore/raw sensation"
            ],
            "citations": [
                {
                    "remedy": "Arum Triphyllum",
                    "source": "Boericke's Materia Medica",
                    "quote": "Hoarseness of singers; COMPLETE aphonia from overuse of voice. Voice uncertain, uncontrollable. Amelioration from cold drinks.",
                    "text": "Hoarseness of singers; COMPLETE aphonia from overuse of voice. Voice uncertain, uncontrollable. Amelioration from cold drinks."
                },
                {
                    "remedy": "Arum Triphyllum",
                    "source": "Allen's Keynotes",
                    "quote": "Hoarseness; VOICE ENTIRELY LOST from overuse (singers, speakers). Tickling in larynx. Craves cold water which relieves momentarily.",
                    "text": "Hoarseness; VOICE ENTIRELY LOST from overuse (singers, speakers). Tickling in larynx. Craves cold water which relieves momentarily."
                },
                {
                    "remedy": "Arum Triphyllum",
                    "source": "Clarke's Dictionary of Materia Medica",
                    "quote": "Aphonia of professional vocalists after prolonged use of voice. Cannot control pitch. Laryngeal irritation with dry cough.",
                    "text": "Aphonia of professional vocalists after prolonged use of voice. Cannot control pitch. Laryngeal irritation with dry cough."
                },
                {
                    "remedy": "Rhus Toxicodendron",
                    "source": "Boericke's Materia Medica",
                    "quote": "Hoarseness from overuse of voice; PAINFUL on beginning to speak, better continued speaking. Worse cold air, damp.",
                    "text": "Hoarseness from overuse of voice; PAINFUL on beginning to speak, better continued speaking. Worse cold air, damp."
                },
                {
                    "remedy": "Causticum",
                    "source": "Kent's Lectures on Materia Medica",
                    "quote": "Paralytic weakness of vocal cords. Aphonia. Hoarseness worse morning, worse cold dry air. Chronic in singers and public speakers.",
                    "text": "Paralytic weakness of vocal cords. Aphonia. Hoarseness worse morning, worse cold dry air. Chronic in singers and public speakers."
                }
            ]
        }
    },
    {
        "id": "44e32df7-5954-4589-9a1e-f40c8ed4b85d",
        "name": "Ramesh Gupta",
        "age": "45",
        "sex": "Male",
        "occupation": "Accountant",
        "address": "Ahmedabad, Gujarat",
        "phone": "+91 9876543212",
        "email": "ramesh.gupta@example.com",
        "weight": "72",
        "height": "170",
        "complaints": "Acute severe right knee pain and swelling since 2 days. Stitching, tearing pain in knee joint. Knee is swollen, hot, and tender to touch.",
        "associated_complaints": "Severe dry mouth and lips. Constipation with dry, hard, dark stools as if burnt.",
        "history": "Pain started suddenly after physical exertion and catching a chill while walking in cold air.",
        "mentals": "Extremely irritable, easily angered, desires to be left alone in silence. Constantly thinking and anxious about business and financial affairs.",
        "vitals": "",
        "general_exam": "",
        "systemic_exam": "",
        "local_exam": "",
        "modalities": "Worse from the slightest movement or motion, worse walking, worse warmth; Better from absolute rest, firm pressure, and lying on the painful right side.",
        "reports": "",
        "notes": "",
        "appetite": "Poor appetite, bitter taste in mouth.",
        "cravings": "",
        "aversions": "",
        "thirst": "Excessive thirst for large draughts of cold water at long intervals.",
        "thermal": "Chilly, but aggravated by warmth of room; wants fresh cool air.",
        "perspiration": "Oily perspiration on slight exertion, sour smelling.",
        "stool": "",
        "urine": "",
        "sleep": "Restless due to knee pain, can only rest when lying still on the right side.",
        "sleep_position": "",
        "past_history": "",
        "vaccination": "",
        "family_history": "",
        "diet": "Vegetarian",
        "marital_status": "Married",
        "upstream_case_id": "44e32df7-5954-4589-9a1e-f40c8ed4b85d",
        "result": {
            "remedy": "Bryonia Alba",
            "potency": "200C",
            "dose": "4 pills, three times daily for 2 days, then stop and observe for 3-5 days before reassessing",
            "diagnosis": "Acute inflammatory arthritis of the right knee joint, likely traumatic synovitis with reactive inflammation, triggered by physical exertion and cold exposure. Accompanied by systemic dryness (mucous membranes, stool) and marked irritability.",
            "rationale": "This case exemplifies the Bryonia picture with STRIKING CHARACTERISTIC symptoms that carry the highest prescribing weight. The keynote triad is unmistakable: (1) AGGRAVATION FROM SLIGHTEST MOTION with amelioration from absolute rest and firm pressure — the pathognomonic Bryonia modality; (2) amelioration lying on the PAINFUL SIDE (right knee), a rare and peculiar symptom characteristic of Bryonia's desire for pressure on inflamed parts; (3) DRYNESS as a pervading feature (dry mouth, lips, hard dark burnt stools). The mental picture of business anxiety, irritability wanting solitude, the thirst for large quantities at long intervals, the stitching tearing pains in swollen hot joints, and the acute onset after exertion plus cold air exposure all confirm Bryonia as the simillimum. While Rhus Tox covers joint complaints worse motion, it ameliorates from CONTINUED motion and is worse at rest (opposite modality). The PECULIAR symptom of lying on the painful side for relief is the decisive differentiating keynote that elevates Bryonia above all polycrests.",
            "remedy_scores": [
                {
                    "remedy": "Bryonia Alba",
                    "score": 94,
                    "coverage": "Covers all PQR symptoms: aggravation slightest motion, amelioration lying on painful side, systemic dryness, business anxiety, large thirst long intervals",
                    "affinity": "Covers all PQR symptoms: aggravation slightest motion, amelioration lying on painful side, systemic dryness, business anxiety, large thirst long intervals"
                },
                {
                    "remedy": "Rhus Toxicodendron",
                    "score": 68,
                    "coverage": "Covers joint pain worse cold, restlessness, but FAILS the motion modality (opposite pattern) and lacks dryness keynotes",
                    "affinity": "Covers joint pain worse cold, restlessness, but FAILS the motion modality (opposite pattern) and lacks dryness keynotes"
                },
                {
                    "remedy": "Belladonna",
                    "score": 58,
                    "coverage": "Covers acute hot swollen joint, irritability, sudden onset, but lacks the dryness constellation and characteristic motion/rest modality",
                    "affinity": "Covers acute hot swollen joint, irritability, sudden onset, but lacks the dryness constellation and characteristic motion/rest modality"
                },
                {
                    "remedy": "Colchicum",
                    "score": 52,
                    "coverage": "Covers knee joint inflammation and irritability, but lacks the Bryonia motion modality and dryness; different gastric symptoms",
                    "affinity": "Covers knee joint inflammation and irritability, but lacks the Bryonia motion modality and dryness; different gastric symptoms"
                }
            ],
            "differentials": [
                "Rhus Toxicodendron — joint stiffness worse initial motion but better continued motion, opposite rest modality",
                "Belladonna — acute hot red swelling with throbbing, but lacks dryness keynotes and motion aggravation pattern",
                "Colchicum — joint inflammation especially knee, but with extreme nausea from smell of food and different modalities"
            ],
            "citations": [
                {
                    "remedy": "Bryonia Alba",
                    "source": "Boericke's Materia Medica",
                    "quote": "Excessive dryness of mucous membranes; worse from any motion; ameliorated by absolute rest. Lies on painful side to relieve pain through pressure.",
                    "text": "Excessive dryness of mucous membranes; worse from any motion; ameliorated by absolute rest. Lies on painful side to relieve pain through pressure."
                },
                {
                    "remedy": "Bryonia Alba",
                    "source": "Allen's Keynotes",
                    "quote": "Great dryness of all mucous membranes. Stitching pains worse from least motion. Desires to be quiet; irritable. Thirst for large quantities at long intervals.",
                    "text": "Great dryness of all mucous membranes. Stitching pains worse from least motion. Desires to be quiet; irritable. Thirst for large quantities at long intervals."
                },
                {
                    "remedy": "Bryonia Alba",
                    "source": "Kent's Lectures on Materia Medica",
                    "quote": "All complaints are made worse from motion and better from rest. Lies on the painful side. Anxious about business affairs. Hard, dry, as if burnt stools.",
                    "text": "All complaints are made worse from motion and better from rest. Lies on the painful side. Anxious about business affairs. Hard, dry, as if burnt stools."
                },
                {
                    "remedy": "Rhus Toxicodendron",
                    "source": "Boericke's Materia Medica",
                    "quote": "Ailments from strains, overlifting, cold exposure. Great restlessness; worse initial motion, better continued motion. Stiffness ameliorated by movement.",
                    "text": "Ailments from strains, overlifting, cold exposure. Great restlessness; worse initial motion, better continued motion. Stiffness ameliorated by movement."
                },
                {
                    "remedy": "Belladonna",
                    "source": "Nash's Leaders in Homoeopathic Therapeutics",
                    "quote": "Sudden violent onset. Parts affected are red, hot, swollen, throbbing. Great heat with burning. Worse from jar, motion, light, noise.",
                    "text": "Sudden violent onset. Parts affected are red, hot, swollen, throbbing. Great heat with burning. Worse from jar, motion, light, noise."
                }
            ],
            "lifestyle": {
                "diet_do": [
                    "Warm cooked vegetable soups and dal to support digestion and hydration",
                    "Warm water with lemon first thing in morning for constipation",
                    "Fresh seasonal fruits soaked or stewed (prunes, figs) for bowel regularity",
                    "Well-cooked whole grains (brown rice, oats) with ghee for lubrication",
                    "Small frequent meals rather than large heavy meals given poor appetite"
                ],
                "diet_avoid": [
                    "Cold water and iced drinks which aggravate (despite thirst, take water at room temperature)",
                    "Dry, rough, hard-to-digest foods (dry crackers, chips, roasted nuts)",
                    "Refined sugar and white flour products which increase dryness",
                    "Spicy hot foods which increase irritability and heat",
                    "Coffee and strong tea (may antidote Bryonia and worsen dryness)"
                ],
                "exercises": [
                    "ABSOLUTE REST of the right knee for next 3-5 days — no weight bearing exercises",
                    "After acute phase subsides, gentle passive range-of-motion exercises lying down",
                    "Deep breathing exercises (pranayama) to calm mental irritability, 10 min twice daily",
                    "Avoid walking, jogging, squatting, climbing stairs until pain fully resolves",
                    "Later: gradual return to gentle walks on level ground, maximum 10-15 minutes initially"
                ],
                "lifestyle": [
                    "Complete mental and physical rest for 3-5 days; minimize business worries and paperwork",
                    "Sleep by 10 pm in a cool, well-ventilated room (avoid stuffy warm room)",
                    "Apply firm compression bandage to knee for comfort (Bryonia loves pressure)",
                    "Avoid coffee and camphor which antidote the remedy; no topical analgesic balms during treatment",
                    "Keep hydrated but drink room-temperature water, not cold (large amounts at intervals as body demands)",
                    "Maintain silence and solitude when irritable; avoid unnecessary social interactions for recovery"
                ]
            }
        }
    }
]

def seed(conn=None):
    close_after = False
    if conn is None:
        conn = sqlite3.connect('primeheal.db')
        close_after = True
    cursor = conn.cursor()

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    for item in GOLDEN_CASES:
        c_id = item["id"]
        # Delete any existing case with similar name or ID to avoid duplicates
        cursor.execute("DELETE FROM cases WHERE id = ? OR patient_name = ?", (c_id, item["name"]))
        
        raw_case = {k: v for k, v in item.items() if k not in ("result", "upstream_case_id")}
        result_obj = item["result"]
        up_id = item.get("upstream_case_id")

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
            c_id,
            item["name"],
            item["age"],
            item["sex"],
            item["occupation"],
            item["address"],
            item["phone"],
            item["email"],
            item["weight"],
            item["height"],
            item["complaints"],
            item["associated_complaints"],
            item["history"],
            item["mentals"],
            item["vitals"],
            item["general_exam"],
            item["systemic_exam"],
            item["local_exam"],
            item["modalities"],
            item["reports"],
            item["notes"],
            item["appetite"],
            item["cravings"],
            item["aversions"],
            item["thirst"],
            item["thermal"],
            item["perspiration"],
            item["stool"],
            item["urine"],
            item["sleep"],
            item["sleep_position"],
            item["past_history"],
            item["vaccination"],
            item["family_history"],
            item["diet"],
            item["marital_status"],
            json.dumps(raw_case),
            json.dumps(result_obj),
            None,
            0,
            now,
            now
        ))
        if up_id:
            try:
                cursor.execute("UPDATE cases SET upstream_case_id = ? WHERE id = ?", (up_id, c_id))
            except Exception:
                pass

    conn.commit()
    print(f"[Seed] Successfully seeded {len(GOLDEN_CASES)} golden reference cases into database!")
    if close_after:
        conn.close()

if __name__ == '__main__':
    seed()
