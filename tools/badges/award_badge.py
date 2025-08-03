# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -*- coding: utf-8 -*-
import json
import hashlib
import io
import sys
from datetime import datetime, timezone
from pathlib import Path
from openbadges_bakery import bake

def slugify(text):
    return ''.join(c if c.isalnum() else '-' for c in text.lower()).strip('-')

def write_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

# --- Locate incubator-training root directory ---
SCRIPT_DIR = Path(__file__).resolve().parent
for parent in SCRIPT_DIR.parents:
    if parent.name == "incubator-training":
        ROOT_DIR = parent
        break
else:
    print("❌ Could not locate 'incubator-training' directory.")
    sys.exit(1)

SITE_BADGES_DIR = ROOT_DIR / "site" / "src" / "site" / "resources" / "badges"
if not SITE_BADGES_DIR.is_dir():
    print(f"❌ Error: badge directory not found at {SITE_BADGES_DIR}")
    sys.exit(1)

# --- Select badge from available ones ---
badge_slugs = sorted([d.name for d in SITE_BADGES_DIR.iterdir() if d.is_dir()])
if not badge_slugs:
    print("❌ No badge directories found.")
    sys.exit(1)

print("Available Badges:")
for idx, slug in enumerate(badge_slugs, 1):
    print(f"{idx}. {slug}")
choice = input("Select badge by number: ").strip()

try:
    badge_slug = badge_slugs[int(choice) - 1]
except (IndexError, ValueError):
    print("❌ Invalid choice.")
    sys.exit(1)

# --- Recipient info ---
name = input("Enter recipient full name: ").strip()
email = input("Enter recipient email: ").strip()
name_slug = slugify(name)

# --- Badge paths ---
BADGE_DIR = SITE_BADGES_DIR / badge_slug
ASSERTION_DIR = BADGE_DIR / "assertions"
BAKED_DIR = BADGE_DIR / "baked"

ASSERTION_DIR.mkdir(exist_ok=True)
BAKED_DIR.mkdir(exist_ok=True)

BASE_IMAGE = BADGE_DIR / "badge.png"
if not BASE_IMAGE.is_file():
    print(f"❌ Error: badge image not found at {BASE_IMAGE}")
    sys.exit(1)

BADGECLASS_URL = f"https://training.apache.org/badges/{badge_slug}/badgeclass.json"
ASSERTION_BASE_URL = f"https://training.apache.org/badges/{badge_slug}/assertions"
# --- Create assertion ---
uid = hashlib.sha256(email.encode("utf-8")).hexdigest()
issued_on = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

assertion = {
    "@context": "https://w3id.org/openbadges/v2",
    "type": "Assertion",
    "id": f"{ASSERTION_BASE_URL}/{name_slug}.json",
    "recipient": {
        "type": "email",
        "hashed": True,
        "salt": None,
        "identity": f"sha256${uid}"
    },
    "badge": BADGECLASS_URL,
    "verification": {
        "type": "Hosted"
    },
    "issuedOn": issued_on
}

assertion_path = ASSERTION_DIR / f"{name_slug}.json"
write_json(assertion_path, assertion)

# --- Bake badge image ---
output_image = BAKED_DIR / f"{name_slug}.png"
with open(BASE_IMAGE, "rb") as img_file:
    baked_file = bake(io.BytesIO(img_file.read()), json.dumps(assertion))
    with open(output_image, "wb") as out:
        out.write(baked_file.read())
    baked_file.close()

print(f"🏷️  Baked badge saved to {output_image}")
