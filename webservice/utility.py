import YoutubeDlJob
import YoutubeDlWorker
from redis import Redis
from rq import Queue, Connection, Worker
from rq.command import send_stop_job_command
from rq.job import Job
import os
import glob
import subprocess
import downloader
import sys
import requests
import json
import shutil

youtube_folder_path = os.getenv('YOUTUBE_STORAGE_MOUNT_PATH')
redis_queue_name = os.getenv('YOUTUBE_QUEUE_NAME')
redis_path = os.getenv('REDIS_PATH')

conn = Redis.from_url(redis_path)

def enqueue_job(url, path):
    if path and path.startswith('/'):
        path = path[1:]

    if path and not path.endswith('/'):
        path = path + "/"

    full_path = youtube_folder_path + path

    if get_type(url) == "list":
        list_name = get_youtube_title(url)
        full_path = full_path + list_name + "/"

    with Connection(conn):
        q = Queue(redis_queue_name, connection=conn)
        result = q.enqueue(downloader.download, args=(url,full_path,), job_timeout=18000, **{'result_ttl':259200})

def get_all_jobs():
    with Connection(conn):
        q = Queue(redis_queue_name, connection=conn)
        workers = Worker.all(queue=q)
        failed_jobs = get_failed_jobs(q)
        enqueued_jobs = get_enqueued_jobs(q)
        running_jobs = get_running_jobs(workers)
        finished_jobs = get_finished_jobs(q)
        all_jobs = failed_jobs + enqueued_jobs + running_jobs + finished_jobs
        return all_jobs

def get_running_jobs(workers):
    running_jobs = []
    for worker in workers:
        job = worker.get_current_job()
        if job is not None:
            youtube_job = YoutubeDlJob.YoutubeDlJob(job)
            running_jobs.append(youtube_job)
    return running_jobs

def get_enqueued_jobs(queue):
    jobs = []
    for job in queue.jobs:
        youtube_job = YoutubeDlJob.YoutubeDlJob(job)
        jobs.append(youtube_job)
    return jobs

def get_finished_jobs(queue):
    finished_jobs = []
    registry = queue.finished_job_registry
    for job_id in registry.get_job_ids():
        job = Job.fetch(job_id, connection=conn)
        youtube_job = YoutubeDlJob.YoutubeDlJob(job)
        finished_jobs.append(youtube_job)
    return finished_jobs

def get_failed_jobs(queue):
    failed_jobs = []
    registry = queue.failed_job_registry
    for job_id in registry.get_job_ids():
        job = Job.fetch(job_id, connection=conn)
        youtube_job = YoutubeDlJob.YoutubeDlJob(job)
        failed_jobs.append(youtube_job)
    return failed_jobs

def requeue_failed_job(id):
    with Connection(conn):
        q = Queue(redis_queue_name, connection=conn)
        registry = q.failed_job_registry
        registry.requeue(id)

def get_job(id):
    with Connection(conn):
        job = Job.fetch(id, conn)
        yt_job = YoutubeDlJob.YoutubeDlJob(job)
        return yt_job

def remove_job_and_delete_files(id):
    with Connection(conn):
        job = get_job(id)
        if job.path is not None and job.video_title is not None:
            if job.type == "video":
                delete_video_files_on_system(job)
            elif job.type == "list":
                delete_list_files_on_system(job)
        q = Queue(redis_queue_name, connection=conn)
        remove_failed_job(q, id)

def remove_failed_job(queue, id):
    registry = queue.failed_job_registry
    registry.remove(id)

def delete_video_files_on_system(job):
    file_name = os.path.normpath(job.path + job.video_title)
    files = glob.glob(file_name + '*')
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def delete_list_files_on_system(job):
    path = job.path
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)

def stop_job(id):
    with Connection(conn):
        send_stop_job_command(conn, id)

def get_folder_structure():
    folders_byte = subprocess.run(['tree', youtube_folder_path, '-d'], stdout=subprocess.PIPE)
    folders = folders_byte.stdout.decode("utf-8")
    folders_without_folder_count = folders.rsplit("\n",3)[0]
    return folders_without_folder_count

def get_workers():
    with Connection(conn):
        yt_workers = []
        q = Queue(redis_queue_name, connection=conn)
        workers = Worker.all(queue=q)
        for worker in workers:
            yt_worker = YoutubeDlWorker.YoutubeDlWorker(worker)
            yt_workers.append(yt_worker)
        return yt_workers

def get_youtube_title(url):
    url = f"https://www.youtube.com/oembed?format=json&url={url}"
    r = requests.get(url)
    if r.status_code == 200:
        json_data = json.loads(r.text)
        return json_data["title"]

def get_type(url):
    if "playlist?" in url:
        return "list"
    elif "watch?" in url:
        return "video"
    else:
        return None
