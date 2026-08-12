from fastapi import Request
from fastapi.responses import JSONResponse


def validation_error_response(request: Request, exc: Exception):
    return JSONResponse({"detail": str(exc)}, status_code=400)
