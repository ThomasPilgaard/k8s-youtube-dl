import datetime
import requests
import sys
import json
import pytz

class YoutubeDlWorker:
    def __init__(self, worker):
        self.pid = worker.pid
        self.hostname = worker.hostname
        self.state = worker.state
        self.current_job = worker.get_current_job()
        self.last_heartbeat = self.format_date(worker.last_heartbeat)
        self.successful_job_count = worker.successful_job_count
        self.failed_job_count = worker.failed_job_count
        self.video_title = self.check_for_job(self.current_job)

    def format_date(self, date):
        if date is not None:
            date_with_timestamp = pytz.utc.localize(date)
            local_time = date_with_timestamp.astimezone()
            return local_time.strftime("%d-%m-%Y %H:%M:%S")

    def check_for_job(self, job):
        if job is not None:
            return self.get_youtube_titel(job.args[0])

    def get_youtube_titel(self, url):
        url_parts = url.split('=')
        if len(url_parts) > 1:
            video_id = url_parts[1]
            url = f"https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={video_id}"
            r = requests.get(url)
            json_data = json.loads(r.text)
            return json_data["title"]
