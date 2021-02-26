from redis import Redis
from rq import Queue, Connection, Worker
from rq.command import send_stop_job_command
from rq.job import Job
import os
import downloader
from flask import Flask, render_template, request, escape, redirect, url_for
import sys
import YoutubeDlJob
import YoutubeDlWorker
from flask_fontawesome import FontAwesome
import subprocess
import glob

redis_queue_name = os.getenv('YOUTUBE_QUEUE_NAME')
redis_path = os.getenv('REDIS_PATH')
youtube_folder_path = os.getenv('YOUTUBE_STORAGE_MOUNT_PATH')

conn = Redis.from_url(redis_path)

app = Flask(__name__)
fa = FontAwesome(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/download', methods = ['POST'])
def download():
    url = request.form['youtube-url']
    path = request.form['file-path']

    if path and path.startswith('/'):
        path = path[1:]

    if path and not path.endswith('/'):
        path = path + "/"

    full_path = youtube_folder_path + path

    with Connection(conn):
        q = Queue(redis_queue_name, connection=conn)
        result = q.enqueue(downloader.download, args=(url,full_path,), job_timeout=18000, **{'result_ttl':259200})
    return redirect(url_for('index'))

@app.route('/jobs', methods=['GET'])
def jobs():
    with Connection(conn):
        q = Queue(redis_queue_name, connection=conn)
        workers = Worker.all(queue=q)
        failed_jobs = get_failed_jobs(q)
        enqueued_jobs = get_enqueued_jobs(q)
        running_jobs = get_running_jobs(workers)
        finished_jobs = get_finished_jobs(q)
        all_jobs = failed_jobs + enqueued_jobs + running_jobs + finished_jobs
    return render_template('jobs.html', jobs = all_jobs)

@app.route('/showerror/<id>', methods=['GET'])
def show_error(id):
    with Connection(conn):
        q = Queue(redis_queue_name, connection=conn)
        failed_jobs = get_failed_jobs(q)
        youtube_job = next((x for x in failed_jobs if x.id == id), None)
    return render_template('errormessage.html', job=youtube_job)

@app.route('/folderstructure', methods=['GET'])
def folder_structure():
    folders_byte = subprocess.run(['tree', youtube_folder_path, '-d'], stdout=subprocess.PIPE)
    folders = folders_byte.stdout.decode("utf-8")
    return render_template('yt-folders.html', folders=folders.rsplit("\n",3)[0])

@app.route('/deletefailedjob/<id>', methods=['GET'])
def delete_failed_job(id):
        with Connection(conn):
            job = get_job(id, conn)
            if job.path is not None and job.video_title is not None:
                file_name = os.path.normpath(job.path + job.video_title)
                delete_job_on_system(file_name)
            q = Queue(redis_queue_name, connection=conn)
            remove_failed_job(q, id)
        return redirect(url_for('jobs'))

@app.route('/requeuejob/<id>', methods=['GET'])
def requeue_job(id):
    with Connection(conn):
        q = Queue(redis_queue_name, connection=conn)
        requeue_failed_job(q, id)
    return redirect(url_for('jobs'))

@app.route('/stopjob/<id>', methods=['GET'])
def stop_job (id):
    with Connection(conn):
        send_stop_job_command(conn, id)
    return redirect(url_for('jobs'))

@app.route('/workers', methods=['GET'])
def workers ():
    with Connection(conn):
        yt_workers = []
        q = Queue(redis_queue_name, connection=conn)
        workers = Worker.all(queue=q)
        for worker in workers:
            yt_worker = YoutubeDlWorker.YoutubeDlWorker(worker)
            yt_workers.append(yt_worker)
    return render_template('workers.html', workers = yt_workers)

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

def remove_failed_job(queue, id):
    registry = queue.failed_job_registry
    registry.remove(id)

def requeue_failed_job(queue, id):
    registry = queue.failed_job_registry
    registry.requeue(id)

def get_job(id, conn):
    job = Job.fetch(id, conn)
    yt_job = YoutubeDlJob.YoutubeDlJob(job)
    return yt_job

def delete_job_on_system(file):
    files = glob.glob(file + '*')
    for file in files:
        if os.path.exists(file):
            os.remove(file)

app.run(debug=True, host='0.0.0.0')

#putte redis storage ud i et volume
