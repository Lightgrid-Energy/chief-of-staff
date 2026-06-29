import json, os

data_path = r"C:\Users\mujta\OneDrive\Documents\Crypto\Robot Work\chief-of-staff\pst-extract\li_widget_data.json"
out_path  = r"C:\Users\mujta\OneDrive\Documents\Crypto\Robot Work\chief-of-staff\pst-extract\li_widget.html"

with open(data_path, encoding="utf-8") as f:
    raw = f.read().strip()

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; font-size: 13px; }}
  .header {{ padding: 16px 20px 12px; border-bottom: 1px solid #1e2a3a; background: #0f1117; position: sticky; top: 0; z-index: 10; }}
  h1 {{ font-size: 15px; font-weight: 700; color: #7dd3fc; margin-bottom: 10px; letter-spacing: 0.02em; }}
  .controls {{ display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }}
  input[type=search] {{ flex: 1; min-width: 180px; padding: 6px 10px; background: #1a2332; border: 1px solid #2d3f55; border-radius: 6px; color: #e2e8f0; font-size: 12px; outline: none; }}
  input[type=search]:focus {{ border-color: #38bdf8; }}
  select {{ padding: 6px 10px; background: #1a2332; border: 1px solid #2d3f55; border-radius: 6px; color: #e2e8f0; font-size: 12px; outline: none; cursor: pointer; }}
  .count {{ font-size: 11px; color: #64748b; white-space: nowrap; margin-left: auto; }}
  table {{ width: 100%; border-collapse: collapse; }}
  thead th {{ position: sticky; top: 0; background: #111827; padding: 8px 12px; text-align: left; font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #1e2a3a; }}
  tbody tr {{ border-bottom: 1px solid #1a2332; transition: background 0.1s; }}
  tbody tr:hover {{ background: #1a2332; }}
  td {{ padding: 7px 12px; vertical-align: middle; }}
  td.num {{ color: #64748b; font-size: 11px; width: 40px; text-align: right; }}
  td.name a {{ color: #e2e8f0; text-decoration: none; font-weight: 500; }}
  td.name a:hover {{ color: #38bdf8; }}
  td.company {{ color: #94a3b8; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  td.position {{ color: #64748b; max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 11px; }}
  td.date {{ color: #64748b; font-size: 11px; white-space: nowrap; }}
  .badge {{ display: inline-block; padding: 2px 7px; border-radius: 10px; font-size: 10px; font-weight: 600; letter-spacing: 0.03em; }}
  .badge-Investor {{ background: #1e3a5f; color: #7dd3fc; }}
  .badge-Energy {{ background: #064e3b; color: #6ee7b7; }}
  .badge-AI {{ background: #2e1065; color: #c4b5fd; }}
  .badge-Academic {{ background: #14532d; color: #86efac; }}
  .badge-Government {{ background: #78350f; color: #fcd34d; }}
  .badge-Accelerator {{ background: #312e81; color: #a5b4fc; }}
  .badge-Finance {{ background: #1f2937; color: #9ca3af; }}
  .badge-Legal {{ background: #450a0a; color: #fca5a5; }}
  .badge-Other {{ background: #1f2937; color: #6b7280; }}
  .badge-Industry {{ background: #1a2332; color: #64748b; }}
  .empty {{ text-align: center; color: #374151; padding: 40px; font-size: 14px; }}
</style>
</head>
<body>
<div class="header">
  <h1>LinkedIn Connections — {len(json.loads(raw))} contacts</h1>
  <div class="controls">
    <input type="search" id="q" placeholder="Search name, company, role..." oninput="render()">
    <select id="cat" onchange="render()">
      <option value="">All categories</option>
      <option>Investor</option>
      <option>Energy / Cleantech</option>
      <option>AI / Tech</option>
      <option>Academic / Research</option>
      <option>Government</option>
      <option>Accelerator / Ecosystem</option>
      <option>Finance / Banking</option>
      <option>Legal</option>
      <option>Industry / Other</option>
    </select>
    <span class="count" id="cnt"></span>
  </div>
</div>
<table>
  <thead><tr>
    <th style="width:40px">#</th>
    <th>Name</th>
    <th>Company</th>
    <th>Role</th>
    <th>Category</th>
    <th>Connected</th>
  </tr></thead>
  <tbody id="tbody"></tbody>
</table>

<script>
const DATA = {raw};

function badgeClass(cat) {{
  if (cat.startsWith('Investor')) return 'badge-Investor';
  if (cat.startsWith('Energy')) return 'badge-Energy';
  if (cat.startsWith('AI')) return 'badge-AI';
  if (cat.startsWith('Academic')) return 'badge-Academic';
  if (cat.startsWith('Gov')) return 'badge-Government';
  if (cat.startsWith('Accel')) return 'badge-Accelerator';
  if (cat.startsWith('Finance')) return 'badge-Finance';
  if (cat.startsWith('Legal')) return 'badge-Legal';
  if (cat.startsWith('Industry')) return 'badge-Industry';
  return 'badge-Other';
}}

function render() {{
  const q = document.getElementById('q').value.toLowerCase();
  const cat = document.getElementById('cat').value;
  const tbody = document.getElementById('tbody');
  let rows = DATA;
  if (q) rows = rows.filter(r => (r.n+r.co+r.p).toLowerCase().includes(q));
  if (cat) rows = rows.filter(r => r.cat === cat);
  document.getElementById('cnt').textContent = rows.length + ' / ' + DATA.length;
  if (!rows.length) {{
    tbody.innerHTML = '<tr><td colspan="6" class="empty">No matches</td></tr>';
    return;
  }}
  tbody.innerHTML = rows.map((r, i) => `
    <tr>
      <td class="num">${{i+1}}</td>
      <td class="name"><a href="${{r.u}}" target="_blank">${{r.n}}</a></td>
      <td class="company" title="${{r.co}}">${{r.co}}</td>
      <td class="position" title="${{r.p}}">${{r.p}}</td>
      <td><span class="badge ${{badgeClass(r.cat)}}">${{r.cat}}</span></td>
      <td class="date">${{r.dt}}</td>
    </tr>
  `).join('');
}}

render();
</script>
</body>
</html>"""

with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done. Written to {out_path}")
print(f"File size: {os.path.getsize(out_path):,} bytes")
