import json, re, os

NODE_PATH = r"C:\Users\mujta\AppData\Roaming\npm\node_modules"
os.environ["NODE_PATH"] = NODE_PATH

with open(r"C:\Users\mujta\OneDrive\Documents\Crypto\Robot Work\chief-of-staff\pst-extract\senders_summary.json", encoding="utf-8") as f:
    data = json.load(f)

# Blocklist patterns — no-reply addresses, known newsletters, platforms, banks, gov portals, etc.
SKIP_DOMAINS = {
    "expedia.com", "eg.expedia.com", "google.com", "accounts.google.com",
    "substack.com", "beehiiv.com", "mail.beehiiv.com", "payments.interac.ca",
    "bcse.org", "scaleai.ca", "ethglobal.com", "calendly.com", "slack.com",
    "slackhq.com", "slack-mail.com", "microsoft.com", "microsoftonline.com",
    "microsoft365.com", "outlook.mail.microsoft", "zoom.us", "e.zoom.us",
    "docusign.net", "camail.docusign.net", "eumail.docusign.net",
    "hellosign.com", "mail.hellosign.com", "trello.com", "airtableemail.com",
    "eventbrite.com", "email.eventbrite.com", "order.eventbrite.com",
    "event.eventbrite.com", "luma-mail.com", "zohobackstage.com",
    "formstack.com", "simplesurvey.com", "smapply.net",
    "bmo.com", "e-news.bmo.com", "td.com", "rbc.com",
    "lastpass.com", "t.lastpass.com", "m.lastpass.com",
    "calendarhero.com", "calendar.luma-mail.com", "user.luma-mail.com",
    "nvidia.com", "news.nvidia.com", "account.nvidia.com",
    "credly.com", "evalato.com", "circleback.ai", "spinach.ai",
    "fireflies.ai", "read.ai", "e.read.ai",
    "zenhub.com", "freshbooks.com", "fb02.freshbooks.com",
    "ccsend.com", "shared1.ccsend.com",
    "nrcan-rncan.gc.ca", "gc.ca", "international.gc.ca",
    "mg1.substack.com", "mg-d0.substack.com", "transactional.hs-send.com",
    "noreply.github.com", "salesforce.com", "boardy.ai",
    "widehall.com", "alliancemail.com", "admissions.alliancemail.com",
    "updates.admissions.alliancemail.com", "outreach.alliancemail.com",
    "innoveici.quebec", "mg.innoveici.quebec",
    "webhost3.osgoode.yorku.ca", "osgoode.yorku.ca",
    "nb2.mailer@csail.mit.edu", "csail.mit.edu",
    "southparkcommons.com", "information.microsoft.com",
    "notifications.microsoft.com", "accountprotection.microsoft.com",
    "email.slackhq.com", "mail.beehiiv.com", "codelaunch.com",
    "no-replyStartups@google.com",
}

SKIP_NAME_PATTERNS = [
    r"noreply", r"no.reply", r"no-reply", r"donotreply", r"do.not.reply",
    r"system@", r"admin@", r"info@", r"hello@", r"team@", r"support@",
    r"notification", r"alert", r"mailer", r"newsletter", r"digest",
    r"portal", r"intake@", r"programs@", r"events@", r"updates@",
    r"community@", r"marketing@", r"partnership", r"membership",
    r"calendar.notification", r"drive-shares", r"forms-receipts",
    r"cloud-noreply", r"CloudPlatform-noreply", r"contactcloud",
    r"workspace-noreply", r"advisory-notifications", r"notify-noreply",
]

SKIP_NAME_WORDS = [
    "eventbrite", "slack", "google", "microsoft", "zoom", "docusign",
    "trello", "airtable", "calendly", "luma", "formstack", "credly",
    "lastpass", "fireflies", "spinach", "boardy", "circleback",
    "newsletter", "noreply", "no-reply", "system", "portal", "mailer",
    "via calendly", "via freshbooks", "via read ai", "via google",
    "via slack", "via luma", "via credly",
]

def is_real_human(entry):
    email = entry["email"].lower().strip()
    name = entry["name"].lower().strip()

    # Skip empty or clearly automated
    if not email or "@" not in email:
        return False

    domain = email.split("@")[-1]
    if domain in SKIP_DOMAINS:
        return False

    # Skip no-reply style prefixes
    local = email.split("@")[0]
    for pat in SKIP_NAME_PATTERNS:
        if re.search(pat, email, re.IGNORECASE):
            return False

    # Skip if name contains platform words
    for word in SKIP_NAME_WORDS:
        if word in name:
            return False

    # Skip obviously automated names
    if not entry["name"] or entry["name"].lower() == email:
        return False

    # Skip gov portals and catch-all addresses
    if any(x in email for x in ["donotreply", "nepasrepondre", "ne-pas-repondre", "noreply", "no-reply"]):
        return False

    return True

