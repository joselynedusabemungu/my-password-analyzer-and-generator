import math
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Password Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CredentialPayload(BaseModel):
    password: str
    pool_size: int

@app.post("/analyze")
async def analyze_credential(payload: CredentialPayload):
    password = payload.password
    pool_size = payload.pool_size

    length = len(password)
    if length > 0 and pool_size > 0:
        entropy_bits = round(length * math.log2(pool_size))
    else:
        entropy_bits = 0

    human_patterns = ["123", "abc", "qwe", "asd", "pass", "admin", "th", "he", "er"]
    risk_matches = sum(1 for pattern in human_patterns if pattern in password.lower())
            
    if entropy_bits < 45 or risk_matches > 0:
        tier = "Vulnerable"
        desc = "CRITICAL EXPOSURE: This asset contains predictable typing patterns or is too short. A cracking script could break it instantly."
    elif entropy_bits < 72:
        tier = "Moderate"
        desc = "WARNING: Decent baseline strength, but increasing the length or adding more character types will close the cracking window."
    else:
        tier = "Excellent"
        desc = "SECURE ASSET: This password shows excellent mathematical randomness and is resistant to common pattern-matching attacks."

    return {
        "password_scanned": password,
        "entropy_bits": entropy_bits,
        "risk_matches": risk_matches,
        "tier_status": tier,
        "summary_desc": desc
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
