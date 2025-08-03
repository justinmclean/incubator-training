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
import os
import json
import shutil
from pathlib import Path
from PIL import Image

def slugify(text):
    return ''.join(c if c.isalnum() else '-' for c in text.lower()).strip('-')

def write_json(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)

# --- Prompt for badge info ---
badge_name = input("Enter badge name (e.g., Mentor Training): ").strip()
badge_slug = slugify(badge_name)
badge_label = badge_name.title()

description = input(f"Enter badge description [{badge_label} completion]: ").strip()
if not description:
    description = f"{badge_label} completion"

narrative = input(f"Enter narrative [{badge_label} awarded for completion of Apache training module]: ").strip()
if not narrative:
    narrative = f"{badge_label} awarded for completion of Apache training module"

# --- Path setup ---
SCRIPT_DIR = Path(__file__).resolve().parent

# Find the incubator-training root directory
for parent in SCRIPT_DIR.parents:
    if parent.name == "incubator-training":
        ROOT_DIR = parent
        break
else:
    print("❌ Could not locate 'incubator-training' directory in script path.")
    exit(1)

# Define where badges will be written
SITE_BADGES_DIR = ROOT_DIR / "site" / "src" / "site" / "resources" / "badges"
BADGE_DIR = SITE_BADGES_DIR / badge_slug
BADGE_DIR.mkdir(parents=True, exist_ok=True)

if BADGE_DIR.exists():
    print(f"⚠️  Badge directory already exists: {BADGE_DIR}")

BADGE_DIR.mkdir(parents=True, exist_ok=True)

# --- Image ---
BASE_IMAGE_PATH = SCRIPT_DIR / f"{badge_slug}.png"
BADGE_IMAGE_PATH = BADGE_DIR / "badge.png"

if not BASE_IMAGE_PATH.exists():
    print(f"❌ Base badge image not found at {BASE_IMAGE_PATH}")
    exit(1)

shutil.copy(BASE_IMAGE_PATH, BADGE_IMAGE_PATH)

# Check image size
with Image.open(BASE_IMAGE_PATH) as img:
    if img.size != (256, 256):
        print("⚠️  Warning: Badge image is not 256x256 pixels. It may not render correctly in some badge systems.")

# --- Issuer JSON ---
ISSUER_URL = f"https://training.apache.org/badges/{badge_slug}/issuer.json"
issuer = {
    "@context": "https://w3id.org/openbadges/v2",
    "type": "Issuer",
    "id": ISSUER_URL,
    "name": "Apache Training",
    "url": "https://training.apache.org",
    "description": "ASF Training Project"
}
write_json(BADGE_DIR / "issuer.json", issuer)

# --- BadgeClass JSON ---
BADGECLASS_URL = f"https://training.apache.org/badges/{badge_slug}/badgeclass.json"
BADGE_IMAGE_URL = f"https://training.apache.org/badges/{badge_slug}/badge.png"

badgeclass = {
    "@context": "https://w3id.org/openbadges/v2",
    "type": "BadgeClass",
    "id": BADGECLASS_URL,
    "name": badge_label,
    "description": description,
    "image": BADGE_IMAGE_URL,
    "criteria": {
        "narrative": narrative
    },
    "issuer": ISSUER_URL
}
write_json(BADGE_DIR / "badgeclass.json", badgeclass)

print(f"\n🏷️  Badge '{badge_name}' created at: {BADGE_DIR}")
print("\n🔗 Public badge URLs:")
print(f" - BadgeClass: {BADGECLASS_URL}")
print(f" - Badge Image: {BADGE_IMAGE_URL}")
print(f" - Issuer: {ISSUER_URL}")
