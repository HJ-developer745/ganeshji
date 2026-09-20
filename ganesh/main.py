"""
YouTube Video Downloader (Single File)
----------------------------------------
A simple desktop app to download YouTube videos using yt-dlp + Tkinter.

REQUIREMENTS (install once):
    pip install yt-dlp

Then just run:
    python youtube_downloader.py

Features:
- Paste a YouTube URL and fetch available quality options
- Choose video quality (or audio-only MP3)
- Choose download folder
- Live progress bar + speed/ETA
- Works fully offline after install (no browser needed)

NOTE: Only download videos you own, have permission to download,
or that are licensed for download (e.g. Creative Commons, your own
uploads). Respect YouTube's Terms of Service and copyright law.
"""

import os
import sys
import shutil
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    import yt_dlp
except ImportError:
    print("yt-dlp is not installed. Run:  pip install yt-dlp")
    sys.exit(1)


def ffmpeg_available():
    """Check if ffmpeg is installed and on PATH.
    Without it, yt-dlp cannot merge separate video+audio streams
    or convert audio to MP3 (common issue on Android/Pydroid)."""
    return shutil.which("ffmpeg") is not None


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("560x420")
        self.root.resizable(False, False)

        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.formats = []          # list of (format_id, label)
        self.video_info = None
        self.has_ffmpeg = ffmpeg_available()

        self._build_ui()

        if not self.has_ffmpeg:
            self.status_var.set(
                "Note: ffmpeg not found - only single-file (progressive) "
                "qualities available, usually up to 720p, and audio will "
                "save as M4A/WebM instead of MP3."
            )

    # ---------------------------------------------------------- UI LAYOUT
    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}

        title = tk.Label(self.root, text="YouTube Video Downloader",
                          font=("Segoe UI", 16, "bold"))
        title.pack(pady=(14, 4))

        # URL entry row
        url_frame = tk.Frame(self.root)
        url_frame.pack(fill="x", **pad)

        tk.Label(url_frame, text="Video URL:").pack(side="left")
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(url_frame, textvariable=self.url_var, width=40)
        self.url_entry.pack(side="left", padx=8, fill="x", expand=True)

        self.fetch_btn = tk.Button(url_frame, text="Fetch Info", command=self.fetch_info)
        self.fetch_btn.pack(side="left")

        # Title / status label
        self.title_label = tk.Label(self.root, text="", wraplength=520,
                                     fg="#2563eb", font=("Segoe UI", 10, "bold"))
        self.title_label.pack(**pad)

        # Quality selector
        quality_frame = tk.Frame(self.root)
        quality_frame.pack(fill="x", **pad)

        tk.Label(quality_frame, text="Quality:").pack(side="left")
        self.quality_var = tk.StringVar()
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var,
                                           state="readonly", width=45)
        self.quality_combo.pack(side="left", padx=8)

        # Audio-only checkbox
        self.audio_only_var = tk.BooleanVar()
        audio_label = "Audio only (MP3)" if ffmpeg_available() else "Audio only (M4A/WebM - ffmpeg missing)"
        audio_check = tk.Checkbutton(self.root, text=audio_label,
                                      variable=self.audio_only_var)
        audio_check.pack(anchor="w", padx=12)

        # Folder picker
        folder_frame = tk.Frame(self.root)
        folder_frame.pack(fill="x", **pad)

        tk.Label(folder_frame, text="Save to:").pack(side="left")
        self.folder_var = tk.StringVar(value=self.download_folder)
        tk.Entry(folder_frame, textvariable=self.folder_var, width=38).pack(
            side="left", padx=8, fill="x", expand=True)
        tk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side="left")

        # Download button
        self.download_btn = tk.Button(self.root, text="Download", bg="#2563eb",
                                       fg="white", font=("Segoe UI", 11, "bold"),
                                       command=self.start_download, state="disabled")
        self.download_btn.pack(pady=14)

        # Progress bar + status
        self.progress = ttk.Progressbar(self.root, length=500, mode="determinate")
        self.progress.pack(pady=4)

        self.status_var = tk.StringVar(value="Paste a YouTube URL and click 'Fetch Info'.")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, fg="#555")
        self.status_label.pack(pady=4)

    # ---------------------------------------------------------- ACTIONS
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)

    def fetch_info(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please paste a YouTube URL first.")
            return

        self.fetch_btn.config(state="disabled")
        self.status_var.set("Fetching video info...")
        threading.Thread(target=self._fetch_info_thread, args=(url,), daemon=True).start()

    def _fetch_info_thread(self, url):
        try:
            ydl_opts = {"quiet": True, "no_warnings": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            self.video_info = info
            formats = info.get("formats", [])

            seen = set()
            options = []
            for f in formats:
                if f.get("vcodec") == "none":
                    continue  # skip audio-only streams here, handled by checkbox

                is_progressive = f.get("acodec") != "none"  # already has audio baked in
                if not self.has_ffmpeg and not is_progressive:
                    continue  # can't merge separate streams without ffmpeg

                height = f.get("height")
                ext = f.get("ext")
                filesize = f.get("filesize") or f.get("filesize_approx")
                if not height:
                    continue
                label_key = (height, ext)
                if label_key in seen:
                    continue
                seen.add(label_key)
                size_mb = f"{filesize / 1_048_576:.1f}MB" if filesize else "size unknown"
                tag = "" if is_progressive else " [needs merge]"
                label = f"{height}p ({ext}, {size_mb}){tag}"
                options.append((f["format_id"], label, height))

            options.sort(key=lambda x: x[2], reverse=True)
            self.formats = [(fid, label) for fid, label, _ in options]

            self.root.after(0, self._update_after_fetch, info.get("title", "Unknown title"))
        except Exception as e:
            self.root.after(0, self._fetch_error, str(e))

    def _update_after_fetch(self, title):
        self.title_label.config(text=f"\u25b6 {title}")
        labels = [label for _, label in self.formats] or ["Best available quality"]
        self.quality_combo["values"] = labels
        if labels:
            self.quality_combo.current(0)
        self.fetch_btn.config(state="normal")
        self.download_btn.config(state="normal")
        if self.has_ffmpeg:
            self.status_var.set("Ready to download.")
        else:
            self.status_var.set(
                "Ready (ffmpeg not found - showing single-file qualities only, "
                "usually max 720p)."
            )

    def _fetch_error(self, message):
        self.fetch_btn.config(state="normal")
        self.status_var.set("Failed to fetch video info.")
        messagebox.showerror("Error", f"Could not fetch video info:\n{message}")

    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            return

        self.download_btn.config(state="disabled")
        self.fetch_btn.config(state="disabled")
        self.progress["value"] = 0
        self.status_var.set("Starting download...")

        threading.Thread(target=self._download_thread, args=(url,), daemon=True).start()

    def _progress_hook(self, d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            speed = d.get("speed")
            eta = d.get("eta")
            if total:
                pct = downloaded / total * 100
                self.root.after(0, self._update_progress, pct, speed, eta)
        elif d["status"] == "finished":
            self.root.after(0, lambda: self.status_var.set("Processing file..."))

    def _update_progress(self, pct, speed, eta):
        self.progress["value"] = pct
        speed_str = f"{speed / 1_048_576:.1f} MB/s" if speed else "..."
        eta_str = f"{eta}s" if eta else "..."
        self.status_var.set(f"Downloading: {pct:.1f}% | {speed_str} | ETA {eta_str}")

    def _download_thread(self, url):
        try:
            os.makedirs(self.folder_var.get(), exist_ok=True)
            outtmpl = os.path.join(self.folder_var.get(), "%(title)s.%(ext)s")

            if self.audio_only_var.get():
                if self.has_ffmpeg:
                    ydl_opts = {
                        "format": "bestaudio/best",
                        "outtmpl": outtmpl,
                        "postprocessors": [{
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }],
                        "progress_hooks": [self._progress_hook],
                        "quiet": True,
                        "no_warnings": True,
                    }
                else:
                    # No ffmpeg -> can't convert to MP3, save best raw audio file as-is
                    ydl_opts = {
                        "format": "bestaudio/best",
                        "outtmpl": outtmpl,
                        "progress_hooks": [self._progress_hook],
                        "quiet": True,
                        "no_warnings": True,
                    }
            else:
                selected_label = self.quality_var.get()
                format_id = None
                for fid, label in self.formats:
                    if label == selected_label:
                        format_id = fid
                        break

                if self.has_ffmpeg:
                    fmt = f"{format_id}+bestaudio/best" if format_id else "bestvideo+bestaudio/best"
                    ydl_opts = {
                        "format": fmt,
                        "outtmpl": outtmpl,
                        "merge_output_format": "mp4",
                        "progress_hooks": [self._progress_hook],
                        "quiet": True,
                        "no_warnings": True,
                    }
                else:
                    # No ffmpeg -> use the exact progressive format (already has audio),
                    # no merging needed at all
                    fmt = format_id if format_id else "best[acodec!=none]"
                    ydl_opts = {
                        "format": fmt,
                        "outtmpl": outtmpl,
                        "progress_hooks": [self._progress_hook],
                        "quiet": True,
                        "no_warnings": True,
                    }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.root.after(0, self._download_done)
        except Exception as e:
            self.root.after(0, self._download_error, str(e))

    def _download_done(self):
        self.progress["value"] = 100
        self.status_var.set("Download complete!")
        self.download_btn.config(state="normal")
        self.fetch_btn.config(state="normal")
        messagebox.showinfo("Done", f"Download saved to:\n{self.folder_var.get()}")

    def _download_error(self, message):
        self.status_var.set("Download failed.")
        self.download_btn.config(state="normal")
        self.fetch_btn.config(state="normal")
        messagebox.showerror("Error", f"Download failed:\n{message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
