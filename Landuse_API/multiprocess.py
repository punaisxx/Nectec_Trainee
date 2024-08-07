import subprocess
import os
from datetime import datetime
import uuid
import shutil
from multiprocessing import Lock, Process, Queue, current_process

PYTHON_PATH = "/opt/miniconda3/bin/python"
# PYTHON_PATH = "/usr/local/bin/python"

def write_empty_file(source_path):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    uid = uuid.uuid4()
    filename = f"{timestamp}_{uid}.txt"
    with open(source_path, 'w') as fp:
        pass
        print("create empty file")
    return filename

def check_file_exists(source_dir, des_dir):
    if os.listdir(source_dir):
        for fs in os.listdir(source_dir):
            if os.path.exists(os.path.join(des_dir, fs)) and os.path.exists(os.path.join(des_dir, fs+'.tmp')):
                print(f"{fs} already exists")
                os.remove(os.path.join(source_dir, fs))
                pass
            else:
                print(1)
                shutil.move(os.path.join(source_dir, fs), os.path.join(des_dir, fs))

    else:
        print("This director is empty.")

# def run_subprocess(filepath, results):    
#     process = subprocess.Popen([PYTHON_PATH, "fake_landuse_classification.py", "--filename", filepath], shell=True, stdout=subprocess.PIPE)

#     pid = process.pid
#     results.append(pid)
#     print("script executed. pid:",pid)
    
#     return pid

# def list_file(des_dir):
#     files = [os.path.join(des_dir, f) for f in os.listdir(des_dir) if os.path.isfile(os.path.join(des_dir, f))]
#     print(files)

def main():
    des_dir = 'destination_dir/'
    source_dir = 'source_dir/'
    results_dir = 'results/'
    results = []

    filename = generate_filename()
    write_empty_file(os.path.join(source_dir, filename))
    
    check_file_exists(source_dir, des_dir)
    for f in os.listdir(des_dir):
        run_subprocess(f, results)
        shutil.move(os.path.join(des_dir, f), os.path.join(results_dir, f))

if __name__ == "__main__":
    main()
    # num_workers = os.cpu_count()
    # print(num_workers)
    # print(type(generate_filename()))