from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import downloader

app = FastAPI()

# CORS — allows your frontend (different port) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production you'd lock this down
    allow_methods=["*"],
    allow_headers=["*"],
)

# This defines what the frontend sends us in a POST request
class DownloadRequest(BaseModel):
    url: str
    format: str = "mp4"   # default to mp4
    quality: str = "best" # default to best quality


@app.get("/")
def root():
    """Just a health check — visit http://localhost:8000 to confirm it's running"""
    return {"message": "YT Downloader API is running!"}


@app.get("/info")
def get_info(url: str):
    """
    Frontend calls this first to preview the video before downloading.
    Example: GET /info?url=https://youtube.com/watch?v=...
    """
    try:
        info = downloader.get_video_info(url)
        return info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/download")
def download(req: DownloadRequest):
    """
    Frontend calls this to trigger the actual download.
    Returns the file directly to the browser.
    """
    try:
        filepath = downloader.download_video(req.url, req.format, req.quality)

        if not os.path.exists(filepath):
            raise HTTPException(status_code=500, detail="File not found after download")

        # FileResponse sends the file to the browser as a download
        return FileResponse(
            path=filepath,
            filename=os.path.basename(filepath),
            media_type="application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))