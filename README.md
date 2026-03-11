# ytdrop

> paste a link. pick a format. done.

---

## Requirements

- Python 3.11+
- ffmpeg -> `sudo apt install ffmpeg` (Linux) / `brew install ffmpeg` (Mac)

---

## Setup

```bash
cd backend
pip install -r requirements.txt
```

Drop your `cookies.txt` (exported from browser while logged into YouTube) into the `backend/` folder.

---

## Run

```bash
cd backend
python -m uvicorn main:app --reload
```

Then open `frontend/index.html` in your browser.

---

## Project Structure

```
yt-downloader/
├── backend/
│   ├── main.py            # FastAPI app & routes
│   ├── downloader.py      # yt-dlp download logic
│   ├── requirements.txt   # Python dependencies
│   └── cookies.txt        # your YouTube cookies (not committed)
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

---

> For personal use only -- respect copyright and YouTube's Terms of Service.