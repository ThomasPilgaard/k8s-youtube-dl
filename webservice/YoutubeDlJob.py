import datetime
import requests
import sys
import json
import pytz

class YoutubeDlJob:
    def __init__(self, job):
        self.id = job.id
        self.url = job.args[0]
        self.path = job.args[1]
        self.status = job.get_status()
        self.error_msg = job.exc_info
        self.enqueued_at = self.format_date(job.enqueued_at)
        self.started_at = self.format_date(job.started_at)
        self.ended_at = self.format_date(job.ended_at)
        self.video_title = self.get_youtube_titel(self.url)

    def format_date(self, date):
        if date is not None:
            date_with_timestamp = pytz.utc.localize(date)
            local_time = date_with_timestamp.astimezone()
            return local_time.strftime("%d-%m-%Y %H:%M:%S")

    def get_youtube_titel(self, url):
        url_parts = url.split('=')
        if len(url_parts) > 1:
            video_id = url_parts[1]
            url = f"https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={video_id}"
            r = requests.get(url)
            json_data = json.loads(r.text)
            return json_data["title"]
