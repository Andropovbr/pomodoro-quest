import json
import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response


logger = logging.getLogger("pomodoro_quest.request")


async def request_logging_middleware(request: Request, call_next: Callable) -> Response:
    """
    Request lifecycle logging middleware.

    Logs one JSON line per request with:
    - request_id
    - method/path
    - status_code
    - latency_ms

    Also injects X-Request-ID into the response headers.
    """
    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        latency_ms = int((time.perf_counter() - start) * 1000)
        logger.exception(
            json.dumps(
                {
                    "event": "request_error",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "latency_ms": latency_ms,
                }
            )
        )
        raise

    latency_ms = int((time.perf_counter() - start) * 1000)
    logger.info(
        json.dumps(
            {
                "event": "request_completed",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "latency_ms": latency_ms,
            }
        )
    )

    response.headers["X-Request-ID"] = request_id
    return response
