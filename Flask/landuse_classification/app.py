from flask import Flask, request, jsonify, send_file, render_template, url_for
from datetime import datetime
import uuid
import os
import asyncio

import landuse_classification
import fake_landuse_classification
from files_status import classified_files



app = Flask(__name__)
loop = asyncio.get_event_loop()

@app.route('/')
def index():
    return jsonify({"Hello": "World!"})

@app.route('/test')
def test():
    # return json.dumps(classified_files)
    # print("Using jsonify")
    # users = [{'id': 1, 'username': 'sweety'},
    #          {'id': 2, 'username': 'pallavi'}]
    str_obj = classified_files
    # output = {
    #     'status': dict_obj
    # }
    # resp = jsonify(output)
    # resp.status_code = 200
    return jsonify(str_obj)

# API 1 create file
def generate_filename():
        # dir = "results"
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        uid = uuid.uuid4()
        filename = f"{timestamp}_{uid}.txt"
        # file_path = os.path.join(dir, filename)
        return filename, uid, timestamp

@app.route('/download', methods=['POST'])
def create_file():
    file_data = generate_filename()
    # filename = file_data[0]
    dir = 'results/'
    file_path = os.path.join(dir, file_data[0])
    # task = loop.create_task(fake_landuse_classification.main(['--filename', file_path]))
    fake_landuse_classification.main(['--filename', file_path])
    # return jsonify({'task_id': id(task)}), 202
    print("script executed.")
    return jsonify(
        {
            "x": "..."
        }
    )

# @app.route('/download', methods=['POST'])
# def create_file():
#     filename = landuse_classification.main()
#     file_url = url_for('download_file', filename=filename)
#     return jsonify(
#         {
#             "filename": filename,
#             "URL": file_url
#         }
#     )
    
# @app.route('/downloads/<filename>')
# def download_file(filename):
#     tiff_path = f'/app/landuse_classification/results/{filename}'
#     return send_file(tiff_path, as_attachment=True, mimetype='image/tiff')

# @app.route("/delete/<filename>", methods=["DELETE"])
# def delete_file(filename):
#     return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)