// API base — backend running locally
const API_BASE = "http://localhost:8000";

const urlInput = document.getElementById("url-input");
const previewBtn = document.getElementById("preview-btn");
const previewBox = document.getElementById("preview-box");
const previewThumb = document.getElementById("preview-thumb");
const previewTitle = document.getElementById("preview-title");
const previewUpload = document.getElementById("preview-uploader");
const previewDur = document.getElementById("preview-duration");
const downloadBtn = document.getElementById("download-btn");
const btnLabel = document.getElementById("btn-label");
const statusEl = document.getElementById("status");
const statusText = document.getElementById("status-text");
const spinner = document.getElementById("spinner");
const qualityGroup = document.getElementById("quality-group");
const qualitySelect = document.getElementById("quality-select");
const fmtMp4 = document.getElementById("fmt-mp4");
const fmtMp3 = document.getElementById("fmt-mp3");

let selectedFormat = "mp4";

fmtMp4.addEventListener("click", () => {
  selectedFormat = "mp4";
  fmtMp4.classList.add("active");
  fmtMp3.classList.remove("active");
  qualityGroup.style.display = "flex";
});

fmtMp3.addEventListener("click", () => {
  selectedFormat = "mp3";
  fmtMp3.classList.add("active");
  fmtMp4.classList.remove("active");
  qualityGroup.style.display = "none";
});

function formatDuration(seconds) {
  if (!seconds) return "Unknown duration";
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  if (h > 0)
    return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  return `${m}:${String(s).padStart(2, "0")}`;
}

function showStatus(message, type = "loading") {
  statusEl.className = "status";
  statusEl.classList.remove("hidden");

  if (type === "loading") {
    spinner.classList.remove("hidden");
    statusEl.classList.add("loading");
  } else {
    spinner.classList.add("hidden");
  }

  if (type === "error") statusEl.classList.add("error");
  if (type === "success") statusEl.classList.add("success");

  statusText.textContent = message;
}

function hideStatus() {
  statusEl.classList.add("hidden");
}

previewBtn.addEventListener("click", async () => {
  const url = urlInput.value.trim();

  if (!url) {
    showStatus("Please paste a YouTube URL first.", "error");
    return;
  }

  showStatus("Fetching video info...", "loading");
  previewBox.classList.add("hidden");

  try {
    const res = await fetch(`${API_BASE}/info?url=${encodeURIComponent(url)}`);
    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Failed to fetch info");

    previewThumb.src = data.thumbnail;
    previewTitle.textContent = data.title;
    previewUpload.textContent = data.channel;
    previewDur.textContent = formatDuration(data.duration);
    previewBox.classList.remove("hidden");
    hideStatus();
  } catch (err) {
    showStatus("Error: " + err.message, "error");
  }
});

downloadBtn.addEventListener("click", async () => {
  const url = urlInput.value.trim();

  if (!url) {
    showStatus("Please paste a YouTube URL first.", "error");
    return;
  }

  const quality = qualitySelect.value;

  btnLabel.textContent = "Downloading...";
  downloadBtn.disabled = true;
  showStatus("Downloading... this may take a moment.", "loading");

  try {
    const res = await fetch(`${API_BASE}/download`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, format: selectedFormat, quality }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Download failed");
    }

    const blob = await res.blob();
    const disposition = res.headers.get("content-disposition");
    let filename = "download." + selectedFormat;
    if (disposition) {
      const match = disposition.match(/filename="?([^"]+)"?/);
      if (match) filename = match[1];
    }

    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);

    showStatus("Downloaded: " + filename, "success");
  } catch (err) {
    showStatus("Error: " + err.message, "error");
  } finally {
    btnLabel.textContent = "Download";
    downloadBtn.disabled = false;
  }
});