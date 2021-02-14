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

ydl_opts = {
    'format': 'bestvideo+bestaudio',
    'logger': MyLogger(),
}

def download(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
