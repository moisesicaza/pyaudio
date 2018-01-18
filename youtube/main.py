from __future__ import unicode_literals
import youtube_dl

# Required Tkinter module for GUI
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    raise SystemExit("The Tkinter module is required for the graphical interface")

# Tkinter window object
window = tk.Tk()

# Variable for storage URL
youtube_url = tk.StringVar()

# Progress bar widget
progress_bar = ttk.Progressbar(window, orient="horizontal", length=200, mode="determinate")


# Hook for progress of the process
def hook(progress):
    global progress_bar
    print(progress['status'])
    if progress['status'] == 'downloading':
        progress_bar["value"] = progress['_percent_str'].replace('%', '')
        progress_bar.update_idletasks()


# Convert video to mp3 format
def convert():
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [hook]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url.get()])


# Launcher of the application
def run():
    # Window settings
    window.title("PyTomp3")
    window.geometry("400x100")
    window.resizable(0, 0)

    # Widgets
    label = tk.Label(window, text="YouTube URL:")
    entry = tk.Entry(window, width=38, textvariable=youtube_url)
    button = tk.Button(window, text="Convert", command=convert)

    # Layout
    label.grid(row=0, column=1, padx=5)
    entry.grid(row=0, column=2, padx=5)
    button.grid(row=0, column=3, pady=10)
    progress_bar.grid(row=1, rowspan=2, columnspan=5)

    window.mainloop()
