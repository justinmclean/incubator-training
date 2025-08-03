# -*- coding: utf-8 -*-
import sys
import json
import requests
from openbadges_bakery import unbake

def validate_assertion(assertion):
    if not isinstance(assertion, dict):
        print("❌ Invalid assertion format (expected JSON object).")
        return False

    required_fields = [
        "@context", "type", "id", "recipient",
        "badge", "verification", "issuedOn"
    ]
    missing = [f for f in required_fields if f not in assertion]
    if missing:
        print(f"❌ Missing fields: {', '.join(missing)}")
        return False

    if assertion.get("type") != "Assertion":
        print(f"❌ Invalid type: expected 'Assertion', got '{assertion.get('type')}'")
        return False

    recipient = assertion.get("recipient", {})
    if not isinstance(recipient, dict):
        print("❌ Invalid recipient field (should be a JSON object).")
        return False
    if not recipient.get("hashed") or not recipient.get("identity"):
        print("❌ Recipient must be hashed and contain identity.")
        return False

    print("✅ Assertion structure looks valid.")
    return True

def fetch_hosted_assertion(assertion):
    hosted_url = assertion.get("id")
    if not hosted_url:
        print("⚠️ No hosted assertion URL found.")
        return
    try:
        resp = requests.get(hosted_url, timeout=10)
        if resp.status_code == 200:
            hosted = resp.json()
            if hosted == assertion:
                print("✅ Hosted assertion matches baked data.")
            else:
                print("⚠️ Hosted assertion differs from baked data.")
        else:
            print(f"⚠️ Failed to fetch hosted assertion: HTTP {resp.status_code}")
    except Exception as e:
        print(f"⚠️ Error fetching hosted assertion: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_badge.py <badge.png>")
        sys.exit(1)

    badge_path = sys.argv[1]

    try:
        with open(badge_path, "rb") as f:
            raw_assertion = unbake(f)
    except Exception as e:
        print(f"❌ Failed to extract badge assertion: {e}")
        sys.exit(1)

    if not raw_assertion:
        print("❌ No embedded badge assertion found.")
        sys.exit(1)

    # Decode JSON string if needed
    try:
        if isinstance(raw_assertion, str):
            assertion = json.loads(raw_assertion)
        else:
            assertion = raw_assertion
    except json.JSONDecodeError as e:
        print(f"❌ Assertion is not valid JSON: {e}")
        sys.exit(1)

    print("🔍 Extracted badge assertion:")
    print(json.dumps(assertion, indent=2))

    print("\n📋 Validating structure...")
    if validate_assertion(assertion):
        print("\n🌐 Checking hosted assertion...")
        fetch_hosted_assertion(assertion)

if __name__ == "__main__":
    main()
