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

#def my_hook(d):
#    #print(d)
#    if d['status'] == 'finished':
#        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestvideo+bestaudio',
    'logger': MyLogger(),
    #'progress_hooks': [my_hook],
}

def download(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

#download("https://www.youtube.com/watch?v=3muR5gB8x2o")
#download("test")