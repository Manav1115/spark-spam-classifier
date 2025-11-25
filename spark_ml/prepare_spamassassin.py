import os
import csv
import email

# Paths
RAW_DIR = "/home/kalp/spam_project/raw"
OUT_CSV = "/home/kalp/spam_project/data/emails.csv"

os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)

rows = []

def extract_body_from_email(msg):
    """
    Extract the body text from an email.message.Message object.
    Handles multipart and plain text emails.
    """
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body += part.get_payload(decode=True).decode("latin-1", errors="ignore")
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True)
            if body:
                body = body.decode("latin-1", errors="ignore")
        except:
            body = ""

    if body is None:
        body = ""

    # Clean text
    body = body.replace("\n", " ").replace("\r", " ")
    return body.strip()


def load_folder(folder_name, label):
    """
    Load all email files from a folder and append to rows list.
    folder_name: name inside RAW_DIR (e.g., 'spam', 'easy_ham')
    label: 1 for spam, 0 for ham
    """
    folder_path = os.path.join(RAW_DIR, folder_name)
    print(f"Processing {folder_name} ...")

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        # Only process files
        if not os.path.isfile(full_path):
            continue

        try:
            with open(full_path, "r", encoding="latin-1", errors="ignore") as f:
                msg = email.message_from_file(f)

            body = extract_body_from_email(msg)
            if len(body.strip()) == 0:
                continue

            rows.append([label, body])

        except Exception as e:
            print(f"Error reading {filename}: {e}")


# Load all folders
load_folder("spam", 1)
load_folder("easy_ham", 0)
load_folder("hard_ham", 0)

# Write to CSV
print("Writing CSV...")

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["label", "text"])
    writer.writerows(rows)

print(f"Saved CSV to: {OUT_CSV}")
print(f"Total rows: {len(rows)}")
