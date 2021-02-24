import datetime
import requests
import sys
import json

class YoutubeDlWorker:
    def __init__(self, worker):
        self.pid = worker.pid
        self.hostname = worker.hostname
        self.state = worker.state
        self.current_job = worker.get_current_job()
        self.last_heartbeat = self.formatDate(worker.last_heartbeat)
        self.successful_job_count = worker.successful_job_count
        self.failed_job_count = worker.failed_job_count
        self.video_title = self.test(self.current_job)

    def formatDate(self, date):
        if date is not None:
            return date.strftime("%d-%m-%Y %H:%M:%S")

    def test(self, job):
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
