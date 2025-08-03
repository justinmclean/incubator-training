🏅 Open Badge Issuer Toolkit (Python)
======================================

This toolkit helps you create, award, bake, and verify Open Badges v2.0
(https://www.imsglobal.org/openbadges) using Python.

📁 Badge Directory Structure
---------------------
.
└── badges/
    └── <badge_slug>/
        ├── badge.png
        ├── badgeclass.json
        ├── issuer.json
        └── assertions/
           └── <recipient>.json

🚀 Scripts
----------

1. create_badge.py
   Create a new badge definition.

   Usage:
     python create_badge.py

   - Prompts for badge name, description, and narrative (criteria)
   - Creates:
     - badges/<slug>/issuer.json
     - badges/<slug>/badgeclass.json
     - badges/<slug>/badge.png 
   - Requires:
     - <slug>.png to already exist

2. award_badges.py
   Award the badge to multiple recipients from a CSV file.

   Usage:
     python award_badges.py

   - Reads recipients.csv:
       name,email
       Alice Smith,alice@example.com
       Bob Jones,bob@example.com

   - Outputs for each recipient:
     - badges/<slug>/assertions/<recipient>.json
     - badges/<slug>/badge_<slug>_<recipient>.png (baked image)

3. award_badge.py
   Award a badge to a single recipient interactively.

   Usage:
     python award_badge.py

   - Prompts for:
     - Badge (from list of available badges)
     - Recipient name and email
   - Outputs:
     - badges/<slug>/assertions/<recipient>.json
     - badges/<slug>/badge_<slug>_<recipient>.png (baked image)

4. verify_badge.py
   Verify a baked badge PNG file.

   Usage:
     python verify_badge.py badge.png

   - Extracts and displays the baked assertion
   - Validates structure and required fields
   - Optionally checks that the hosted assertion matches the baked one

📦 Requirements
---------------
Install dependencies with:

  pip install openbadges-bakery requests

🌐 URLs
-------
Badges use the training.apache.org namespace by default:

- Issuer:
    https://training.apache.org/badges/<slug>/issuer.json
- BadgeClass:
    https://training.apache.org/badges/<slug>/badgeclass.json
- Assertions:
    https://training.apache.org/assertions/<slug>/<recipient>.json

To enable public verification, upload the relevant files to match those URLs.

🛡️ Notes
--------
- Email addresses are hashed using SHA-256
- Assertions follow Open Badges v2.0 JSON-LD format
- Baked PNGs are valid standalone badges with embedded metadata

✅ Example
----------
  python create_badge.py
  python award_badge.py
  python verify_badge.py alice-smith.png
