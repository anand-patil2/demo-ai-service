from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api.routes.profiles import router as profiles_router

app = FastAPI(title="Customer Profile Microservice")

app.include_router(profiles_router, prefix="/profiles", tags=["profiles"])


@app.get("/healthz")
def healthz():
    return JSONResponse(
        {"status": "ok", "service": "customer-profile", "details": "healthy"}
    )


@app.get("/readyz")
def readyz():
    return JSONResponse({"status": "ready", "service": "customer-profile"})


@app.get("/livez")
def livez():
    return JSONResponse({"status": "live", "service": "customer-profile"})
