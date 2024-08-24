from flask import Flask, request, jsonify, send_file, redirect, url_for, abort
from datetime import datetime
import uuid
import os
import subprocess
import psutil

# croppingg polygon and find area
from polygon_to_tiff import TiffFactory
tiff_factory = TiffFactory()

# manage tasks for landuse detection engine on DB
from manage_task import TaskMonitoring
task_monitoring = TaskMonitoring()

# path for landuse detection engine
# Edit python path amd ai resiltd path
# PYTHON_PATH = "/usr/local/bin/python"
# ai_results = "./ai_results"
PYTHON_PATH = "/opt/miniconda3/bin/python"
ai_results = "/Users/rawinnipha/Nectec_Trainee-Test local/Postgis_Raster_API/ai_results"

app = Flask(__name__)

# Edit UPLOAD_FOLDER path
# UPLOAD_FOLDER = 'tiff_results/'
UPLOAD_FOLDER = '/Users/rawinnipha/Nectec_Trainee-Test1/Postgis_Raster_API/tiff_results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/download/', methods=['POST'])
def tiff_output():
    try:
        data = request.get_json()       
        polygon_coords = data.get('polygon_coords')
        result = tiff_factory.polygon_to_geotiff(polygon_coords)
        filename = result[0]
        status = result[1]
        if filename == None:
            return jsonify({"Error": status}), 422
        elif filename == 'x':
            return redirect(url_for('create_file'))
        else:
            file_url = url_for('get_tiff', filename=filename)
            plant_area = tiff_factory.polygon_to_area(polygon_coords)
            out_of_raster = tiff_factory.out_raster_area(polygon_coords)
            return jsonify(
                {
                    "status": status,
                    "result": {
                        "raster": file_url,
                        "stats": {
                            "area": {
                                "rice": plant_area[1],
                                "sugarcane": plant_area[2],
                                "other": plant_area[0],
                                "out_of_raster": out_of_raster
                            },
                            "area_unit": "m²"
                        }
                    },
                    "input_polygon": polygon_coords
                }
            )

    except Exception as e:
        return jsonify({'Error': 'An unexpected error occurred', 'details': str(e)}), 400

@app.route('/downloads/<filename>')
def get_tiff(filename):
    try:
        tiff_path = f'/Users/rawinnipha/Nectec_Trainee-Test local/Postgis_Raster_API/tiff_results/{filename}'
    
        # tiff_path = f'/app/tiff_results/{filename}'
        return send_file(tiff_path, as_attachment=True, mimetype='image/tiff')
    except FileNotFoundError:
        abort(404, description="File not found")

# Start use Landuse Detect Classification.
@app.route('/detect_land/createfile')
def create_file():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    uid = uuid.uuid4()
    filename = f"{timestamp}_{uid}.txt"
    file_path = os.path.join(ai_results, filename)

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

@app.route('/detect_land/status')
def status():

    finished_file = task_monitoring.check_finished_status()

    for f in finished_file:
        action = url_for('download_file', filename=f[0])
        if os.path.exists(os.path.join(ai_results, f[0])):
            task_monitoring.finished_creation(f, action)
            print(f'{f[0]} finished')
        elif os.path.exists(os.path.join(ai_results, f[0]+'.tmp')):
            print(f'{f[0]} still running')

    tasks = task_monitoring.display_tasks()
    formatted_data = [
        {
            "id": row[0],
            "pid": row[1], 
            "filename": row[2], 
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

@app.route('/detect_land/downloads/<filename>')
def download_file(filename):
    filepath = os.path.join(ai_results, filename)
    return send_file(filepath, as_attachment=True, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)