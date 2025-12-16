from fastapi import Request
from audit.logger import audit_log

async def audit_middleware(request: Request, call_next):
    response = await call_next(request)

    audit_log(
        action="http_request",
        entity="route",
        entity_id=request.url.path,
        user_id=request.headers.get("X-User-ID"),
        request_ip=request.client.host if request.client else None,
        details={
            "method": request.method,
            "status": response.status_code,
        },
    )

    return response
