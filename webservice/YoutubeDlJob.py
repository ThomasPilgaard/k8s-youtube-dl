import datetime

class YoutubeDlJob:
    def __init__(self, job_id, youtube_link, job_status, exc_info, enqueued_at, started_at, ended_at):
        self.id = job_id
        self.url = youtube_link
        self.status = job_status
        self.error_msg = exc_info
        self.enqueued_at = self.formatDate(enqueued_at)
        self.started_at = self.formatDate(started_at)
        self.ended_at = self.formatDate(ended_at)

    def formatDate(self, date):
        if date is not None:
            return date.strftime("%d-%m-%Y %H:%M:%S")