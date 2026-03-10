import os
import yt_dlp

def get_cookie_file():
    # Path relative to this file's location
    cookie_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies.txt")
    if os.path.exists(cookie_path):
        return cookie_path
    return None

def get_ydl_opts(format: str, quality: str, output_path: str) -> dict:
    cookie_file = get_cookie_file()

    opts = {
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "quiet": True,
    }

    # Add cookies if available
    if cookie_file:
        opts["cookiefile"] = cookie_file

    if format == "mp3":
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        if quality == "best":
            opts["format"] = "bestvideo+bestaudio/best"
        else:
            opts["format"] = f"bestvideo[height<={quality}]+bestaudio/best"
        opts["merge_output_format"] = "mp4"

    return opts