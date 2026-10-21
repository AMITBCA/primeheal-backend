import urllib.request
import json

base = "http://127.0.0.1:8000"

def test_endpoint(url, method="GET", body=None):
    req = urllib.request.Request(url, method=method)
    if body:
        data = json.dumps(body).encode("utf-8")
        req.data = data
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode("utf-8")
            return resp.status, json.loads(content) if "{" in content else content
    except Exception as e:
        return 500, str(e)

print("1. Testing /api/auth/me:")
s, r = test_endpoint(f"{base}/api/auth/me")
print(f"Status {s}: is_admin={r.get('is_admin')}, plan={r.get('plan')}, unlimited={r.get('usage', {}).get('unlimited')}")

print("\n2. Testing /api/plans:")
s, r = test_endpoint(f"{base}/api/plans")
print(f"Status {s}: plans count = {len(r.get('plans', []))}")
for p in r.get('plans', []):
    print(f"   Plan: {p['name']}, Price: {p['price_inr']}, Limits: {p['limits']}")

print("\n3. Testing /api/cases (Creating a test homeopathic case):")
test_case = {
    "patient_name": "Ramesh Kumar",
    "age": "45",
    "sex": "Male",
    "occupation": "Shopkeeper",
    "complaints": "Severe dry painful cough, worse from least motion, wants to hold chest while coughing. Constant thirst for large quantities of cold water.",
    "associated_complaints": "Headache over right eye, worse by walking or stooping.",
    "mentals": "Irritable, dislikes being spoken to, worries about financial affairs.",
    "modalities": "Worse from motion, morning, heat; better from absolute rest and pressure."
}
s, created = test_endpoint(f"{base}/api/cases", method="POST", body=test_case)
print(f"Status {s}: Case ID = {created.get('id')}")
print(f"   Similimum Remedy: {created.get('result', {}).get('remedy')} {created.get('result', {}).get('potency')}")
print(f"   Dose: {created.get('result', {}).get('dose')}")
print(f"   Rationale: {created.get('result', {}).get('rationale')[:120]}...")

print("\n4. Testing /api/chat/general (Ask AI):")
s, chat_res = test_endpoint(f"{base}/api/chat/general", method="POST", body={"message": "What is the difference between Bryonia and Rhus tox in joint pain?"})
print(f"Status {s}: AI Reply = {chat_res.get('reply')[:120]}...")

print("\n5. Testing /api/materia-medica/corpus:")
s, corpus = test_endpoint(f"{base}/api/materia-medica/corpus")
print(f"Status {s}: remedies = {corpus.get('remedies')}, books count = {len(corpus.get('books', []))}")
for b in corpus.get('books', []):
    print(f"   Source: {b.get('display')} ({b.get('remedies')} remedies)")

print("\n6. Testing /api/materia-medica (All 758 remedies & search):")
s, mm_all = test_endpoint(f"{base}/api/materia-medica")
print(f"Status {s}: Total remedies in Materia Medica = {len(mm_all.get('results', []))}")

s, mm_search = test_endpoint(f"{base}/api/materia-medica?q=arsenicum")
print(f"Status {s}: Search 'arsenicum' found = {len(mm_search.get('results', []))}")

print("\n7. Testing /api/materia-medica/arsenicum-album (Card Detail):")
s, card = test_endpoint(f"{base}/api/materia-medica/arsenicum-album")
print(f"Status {s}: Remedy = {card.get('remedy_display')}")
print(f"   Common name: {card.get('card', {}).get('common_name')}")
print(f"   Thermal: {card.get('card', {}).get('thermal')}, Sides: {card.get('card', {}).get('sides')}")
print(f"   Essence: {card.get('card', {}).get('essence')[:100]}...")
print(f"   Keynotes count: {len(card.get('card', {}).get('keynotes', []))}")
