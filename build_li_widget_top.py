import json, os

data_path = r"C:\Users\mujta\OneDrive\Documents\Crypto\Robot Work\chief-of-staff\pst-extract\li_widget_data.json"
out_path  = r"C:\Users\mujta\OneDrive\Documents\Crypto\Robot Work\chief-of-staff\pst-extract\li_top.json"

with open(data_path, encoding="utf-8") as f:
    data = json.load(f)

# Top 200 most recent, compact keys
def compress(r):
    return [r["n"][:40], r["co"][:40], r["p"][:50], r["cat"], r["dt"], r["u"]]

top = [compress(r) for r in data[:200]]
raw = json.dumps(top, ensure_ascii=False, separators=(',',':'))
print(f"Top 200 contacts, {len(raw)} chars")

with open(out_path, "w", encoding="utf-8") as f:
    f.write(raw)
