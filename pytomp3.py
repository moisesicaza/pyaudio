#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import threading
import tkinter as tk
import youtube_dl
from tkinter import ttk, Frame, END
from tkinter import messagebox
from tkinter import Menu


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
        # Attributes
        self.download_option_value = 1
        self.ydl_opts = {
            'format': '',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [],
            'logger': CustomLogger(),
            'progress_hooks': [self.progress_hook],
        }

        # Tkinter widget instances
        self.root = tk.Tk()
        self.top_frame = Frame(self.root)
        self.bottom_frame = Frame(self.root)
        self.youtube_url = tk.StringVar()
        self.label = ttk.Label(self.top_frame)
        self.entry = ttk.Entry(self.top_frame)
        self.button = ttk.Button(self.top_frame)
        self.progress_bar = ttk.Progressbar(self.bottom_frame)
        self.menu_bar = Menu(self.root, tearoff=0)
        self.option_menu = Menu(self.root, tearoff=0)
        self.download_option = Menu(self.root)

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

        # Menu bar
        self.menu_bar.add_cascade(label="Options", menu=self.option_menu)
        self.option_menu.add_cascade(label="Download options", menu=self.download_option)
        self.download_option.add_radiobutton(label="Only audio (.mp3)", command=lambda: self.set_download_option(1))
        self.download_option.add_radiobutton(label="Only video (.mp4)", command=lambda: self.set_download_option(2))

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
        self.root.config(menu=self.menu_bar)
        self.root.mainloop()

    def run_process(self):
        """ Executes the download process in a separate thread.
        :return: void
        """
        threading.Thread(target=self.convert_video).start()

    def progress_hook(self, data):
        """ Hook of the process progress.
        :param data: Data structure of the process.
        :return: void.
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
            ydl_opts = self.get_ydl_options()

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

    def get_ydl_options(self):
        """ Returns the youtbe-dl module options
            Option 1 = mp3 file.
            Option 2 = mp4 file.
        :returns dict.
        """
        if self.download_option_value == 1:
            self.ydl_opts['format'] = 'bestaudio/best'
            self.ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        elif self.download_option_value == 2:
            self.ydl_opts['format'] = 'bestvideo/best'
            self.ydl_opts['postprocessors'] = []

        return self.ydl_opts

    def set_download_option(self, value):
        """ Sets the option of download (mp3, mp4 formats).
        :param value: Option number
        :return: void.
        """
        self.download_option_value = value