# Also tag known categories
def tag(entry):
    email = entry["email"].lower()
    name = entry["name"].lower()
    domain = email.split("@")[-1]

    if any(x in domain for x in ["vc.com", "capital.com", "ventures.com", "fund", "invest"]):
        return "Investor"
    if any(x in domain for x in ["university", "utoronto", "yorku", "uwo", "ucalgary", "vectorinstitute", "mila.quebec", "amii", "torontomu"]):
        return "Academic / Research"
    if any(x in domain for x in ["gc.ca", "gov", "nrcan", "ised", "dec-ced", "albertainnovates", "feddev"]):
        return "Government"
    if any(x in domain for x in ["marsdd", "nextcanada", "venturelab", "altitude", "arctech", "catalyst", "ipcollective", "next.ai", "antler"]):
        return "Accelerator / Ecosystem"
    if any(x in domain for x in ["arcadeiplaw", "pandolaw", "klgates"]):
        return "Legal"
    if any(x in domain for x in ["bdo", "bmo.com", "td.com", "rbc.com"]):
        return "Finance / Banking"
    if any(x in name for x in ["investor", "venture", "capital", "fund", "partner"]):
        return "Investor"
    return "Industry / Other"

humans = [e for e in data if is_real_human(e)]
for e in humans:
    e["category"] = tag(e)

print(f"Filtered to {len(humans)} real humans from {len(data)} total")

# Save clean contacts
out = r"C:\Users\mujta\OneDrive\Documents\Crypto\Robot Work\chief-of-staff\pst-extract\contacts_clean.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(humans, f, indent=2)

print("Saved contacts_clean.json")

# Now build the docx contacts sheet
import subprocess, sys

# Write the node script
node_script = r"""
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        WidthType, BorderStyle, ShadingType, HeadingLevel } = require('docx');
const fs = require('fs');

const contacts = JSON.parse(fs.readFileSync(
  'C:/Users/mujta/OneDrive/Documents/Crypto/Robot Work/chief-of-staff/pst-extract/contacts_clean.json',
  'utf8'
));

const border = { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' };
const borders = { top: border, bottom: border, left: border, right: border };
const cm = { top: 80, bottom: 80, left: 120, right: 120 };

function hCell(text, w) {
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA },
    shading: { fill: '1F3864', type: ShadingType.CLEAR }, margins: cm,
    children: [new Paragraph({ children: [new TextRun({ text, bold: true, color: 'FFFFFF', size: 18, font: 'Arial' })] })] });
}

function catColor(cat) {
  const map = {
    'Investor': 'EAF4FB',
    'Academic / Research': 'EAF7EA',
    'Government': 'FFF8DC',
    'Accelerator / Ecosystem': 'F3E8FF',
    'Legal': 'FFE8E8',
    'Finance / Banking': 'F0F0F0',
    'Industry / Other': 'FFFFFF',
  };
  return map[cat] || 'FFFFFF';
}

function row(c) {
  const fill = catColor(c.category);
  const cols = [c.name, c.email, c.category, String(c.count), (c.subjects||[]).slice(0,2).join(' / ')];
  const ws = [1800, 2400, 1400, 500, 3200];
  return new TableRow({ children: cols.map((v, i) =>
    new TableCell({ borders, width: { size: ws[i], type: WidthType.DXA },
      shading: { fill, type: ShadingType.CLEAR }, margins: cm,
      children: [new Paragraph({ children: [new TextRun({ text: v||'', size: 18, font: 'Arial' })] })] })
  )});
}

const headers = ['Name', 'Email', 'Category', 'Emails', 'Sample Subjects'];
const ws = [1800, 2400, 1400, 500, 3200];

const doc = new Document({
  styles: {
    default: { document: { run: { font: 'Arial', size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 40, bold: true, font: 'Arial', color: '1F3864' },
        paragraph: { spacing: { before: 320, after: 160 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true, font: 'Arial', color: '2E5F9C' },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: {
      page: { size: { width: 15840, height: 12240 }, margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } }
    },
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: 'PST Contacts — Real Humans', font: 'Arial', bold: true, color: '1F3864', size: 40 })] }),
      new Paragraph({ children: [new TextRun({ text: `Extracted from mujtaba@lightgrid.energy.pst  |  ${contacts.length} contacts  |  Newsletters and automated emails removed`, font: 'Arial', size: 20, color: '555555', italics: true })] }),
      new Paragraph({ children: [new TextRun('')] }),
      new Table({
        width: { size: ws.reduce((a,b)=>a+b,0), type: WidthType.DXA },
        columnWidths: ws,
        rows: [
          new TableRow({ tableHeader: true, children: headers.map((h,i) => hCell(h, ws[i])) }),
          ...contacts.map(c => row(c))
        ]
      }),
      new Paragraph({ children: [new TextRun('')] }),
      new Paragraph({ children: [new TextRun({ text: 'Color key: Blue = Investor  |  Green = Academic/Research  |  Yellow = Government  |  Purple = Accelerator/Ecosystem  |  Red = Legal  |  Grey = Finance  |  White = Industry/Other', font: 'Arial', size: 16, italics: true, color: '888888' })] }),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('C:/Users/mujta/OneDrive/Documents/Crypto/Robot Work/chief-of-staff/pst-contacts.docx', buf);
  console.log('Done');
}).catch(e => { console.error(e.message); process.exit(1); });
"""

node_file = r"C:\Users\mujta\OneDrive\Documents\Crypto\Robot Work\chief-of-staff\build_contacts_doc.js"
with open(node_file, "w", encoding="utf-8") as f:
    f.write(node_script)

result = subprocess.run(
    ["node", node_file],
    env={**os.environ, "NODE_PATH": NODE_PATH},
    capture_output=True, text=True
)
print(result.stdout)
if result.stderr:
    print("ERR:", result.stderr[:500])
