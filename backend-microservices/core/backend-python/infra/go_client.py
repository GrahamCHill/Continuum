import os
import httpx

GO_SERVICE_URL = os.getenv("GO_SERVICE_URL")

def call_go_service():
    r = httpx.get(f"{GO_SERVICE_URL}/internal")
    r.raise_for_status()
    return {"go_response": r.json()}
