import youtube_dl
import sys
import os

class MyLogger(object):
    def debug(self, msg):
        if "ENABLE_DEBUG_LOG" in os.environ:
            print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def build_ydl_opts(path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio',
        'logger': MyLogger(),
        'outtmpl': path + '%(title)s.%(ext)s'
    }
    return ydl_opts

def download(url, path):
    ydl_opts = build_ydl_opts(path)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
