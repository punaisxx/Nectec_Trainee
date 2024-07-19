from flask import Flask, request, jsonify, send_file, render_template, url_for
import json

import landuse_classification
from files_status import classified_files


app = Flask(__name__)


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

@app.route('/download', methods=['POST'])
def create_file():
    filename = landuse_classification.main()
    file_url = url_for('download_file', filename=filename)
    return jsonify(
        {
            "filename": filename,
            "URL": file_url
        }
    )
    
@app.route('/downloads/<filename>')
def download_file(filename):
    tiff_path = f'/app/landuse_classification/results/{filename}'
    return send_file(tiff_path, as_attachment=True, mimetype='image/tiff')

@app.route("/delete/<filename>", methods=["DELETE"])
def delete_file(filename):
    return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)