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
import sys
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_ASSERTION_FIELDS = ["@context", "type", "id", "recipient", "badge", "verification", "issuedOn"]
REQUIRED_BADGECLASS_FIELDS = ["@context", "type", "id", "name", "description", "criteria", "issuer"]
REQUIRED_ISSUER_FIELDS = ["@context", "type", "id", "name", "url", "description"]

ROOT_DIR = Path(__file__).resolve().parent
for parent in ROOT_DIR.parents:
    if parent.name == "incubator-training":
        BASE_DIR = parent / "site" / "src" / "site" / "resources" / "badges"
        break
else:
    print("❌ Could not locate 'incubator-training' directory.")
    sys.exit(1)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https") and bool(result.netloc)
    except:
        return False

def validate_json(path, required_fields):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"Invalid JSON: {e}"]

    issues = []
    for field in required_fields:
        if field not in data:
            issues.append(f"Missing required field: '{field}'")

    if "id" in data and not is_valid_url(data["id"]):
        issues.append(f"Invalid or missing 'id' URL: {data['id']}")

    return issues

def validate_all_badges():
    total = 0
    failed = 0

    for badge_dir in BASE_DIR.iterdir():
        if not badge_dir.is_dir():
            continue

        print(f"\n🔍 Validating badge: {badge_dir.name}")

        badgeclass = badge_dir / "badgeclass.json"
        issuer = badge_dir / "issuer.json"
        assertions_dir = badge_dir / "assertions"

        if badgeclass.exists():
            issues = validate_json(badgeclass, REQUIRED_BADGECLASS_FIELDS)
            if issues:
                print("  ❌ badgeclass.json:")
                for issue in issues:
                    print(f"    - {issue}")
                failed += 1
        else:
            print("  ❌ Missing badgeclass.json")
            failed += 1

        if issuer.exists():
            issues = validate_json(issuer, REQUIRED_ISSUER_FIELDS)
            if issues:
                print("  ❌ issuer.json:")
                for issue in issues:
                    print(f"    - {issue}")
                failed += 1
        else:
            print("  ❌ Missing issuer.json")
            failed += 1

        if assertions_dir.exists():
            for assertion_file in assertions_dir.glob("*.json"):
                total += 1
                issues = validate_json(assertion_file, REQUIRED_ASSERTION_FIELDS)
                if issues:
                    print(f"  ❌ Assertion {assertion_file.name}:")
                    for issue in issues:
                        print(f"    - {issue}")
                    failed += 1
        else:
            print("  ⚠️ No assertions/ directory found")

    print("\n✅ Validation complete.")
    print(f"Total assertions checked: {total}")
    print(f"Total problems found: {failed}")

if __name__ == "__main__":
    validate_all_badges()
