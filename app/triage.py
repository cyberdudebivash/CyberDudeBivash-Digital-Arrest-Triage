def triage_digital_arrest(transcript: str, url: str = None, image_url: str = None, language: str = "en") -> list[str]:
    indicators = []
    if "arrest" in transcript.lower() or "cbi" in transcript.lower() or "ed" in transcript.lower():
        indicators.append("Fake authority mention")
    if url and "gov.in" not in url:
        indicators.append("Suspicious URL")
    if image_url:
        indicators.append("Fake ID image detected - verify manually")  # Stub for OCR integration
    if language == "hi":
        indicators.append("Hindi script - common in India scams")
    return indicators

# © 2026 CyberDudeBivash Pvt. Ltd.