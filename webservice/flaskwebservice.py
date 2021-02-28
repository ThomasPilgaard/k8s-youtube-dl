from flask import Flask, render_template, request, redirect, url_for
import sys
from flask_fontawesome import FontAwesome
import utility

app = Flask(__name__)
fa = FontAwesome(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/download', methods = ['POST'])
def download():
    url = request.form['youtube-url']
    path = request.form['file-path']

    utility.enqueue_job(url, path)
    return redirect(url_for('index'))

@app.route('/jobs', methods=['GET'])
def jobs():
    all_jobs = utility.get_all_jobs()
    return render_template('jobs.html', jobs = all_jobs)

@app.route('/showerror/<id>', methods=['GET'])
def show_error(id):
    failed_job = utility.get_job(id)
    return render_template('errormessage.html', job = failed_job)

@app.route('/folderstructure', methods=['GET'])
def folder_structure():
    folder_structure = utility.get_folder_structure()
    return render_template('yt-folders.html', folders=folder_structure)

@app.route('/deletefailedjob/<id>', methods=['GET'])
def delete_failed_job(id):
    utility.remove_job_and_delete_files(id)
    return redirect(url_for('jobs'))

@app.route('/requeuejob/<id>', methods=['GET'])
def requeue_job(id):
    utility.requeue_failed_job(id)
    return redirect(url_for('jobs'))

@app.route('/stopjob/<id>', methods=['GET'])
def stop_job (id):
    utility.stop_job(id)
    return redirect(url_for('jobs'))

@app.route('/workers', methods=['GET'])
def workers ():
    yt_workers = utility.get_workers()
    return render_template('workers.html', workers = yt_workers)

app.run(debug=True, host='0.0.0.0')

#putte redis storage ud i et volume
