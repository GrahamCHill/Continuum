from typing import Optional, Dict
from audit.repository import persist_audit_event

def audit_log(
    action: str,
    entity: Optional[str] = None,
    entity_id: Optional[str] = None,
    user_id: Optional[str] = None,
    request_ip: Optional[str] = None,
    details: Optional[Dict] = None,
):
    """
    Record an audit event.

    This function is intentionally thin.
    It defines WHAT is audited, not HOW.
    """
    persist_audit_event(
        action=action,
        entity=entity,
        entity_id=entity_id,
        user_id=user_id,
        request_ip=request_ip,
        details=details,
    )
