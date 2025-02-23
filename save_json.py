import json

with open("collected_pages.json", "r", encoding="utf-8") as f:
    collected_pages = json.load(f)

print(f"✅ Loaded {len(collected_pages)} pages from file.")
