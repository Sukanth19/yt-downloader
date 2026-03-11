from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import downloader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    url: str
    format: str = "mp4"
    quality: str = "best"


@app.get("/")
def root():
    return {"message": "YT Downloader API is running!"}


@app.get("/info")
def get_info(url: str):
    try:
        info = downloader.get_video_info(url)
        return info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/download")
def download(req: DownloadRequest):
    try:
        filepath = downloader.download_video(req.url, req.format, req.quality)

        if not os.path.exists(filepath):
            raise HTTPException(status_code=500, detail="File not found after download")

        return FileResponse(
            path=filepath,
            filename=os.path.basename(filepath),
            media_type="application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))