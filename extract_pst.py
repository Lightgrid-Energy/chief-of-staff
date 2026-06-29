import win32com.client
import json
import os
import re
from datetime import datetime

OUTPUT_DIR = r"C:\Users\mujta\OneDrive\Documents\Crypto\Robot Work\chief-of-staff\pst-extract"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PST_PATH = r"C:\Users\mujta\Downloads\mujtaba@lightgrid.energy.pst"
CHUNK_SIZE = 500

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Find the PST store
store = None
for i in range(1, outlook.Stores.Count + 1):
    s = outlook.Stores.Item(i)
    if "lightgrid" in (s.FilePath or "").lower():
        store = s
        break

if not store:
    print("PST store not found")
    exit(1)

print(f"Found store: {store.DisplayName}")

contacts = []
emails = []
email_chunk = 0
contact_chunk = 0

def safe(val):
    try:
        return str(val) if val else ""
    except:
        return ""

def process_folder(folder, depth=0):
    global email_chunk, contact_chunk
    indent = "  " * depth
    name = safe(folder.Name)
    print(f"{indent}Processing: {name}")

    try:
        items = folder.Items
        count = items.Count
        print(f"{indent}  {count} items")

        for i in range(1, count + 1):
            try:
                item = items.Item(i)
                cls = item.Class

                # 43 = MailItem, 40 = ContactItem
                if cls == 43:  # Email
                    try:
                        sender_name = safe(item.SenderName)
                        sender_email = safe(item.SenderEmailAddress)
                        subject = safe(item.Subject)
                        received = safe(item.ReceivedTime)
                        to = safe(item.To)
                        cc = safe(item.CC)
                        body_preview = safe(item.Body)[:300] if item.Body else ""

                        emails.append({
                            "from_name": sender_name,
                            "from_email": sender_email,
                            "to": to,
                            "cc": cc,
                            "subject": subject,
                            "date": received,
                            "body_preview": body_preview,
                            "folder": name
                        })

                        if len(emails) >= CHUNK_SIZE:
                            path = os.path.join(OUTPUT_DIR, f"emails_chunk_{email_chunk:03d}.json")
                            with open(path, "w", encoding="utf-8") as f:
                                json.dump(emails, f, indent=2, default=str)
                            print(f"  Saved email chunk {email_chunk} ({len(emails)} emails)")
                            email_chunk += 1
                            emails.clear()
                    except Exception as e:
                        pass

                elif cls == 40:  # Contact
                    try:
                        contacts.append({
                            "full_name": safe(item.FullName),
                            "first_name": safe(item.FirstName),
                            "last_name": safe(item.LastName),
                            "email1": safe(item.Email1Address),
                            "email2": safe(item.Email2Address),
                            "company": safe(item.CompanyName),
                            "title": safe(item.JobTitle),
                            "phone": safe(item.BusinessTelephoneNumber),
                            "mobile": safe(item.MobileTelephoneNumber),
                            "notes": safe(item.Body)[:200] if item.Body else "",
                        })
                    except Exception as e:
                        pass

            except Exception as e:
                pass

    except Exception as e:
        print(f"{indent}  Error reading items: {e}")

    # Recurse into subfolders
    try:
        for j in range(1, folder.Folders.Count + 1):
            try:
                process_folder(folder.Folders.Item(j), depth + 1)
            except:
                pass
    except:
        pass

root = store.GetRootFolder()
process_folder(root)

# Save remaining emails
if emails:
    path = os.path.join(OUTPUT_DIR, f"emails_chunk_{email_chunk:03d}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=2, default=str)
    print(f"Saved final email chunk {email_chunk} ({len(emails)} emails)")

# Save all contacts in one file
if contacts:
    path = os.path.join(OUTPUT_DIR, "contacts_all.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, default=str)
    print(f"Saved {len(contacts)} contacts")

# Build summary of unique senders
all_senders = {}
for chunk_file in sorted(os.listdir(OUTPUT_DIR)):
    if chunk_file.startswith("emails_chunk"):
        with open(os.path.join(OUTPUT_DIR, chunk_file), encoding="utf-8") as f:
            chunk = json.load(f)
        for e in chunk:
            key = e["from_email"].lower().strip()
            if key and "@" in key:
                if key not in all_senders:
                    all_senders[key] = {"name": e["from_name"], "email": e["from_email"], "count": 0, "subjects": []}
                all_senders[key]["count"] += 1
                if len(all_senders[key]["subjects"]) < 3:
                    all_senders[key]["subjects"].append(e["subject"])

senders_list = sorted(all_senders.values(), key=lambda x: -x["count"])
path = os.path.join(OUTPUT_DIR, "senders_summary.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(senders_list, f, indent=2, default=str)

print(f"\nDone. {sum(1 for f in os.listdir(OUTPUT_DIR) if f.startswith('emails_chunk'))} email chunks, {len(contacts)} contacts, {len(senders_list)} unique senders.")
