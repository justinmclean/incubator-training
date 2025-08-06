# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements. See the NOTICE file for details.
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-
import csv
import hashlib
import json
import sys
import io
from datetime import datetime, timezone
from pathlib import Path
from openbadges_bakery import bake

def write_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

# --- Locate root directory ---
SCRIPT_DIR = Path(__file__).resolve().parent
for parent in SCRIPT_DIR.parents:
    if parent.name == "incubator-training":
        ROOT_DIR = parent
        break
else:
    print("❌ Could not locate 'incubator-training' directory in script path.")
    sys.exit(1)

# --- Set paths ---
BADGES_BASE_DIR = ROOT_DIR / "site" / "src" / "site" / "resources" / "badges"
if not BADGES_BASE_DIR.exists():
    print(f"❌ Badge directory does not exist at {BADGES_BASE_DIR}")
    sys.exit(1)

# --- Select badge from existing ---
badge_slugs = sorted([d.name for d in BADGES_BASE_DIR.iterdir() if d.is_dir()])
if not badge_slugs:
    print("❌ No badge directories found.")
    sys.exit(1)

print("Available Badges:")
for idx, slug in enumerate(badge_slugs, 1):
    print(f"{idx}. {slug}")

try:
    selection = int(input("Select badge by number: ").strip())
    badge_slug = badge_slugs[selection - 1]
except (ValueError, IndexError):
    print("❌ Invalid badge selection.")
    sys.exit(1)

# --- Set badge-specific paths ---
BADGE_DIR = BADGES_BASE_DIR / badge_slug
ASSERTION_DIR = BADGE_DIR / "assertions"
BAKED_DIR = BADGE_DIR / "baked"

ASSERTION_DIR.mkdir(parents=True, exist_ok=True)
BAKED_DIR.mkdir(parents=True, exist_ok=True)

BASE_IMAGE = BADGE_DIR / "badge.png"
if not BASE_IMAGE.exists():
    print(f"❌ Error: badge image not found at {BASE_IMAGE}")
    sys.exit(1)

BADGECLASS_URL = f"https://training.apache.org/badges/{badge_slug}/badgeclass.json"
ASSERTION_BASE_URL = f"https://training.apache.org/badges/{badge_slug}/assertions"

# --- Read recipients.csv ---
try:
    with open("recipients.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row["email"].strip()
            uid = hashlib.sha256(email.encode("utf-8")).hexdigest()
            badge_id_length = 12    
            while True:
                badge_id = uid[:badge_id_length]
                assertion_path = ASSERTION_DIR / f"{badge_id}.json"
                output_image = BAKED_DIR / f"{badge_id}.png"
                if not assertion_path.exists() and not output_image.exists():
                    break
                badge_id_length += 1
                if badge_id_length > len(uid):
                    print("❌ Could not generate unique badge ID — hash exhausted.")
                    sys.exit(1)

            issued_on = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            assertion = {
                "@context": "https://w3id.org/openbadges/v2",
                "type": "Assertion",
                "id": f"{ASSERTION_BASE_URL}/{badge_id}.json",
                "recipient": {
                    "type": "email",
                    "hashed": True,
                    "identity": f"sha256${uid}"
                },
                "badge": BADGECLASS_URL,
                "verification": {
                    "type": "Hosted"
                },
                "issuedOn": issued_on
            }

            # Write assertion
            assertion_path = ASSERTION_DIR / f"{badge_id}.json"
            write_json(assertion_path, assertion)

            # Bake badge image
            with open(BASE_IMAGE, "rb") as img_file:
                baked_file = bake(io.BytesIO(img_file.read()), json.dumps(assertion))
                output_image = BAKED_DIR / f"{badge_id}.png"
                with open(output_image, "wb") as out:
                    out.write(baked_file.read())
                baked_file.close()

            print(f"🏷️  Baked badge for {email} → {output_image}")

except FileNotFoundError:
    print("❌ recipients.csv file not found.")
    sys.exit(1)
except KeyError as e:
    print(f"❌ Missing column in CSV: {e}")
    sys.exit(1)
