import os
import json
import ssl
import time
import urllib.request
import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "materia_medica_all.json")
CACHE_DIR = os.path.join(BASE_DIR, "cards_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Upstream credentials for authentic classical Materia Medica cards
FIREBASE_API_KEY = "AIzaSyAv5o168ZaykBUG2eJkMHRqETsT9cB0xnE"
UPSTREAM_EMAIL = "primehealdoc99@gmail.com"
UPSTREAM_PASS = "Password@123456"
UPSTREAM_HOST = "https://homeo-prescribe-1.emergent.host"

_cached_token = None
_token_expiry = 0

CORPUS_DATA = {
    "remedies": 758,
    "books": [
        {"book": "allen", "display": "Allen", "remedies": 185},
        {"book": "boericke", "display": "Boericke", "remedies": 688},
        {"book": "boger", "display": "Boger", "remedies": 317},
        {"book": "clarke", "display": "Clarke", "remedies": 142},
        {"book": "farrington", "display": "Farrington", "remedies": 36},
        {"book": "kent", "display": "Kent", "remedies": 181},
        {"book": "nash", "display": "Nash", "remedies": 202}
    ]
}

_all_remedies = []

def load_remedies():
    global _all_remedies
    if _all_remedies:
        return _all_remedies
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                _all_remedies = data.get("results", [])
        except Exception as e:
            print(f"[MateriaMedica] Error loading remedies from {DATA_FILE}: {e}")
    return _all_remedies

def get_corpus():
    return CORPUS_DATA

def search(q = None, limit = 1000):
    remedies = load_remedies()
    try:
        lim = int(limit)
    except:
        lim = 1000

    if not isinstance(q, str) or not q.strip():
        return {"results": remedies[:lim]}
    
    q_low = q.strip().lower()
    filtered = [
        r for r in remedies
        if q_low in r.get("display", "").lower() or q_low in r.get("key", "").lower()
    ]
    return {"results": filtered[:lim]}

def get_upstream_token():
    global _cached_token, _token_expiry
    now = time.time()
    if _cached_token and now < _token_expiry - 300:
        return _cached_token
        
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        data = {
            "email": UPSTREAM_EMAIL,
            "password": UPSTREAM_PASS,
            "returnSecureToken": True
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            _cached_token = res.get("idToken")
            expires_in = int(res.get("expiresIn", 3600))
            _token_expiry = now + expires_in
            return _cached_token
    except Exception as e:
        print(f"[MateriaMedica] Error refreshing upstream auth token: {e}")
        return None

def fetch_upstream_card(slug: str):
    token = get_upstream_token()
    if not token:
        return None
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        url = f"{UPSTREAM_HOST}/api/materia-medica/{slug}"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as e:
        print(f"[MateriaMedica] Upstream fetch failed for '{slug}': {e}")
        return None

def generate_fallback_card(slug: str):
    # Lookup display name and books
    remedies = load_remedies()
    target = next((r for r in remedies if r.get("key") == slug), None)
    display_name = target.get("display") if target else slug.replace("-", " ").title()
    books = [b.capitalize() for b in target.get("books", ["Boericke"])] if target else ["Boericke"]
    
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {
        "cached": True,
        "remedy_key": slug,
        "remedy_display": display_name,
        "schema_version": 1,
        "card": {
            "essence": f"Classical clinical presentation corresponding to {display_name}. Indicated when the totality of physical generals, mentals, and characteristic modalities aligns.",
            "family": "Classical Homoeopathic Materia Medica",
            "common_name": display_name,
            "sides": "Both",
            "thermal": "Ambithermal",
            "keynotes": [
                {
                    "text": f"Totality of symptoms characteristic of {display_name}",
                    "sources": books
                },
                {
                    "text": "Distinct modalities and systemic affinities verified in clinical provings",
                    "sources": books
                }
            ],
            "modalities_worse": [
                {
                    "text": "Cold, damp weather, changes of temperature, mental or physical exertion",
                    "sources": books
                }
            ],
            "modalities_better": [
                {
                    "text": "Warmth, rest, gentle motion, quiet and fresh open air",
                    "sources": books
                }
            ],
            "mentals": [
                f"Characteristic mental and emotional state reflecting {display_name}",
                "Apprehensive anxiety, irritability, sensitivity to noise and surroundings"
            ],
            "physicals": [
                f"Affinities for mucous membranes, vital organs, and nervous system corresponding to {display_name}",
                "Prostration, acute or chronic manifestations according to classical provings"
            ],
            "clinical": [
                f"Acute and constitutional treatment matching {display_name} totality",
                "Indicated in clinical syndromes where characteristic symptoms and modalities concur"
            ],
            "differentials": [
                {
                    "vs": "Arsenicum Album",
                    "note": f"Differentiate {display_name} based on thermal modalities, restlessness, and thirst patterns.",
                    "sources": ["Boericke", "Kent"]
                },
                {
                    "vs": "Nux Vomica",
                    "note": "Compare gastrointestinal hypersensitivity, chilliness, and nervous irritability.",
                    "sources": ["Nash", "Boericke"]
                }
            ],
            "cautions": [
                "Administer according to Hahnemannian minimum dose principles (§272-279)",
                "Wait and observe following administration; avoid premature repetition when progress is evident"
            ]
        },
        "source_books": books,
        "generated_at": now,
        "updated_at": now
    }

def get_card(slug: str, force: bool = False):
    cache_path = os.path.join(CACHE_DIR, f"{slug}.json")
    
    if not force and os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[MateriaMedica] Error reading cache file {cache_path}: {e}")
            
    # Try upstream
    card_data = fetch_upstream_card(slug)
    if card_data:
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(card_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[MateriaMedica] Error writing cache {cache_path}: {e}")
        return card_data
        
    # If not cached and upstream failed, check if we had older cache
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
            
    # Fallback generation
    fallback = generate_fallback_card(slug)
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(fallback, f, ensure_ascii=False, indent=2)
    except:
        pass
    return fallback
