# 🏅 Digital Badge FAQ

## What are digital badges?
Digital badges are visual tokens of achievement or participation. Each badge includes embedded metadata that conforms to the [Open Badges](https://www.imsglobal.org/activity/digital-badges) standard. This metadata describes:
- What the badge represents  
- Who issued it  
- When it was issued  
- Who it was issued to (via a hashed email address)  

---

## Who issues these badges?
Badges are issued by the **ASF Training Project** or participating **ASF projects**. The metadata embedded in each badge includes a verifiable issuer profile.

---

## Who can receive a badge?
Badges may be awarded to **Community members completing key activities**, such as writing documentation, helping with releases, mentoring, or sustained participation in ASF projects and initiatives.

---

## Are these only for ASF committers?
No. Many badges are available to **contributors, learners, and participants**, regardless of committer status. They’re meant to encourage broader involvement in the ASF ecosystem.

---

## What can I do with a badge?
You can:
- Share it on LinkedIn, GitHub, or your website  
- Include it in your résumé or portfolio  
- Use it to demonstrate verified experience in open-source contributions or training  
- Store and manage it using services like [Open Badge Passport](https://openbadgepassport.com), which allow you to organize and showcase your badges across different platforms

Each badge includes a unique verification URL.

---

## Where are badges hosted?
Badges are hosted on the [ASF Training site](https://training.apache.org/) or relevant ASF project infrastructure. Badge metadata is available in JSON format for verification.

---

## What personal data is stored?
Badges **do not store names or email addresses**.

Instead, recipient identity is verified using a **SHA-256 hash of their email address**. This allows the badge to be validated without storing personally identifiable information (PII).

---

## Can a badge be revoked?
Yes. Badges can be revoked:
- If issued in error  
- If requested by the recipient  
- If project policy changes  

Revoked badges will no longer verify successfully using Open Badge validators.

---

## How do I verify a badge?
Each badge includes:
- A **PNG file** with embedded metadata  
- A linked **assertion file (JSON)** that contains the hashed recipient ID, issue date, and badge criteria  

You can verify it using tools like:
- [badgecheck.io](https://badgecheck.io/)  
- OpenBadgeValidator  
- Direct inspection of the assertion file  

---

## Do badges confer ASF roles or privileges?
No. Badges are a **form of recognition**, not a form of authority. They do not:
- Grant ASF Membership or committership  
- Provide voting rights  
- Change a person's status within the ASF  

They are designed to encourage learning, visibility, and community engagement.

---

## How do I claim my badge?

Badges are typically awarded automatically or manually and hosted on a public ASF infrastructure URL. There is no account registration required. If your email hash matches a badge, you have effectively "claimed" it. If your badge was not generated but you believe you earned one, contact the issuer.

---

## What if my badge isn’t showing up or validating?

- Double-check the badge URL and associated JSON files  
- Use [https://badgecheck.io](https://badgecheck.io) to validate the badge  
- If you see a 404 or hash mismatch, reach out to the badge issuer or project contact  

---

## Can I see the metadata in a badge?

Yes. Each badge links to three JSON files:
- `assertion.json`: recipient ID hash, issued date, and evidence  
- `badgeclass.json`: badge name, description, and criteria  
- `issuer.json`: who issued the badge and how to contact them  

---

## Can I update or correct my badge after it's issued?

Yes, in most cases. While badge files are static, they can be:
- Re-issued using a new email hash  
- Removed or replaced if there’s an error  
- Updated if badge criteria or descriptions change retroactively  

---

## Why do you use email hashes instead of names?

To protect recipient privacy. By hashing email addresses:
- No PII is stored  
- Verification is still possible via hash comparison  
- We avoid compliance issues with data retention  

---

## Can other ASF projects create their own badge programs?

Yes. Projects can:
- Reuse existing tooling from ASF Training  
- Host their own badge infrastructure  

---

## Can I design or submit artwork for a badge?

Yes. Contributions are welcome!
- Submit artwork as SVG or square PNG (256x256)  
- Prefer CC0 or Apache-licensed assets  
- Badge icons should visually match the badge theme  

---