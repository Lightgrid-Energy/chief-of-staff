import json, os

data_path = r"C:\Users\mujta\OneDrive\Documents\Crypto\Robot Work\chief-of-staff\pst-extract\li_widget_data.json"
out_path  = r"C:\Users\mujta\OneDrive\Documents\Crypto\Robot Work\chief-of-staff\pst-extract\li_compact.html"

with open(data_path, encoding="utf-8") as f:
    data = json.load(f)

# Compact each record further - shorten long strings
def compress(r):
    return {
        "n": r["n"][:45],
        "co": r["co"][:45],
        "p": r["p"][:55],
        "cat": r["cat"],
        "dt": r["dt"],
        "u": r["u"]
    }

compact = [compress(r) for r in data]
raw = json.dumps(compact, ensure_ascii=False, separators=(',', ':'))

template = '''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0f1117;color:#e2e8f0;font-size:13px}
.hd{padding:14px 16px 10px;border-bottom:1px solid #1e2a3a;background:#0f1117;position:sticky;top:0;z-index:10}
h1{font-size:14px;font-weight:700;color:#7dd3fc;margin-bottom:8px}
.ctrl{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
input{flex:1;min-width:160px;padding:5px 9px;background:#1a2332;border:1px solid #2d3f55;border-radius:6px;color:#e2e8f0;font-size:12px;outline:none}
input:focus{border-color:#38bdf8}
select{padding:5px 9px;background:#1a2332;border:1px solid #2d3f55;border-radius:6px;color:#e2e8f0;font-size:12px;outline:none;cursor:pointer}
.cnt{font-size:11px;color:#64748b;white-space:nowrap;margin-left:auto}
table{width:100%;border-collapse:collapse}
thead th{background:#111827;padding:7px 10px;text-align:left;font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid #1e2a3a}
tbody tr{border-bottom:1px solid #1a2332}
tbody tr:hover{background:#1a2332}
td{padding:6px 10px;vertical-align:middle}
td.i{color:#64748b;font-size:11px;width:36px;text-align:right}
td.nm a{color:#e2e8f0;text-decoration:none;font-weight:500}
td.nm a:hover{color:#38bdf8}
td.co{color:#94a3b8;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
td.ro{color:#64748b;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:11px}
td.dt{color:#64748b;font-size:11px;white-space:nowrap}
.b{display:inline-block;padding:2px 6px;border-radius:10px;font-size:10px;font-weight:600}
.bI{background:#1e3a5f;color:#7dd3fc}
.bE{background:#064e3b;color:#6ee7b7}
.bA{background:#2e1065;color:#c4b5fd}
.bR{background:#14532d;color:#86efac}
.bG{background:#78350f;color:#fcd34d}
.bC{background:#312e81;color:#a5b4fc}
.bF{background:#1f2937;color:#9ca3af}
.bL{background:#450a0a;color:#fca5a5}
.bO{background:#1a2332;color:#64748b}
.empty{text-align:center;color:#374151;padding:40px;font-size:14px}
</style>
</head>
<body>
<div class="hd">
  <h1>LinkedIn Connections &mdash; {count} contacts (most recent first)</h1>
  <div class="ctrl">
    <input type="search" id="q" placeholder="Search name, company, role..." oninput="render()">
    <select id="cat" onchange="render()">
      <option value="">All categories</option>
      <option value="Investor">Investor</option>
      <option value="Energy / Cleantech">Energy / Cleantech</option>
      <option value="AI / Tech">AI / Tech</option>
      <option value="Academic / Research">Academic / Research</option>
      <option value="Government">Government</option>
      <option value="Accelerator / Ecosystem">Accelerator / Ecosystem</option>
      <option value="Finance / Banking">Finance / Banking</option>
      <option value="Legal">Legal</option>
      <option value="Industry / Other">Industry / Other</option>
    </select>
    <span class="cnt" id="cnt"></span>
  </div>
</div>
<table>
  <thead><tr><th style="width:36px">#</th><th>Name</th><th>Company</th><th>Role</th><th>Category</th><th>Connected</th></tr></thead>
  <tbody id="tb"></tbody>
</table>
<script>
const D={DATA};
const BC={{
  'Investor':'bI','Energy / Cleantech':'bE','AI / Tech':'bA',
  'Academic / Research':'bR','Government':'bG','Accelerator / Ecosystem':'bC',
  'Finance / Banking':'bF','Legal':'bL','Industry / Other':'bO'
}};
function render(){{
  const q=document.getElementById('q').value.toLowerCase();
  const c=document.getElementById('cat').value;
  let r=D;
  if(q) r=r.filter(x=>(x.n+x.co+x.p).toLowerCase().includes(q));
  if(c) r=r.filter(x=>x.cat===c);
  document.getElementById('cnt').textContent=r.length+'/'+D.length;
  const tb=document.getElementById('tb');
  if(!r.length){{tb.innerHTML='<tr><td colspan="6" class="empty">No matches</td></tr>';return;}}
  tb.innerHTML=r.map((x,i)=>`<tr>
    <td class="i">${{i+1}}</td>
    <td class="nm"><a href="${{x.u}}" target="_blank">${{x.n}}</a></td>
    <td class="co" title="${{x.co}}">${{x.co}}</td>
    <td class="ro" title="${{x.p}}">${{x.p}}</td>
    <td><span class="b ${{BC[x.cat]||'bO'}}">${{x.cat}}</span></td>
    <td class="dt">${{x.dt}}</td>
  </tr>`).join('');
}}
render();
</script>
</body></html>'''

html = template.replace('{DATA}', raw).replace('{count}', str(len(data)))
# Fix template literals - they use {{ and }} for escaping in Python format strings

with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

size = os.path.getsize(out_path)
print(f"Done. {len(data)} contacts, {size:,} bytes")
