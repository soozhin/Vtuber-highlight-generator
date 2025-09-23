from fastapi import FastAPI
from backend.routers.router import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Highlight generator backend",
    description="An app that generates highlight clips from just a YouTube URL",
)

app.include_router(router, prefix="/api/v1")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# For demonstration purposes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
