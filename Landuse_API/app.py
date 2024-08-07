from flask import Flask, jsonify, send_file, url_for
from datetime import datetime
import uuid
import os
import subprocess

import psutil

from multiprocess import *
from manage_task import TaskMonitoring

PYTHON_PATH = "/usr/local/bin/python"
results_dir = "./results"

app = Flask(__name__)

task_monitoring = TaskMonitoring()

@app.route('/')
def index():
    return jsonify({"Hello": "World!"})

def generate_filename():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    uid = uuid.uuid4()
    filename = f"{timestamp}_{uid}.txt"
    return filename

@app.route('/createfile', methods=['POST'])
def create_file():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = generate_filename()
    file_path = os.path.join(results_dir, filename)

    process = subprocess.Popen([PYTHON_PATH, "fake_landuse_classification.py", "--filename", file_path])
    # process.wait()
    pid = process.pid
    action = url_for('terminate_process', pid=pid)
    print("script executed. pid:",pid)
    task_monitoring.add_task(pid, filename, action)

    return jsonify(
        {
            "status": 'Start creating a file',
            "file": {
                "filename": filename,
                "pid": pid,
                "cancel": action,
                "timestamp": timestamp
            }
        }
    )

@app.route('/status')
def status():

    finished_file = task_monitoring.check_finished_status()

    for f in finished_file:
        action = url_for('download_file', filename=f[0])
        if os.path.exists(os.path.join(results_dir, f[0])):
            task_monitoring.finished_creation(f, action)
            print(f'{f[0]} finished')
        elif os.path.exists(os.path.join(results_dir, f[0]+'.tmp')):
            print(f'{f[0]} still running')



    tasks = task_monitoring.display_tasks()
    formatted_data = [
        {
            "id": row[0],
            "pid": row[1],  # filename
            "filename": row[2],  # size
            "status": row[3],
            "action": row[4],
            "timestamp": row[5].strftime("%Y%m%d-%H%M%S")
        }
        for row in tasks
    ]
    return jsonify(formatted_data)

@app.route('/cancel/<pid>')
def terminate_process(pid):
    pidi = int(pid)
    try:
        process = psutil.Process(pidi)
        if process.is_running():
            process.terminate() 
            process.wait(timeout=3)
            task_monitoring.cancel_file_creation(pidi)  
            if process.is_running():
                process.kill() 
            print(f"Process with PID {pid} has been terminated.")
            status = f"Process with PID {pid} has been terminated."
            print(status)
        else:
            status = f"Process with PID {pid} is not running."
            print(status)
    except psutil.NoSuchProcess:
        status = f"No such process with PID {pid}."
        print(status)
    except psutil.AccessDenied:
        status = f"Permission denied to terminate process with PID {pid}."
        print(status)
    except psutil.TimeoutExpired:
        status = f"Timeout expired while waiting for process with PID {pid} to terminate."
        print(status)
    return jsonify(
        {
                "status": status
        }
    )

@app.route('/running')
def is_process_running():
    pid = 104
    try:
        process = psutil.Process(pid)
        return f'{process.is_running()}'
    except psutil.NoSuchProcess:
        return 'False'

    
@app.route('/downloads/<filename>')
def download_file(filename):
    filepath = os.path.join(results_dir, filename)
    return send_file(filepath, as_attachment=True, mimetype='text/plain')

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)