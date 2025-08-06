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
import hashlib
import json
import sys
from pathlib import Path
from openbadges_bakery import unbake

def verify_email_hash_from_baked(badge_path, email_to_check):
    try:
        with open(badge_path, "rb") as f:
            baked_json = unbake(f)
    except Exception as e:
        print(f"❌ Failed to extract Open Badge metadata: {e}")
        return False

    if baked_json is None:
        print("❌ No Open Badge metadata found in the PNG.")
        return False

    try:
        data = json.loads(baked_json)
        recipient = data["recipient"]

        if recipient["type"] != "email" or not recipient.get("hashed", False):
            print("❌ Badge recipient is not a hashed email.")
            return False

        identity = recipient["identity"]
        if not identity.startswith("sha256$"):
            print("❌ Unsupported hash format.")
            return False

        expected_hash = identity.split("sha256$")[1]
        actual_hash = hashlib.sha256(email_to_check.encode("utf-8")).hexdigest()

        if expected_hash == actual_hash:
            print("✅ Email matches the recipient hash.")
            return True
        else:
            print("❌ Email does NOT match the recipient hash.")
            return False

    except KeyError as e:
        print(f"❌ Missing field in assertion: {e}")
        return False
    except json.JSONDecodeError:
        print("❌ Assertion is not valid JSON.")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python verify_baked_badge_email.py <badge.png> <email>")
        sys.exit(1)

    badge_file = Path(sys.argv[1])
    email_input = sys.argv[2]

    verify_email_hash_from_baked(badge_file, email_input)
