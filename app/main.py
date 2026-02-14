from fastapi import FastAPI

from app.api.videos.router import router as video_router

app = FastAPI(title="CenterPass (Netball Stats) API", version="0.1.0")

app.include_router(video_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
