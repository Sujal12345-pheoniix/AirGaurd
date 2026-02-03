from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints

app = FastAPI(title="AirGuard API", version="1.0.0")

# CORS
origins = ["*"] # Allow all for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to AirGuard API. Visit /docs for Swagger UI."}
