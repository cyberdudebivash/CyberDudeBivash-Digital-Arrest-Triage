import bleach

def sanitize_input(text: str) -> str:
    return bleach.clean(text, tags=[], strip=True)

# © 2026 CyberDudeBivash Pvt. Ltd.