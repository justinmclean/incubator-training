# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import argparse
import sys
from pathlib import Path

# --- Locate root directory ---
SCRIPT_DIR = Path(__file__).resolve().parent
for parent in SCRIPT_DIR.parents:
    if parent.name == "incubator-training":
        ROOT_DIR = parent
        break
else:
    print("❌ Could not locate 'incubator-training' directory in script path.")
    sys.exit(1)

# --- Set base path for assertions ---
BADGES_BASE_DIR = ROOT_DIR / "site" / "src" / "site" / "resources" / "badges"

def hash_email(email):
    cleaned = email.strip().lower()
    full_hash = hashlib.sha256(cleaned.encode('utf-8')).hexdigest()
    short_hash = full_hash[:12]
    print(f"[DEBUG] Normalized email: {cleaned}")
    print(f"[DEBUG] Full SHA-256: {full_hash}")
    print(f"[DEBUG] Short hash (first 12 chars): {short_hash}")
    return short_hash

def find_assertions(prefix):
    matches = []
    for assertions_dir in BADGES_BASE_DIR.glob("*/assertions"):
        for file in assertions_dir.glob(f"{prefix}*.json"):
            matches.append(file)
    print(f"[DEBUG] Searched in: {BADGES_BASE_DIR}")
    return matches

def main():
    parser = argparse.ArgumentParser(description="Find badge assertions by email (match filenames by SHA-256 prefix).")
    parser.add_argument("email", help="Recipient email address")
    args = parser.parse_args()

    prefix = hash_email(args.email)
    matches = find_assertions(prefix)

    if matches:
        print("\n✔ Matching badge assertions:")
        for m in matches:
            print(f"- {m}")
    else:
        print("\n✖ No matching assertions found.")

if __name__ == "__main__":
    main()
