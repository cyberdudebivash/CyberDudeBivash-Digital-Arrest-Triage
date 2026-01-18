# CyberDudeBivash Digital Arrest Triage Script

**AI-powered tool to detect Digital Arrest scams in India**  
Get instant risk score, red flags, and advice by pasting suspicious call/message transcripts.

Live Demo: https://cyberdudebivash-digital-arrest-triage.onrender.com/docs  
Landing Page: https://cyberdudebivash-digital-arrest-triage.onrender.com/

© 2026 CyberDudeBivash Pvt. Ltd. All rights reserved.  
Built under CyberDudeBivash™ signature, copyright, and authority.

## Features

- Zero-trust authentication (register/login → JWT)
- Real-time scam triage with risk scoring (0–100)
- Detects fake authority mentions, urgency words, UPI references, Hindi keywords, etc.
- Saves reports in SQLite (persistent)
- Dockerized & deployed on Render (free tier)
- Interactive Swagger docs + simple landing page

## Quick Start (Local)

1. Clone repo:
   ```bash
   git clone https://github.com/cyberdudebivash/CyberDudeBivash-Digital-Arrest-Triage.git
   cd CyberDudeBivash-Digital-Arrest-Triage

Run with Docker:Bashdocker compose up --build
Open in browser:
Landing page: http://localhost:8000/
Swagger API docs: http://localhost:8000/docs


Test the API (curl examples)
Register a user
Bashcurl -X POST "http://localhost:8000/register" \
-H "Content-Type: application/json" \
-d '{"username":"testuser","password":"secure123"}'
Login & get token
Bashcurl -X POST "http://localhost:8000/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=testuser&password=secure123"
Analyze a scam message (replace YOUR_TOKEN with access_token from login)
Bashcurl -X POST "http://localhost:8000/triage" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{"transcript":"CBI bol raha hoon digital arrest hai turant 50000 UPI pe bhejo warna police aa jayegi","language":"en"}'
Live on Render (same commands, replace localhost with):
texthttps://cyberdudebivash-digital-arrest-triage.onrender.com
Tech Stack

Backend: FastAPI (Python)
Auth: JWT + passlib (bcrypt → SHA256 for MVP)
DB: SQLite (persistent via Docker volume)
Deployment: Docker + Render.com (free tier)
Frontend: Simple HTML landing page

License
MIT License – see LICENSE file.
Built by
CyberDudeBivash™
Protecting India from digital fraud one triage at a time.
Questions? Reach out on X/LinkedIn.
#CyberSecurity #DigitalArrest #India #CyberDudeBivash