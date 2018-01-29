#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import threading
import tkinter as tk
import youtube_dl
from tkinter import ttk, Frame, END
from tkinter import messagebox


class CustomLogger:
    """ Custom class for the logger of the youtube_dl process. """
    def debug(self, msg):
        """ Debug log.
        :param msg: Message of the debug.
        :return: void.
        """
        pass

    def warning(self, msg):
        """ Warning log.
        :param msg: Message of the debug.
        :return: void.
        """
        messagebox.showwarning("Warning", msg)

    def error(self, msg):
        """ Error log.
        :param msg: Messages de error.
        :return: void.
        """
        messagebox.showerror("Error", msg)


class PyToMp3:
    """ Class to convert videos from youtube.com to mp3. """
    def __init__(self):
        """ Constructor of the class """
        # Tkinter widget instances
        self.root = tk.Tk()
        self.top_frame = Frame(self.root)
        self.bottom_frame = Frame(self.root)
        self.youtube_url = tk.StringVar()
        self.label = ttk.Label(self.top_frame)
        self.entry = ttk.Entry(self.top_frame)
        self.button = ttk.Button(self.top_frame)
        self.progress_bar = ttk.Progressbar(self.bottom_frame)

    def config_gui(self):
        """ Setting options for widgets
        :return: void
        """
        # Window settings
        self.root.title("PyTomp3")
        self.root.geometry("500x100")

        # Widgets
        self.label.config(text="YouTube URL:")
        self.entry.config(width=40, textvariable=self.youtube_url)
        self.button.config(text="Convert", command=self.run_process)
        self.progress_bar.config(orient="horizontal", length=400, mode="determinate")

    def layout(self):
        """ Setting options for position of widgets in the surface.
        :return: void
        """
        self.label.pack(side='left', ipady=15)
        self.entry.pack(side='left')
        self.button.pack(side='left')
        self.top_frame.pack(side='top')
        self.progress_bar.pack(side='bottom')
        self.bottom_frame.pack(side='bottom')

    def run(self):
        """ Runs the GUI.
        :return: void
        """
        self.config_gui()
        self.layout()
        self.root.mainloop()

    def run_process(self):
        """ Executes the download process in a separate thread.
        :return: void
        """
        threading.Thread(target=self.convert_video).start()

    def progress_hook(self, data):
        """ Hook of the process progress.
        :param data: Data structure of the process.
        :return:
        """
        if data['status'] == 'finished':
            self.entry.delete(0, END)
            self.progress_bar["value"] = 0
            self.progress_bar.update_idletasks()
            messagebox.showinfo("Info", 'Process finished.')

        elif data['status'] == 'downloading':
            percent = data['_percent_str'].replace('%', '')
            self.progress_bar["value"] = int(float(percent))
            self.progress_bar.update_idletasks()

    def convert_video(self):
        """ Converts the video form youtube.com url.
        :return: void.
        """
        url = self.youtube_url.get()
        regex = r"^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+"

        if not re.search(regex, url):
            messagebox.showerror("Error", "This is not a valid Youtube URL")

        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'logger': CustomLogger(),
                'progress_hooks': [self.progress_hook],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
