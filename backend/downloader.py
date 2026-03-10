import yt_dlp
import os

# This is the folder where downloaded files will be saved temporarily
DOWNLOAD_DIR = "downloads"

def ensure_download_dir():
    """Create the downloads folder if it doesn't exist"""
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

def download_video(url: str, format: str = "mp4", quality: str = "best") -> str:
    """
    Downloads a YouTube video or audio.
    
    url     -> the YouTube link
    format  -> "mp4" for video, "mp3" for audio only
    quality -> "best", "720", "480", "360"
    
    Returns the file path of the downloaded file.
    """
    ensure_download_dir()

    if format == "mp3":
        # Audio only — strips video, converts to mp3
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:
        # Video — pick quality
        if quality == "best":
            fmt = "bestvideo+bestaudio/best"
        else:
            fmt = f"bestvideo[height<={quality}]+bestaudio/best"

        ydl_opts = {
            "format": fmt,
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "merge_output_format": "mp4",  # always output as mp4
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # Figure out what the final filename is
        filename = ydl.prepare_filename(info)
        # If mp3, the extension changes after conversion
        if format == "mp3":
            filename = os.path.splitext(filename)[0] + ".mp3"

    return filename


def get_video_info(url: str) -> dict:
    """
    Fetches video metadata WITHOUT downloading it.
    Used to show title, thumbnail, duration etc. on the frontend.
    """
    ydl_opts = {"quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),  # in seconds
            "uploader": info.get("uploader"),
        }