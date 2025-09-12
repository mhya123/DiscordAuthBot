from __future__ import annotations

import logging
import httpx
from typing import Any, Dict, Optional

log = logging.getLogger("authbot.auth_api")

class AuthAPI:
    """Simple client for the login auth API."""

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def login(self, login: str, password: str) -> Dict[str, Any]:
        # API expects action in query string per provided cURL example
        url = f"{self.base_url}/?action=login"
        data = {
            "login": login,
            "password": password,
        }
        # Do not log credentials; log high-level info only
        log.info("AuthAPI: POST %s", url)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
            status = resp.status_code
            log.debug("AuthAPI: response status=%s", status)
            try:
                payload = resp.json()
            except Exception:
                # Non-JSON response; normalize
                payload = {"success": False}
            # Surface HTTP status for callers without raising
            payload.setdefault("status_code", status)
            log.info("AuthAPI: login success=%s status=%s", bool(payload.get("success")), status)
            return payload

    @staticmethod
    def pick_username(payload: Dict[str, Any]) -> Optional[str]:
        try:
            return payload.get("user", {}).get("username")
        except Exception:
            return None

    @staticmethod
    def is_success(payload: Dict[str, Any]) -> bool:
        # Treat only HTTP 200 + payload.success truthy as success
        status = int(payload.get("status_code", 0))
        return status == 200 and bool(payload.get("success"))
