from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException, Request

from backend.app.core.config import get_settings


_events: dict[str, deque[float]] = defaultdict(deque)
_lock = Lock()


def enforce_rate_limit(request: Request) -> None:
    """Apply a small process-local limit suitable for development and one-worker deployments."""
    settings = get_settings()
    now = monotonic()
    client = request.client.host if request.client else "unknown"
    with _lock:
        bucket = _events[client]
        while bucket and now - bucket[0] > settings.rate_limit_window_seconds:
            bucket.popleft()
        if len(bucket) >= settings.rate_limit_requests:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        bucket.append(now)
