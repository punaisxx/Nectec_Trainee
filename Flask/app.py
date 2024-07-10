from flask import Flask, request, jsonify, send_file, render_template, url_for

from lat_lon_db import lat_lon_to_plant_type
from polygon_to_area import polygon_to_area
from polygon_to_tiff import polygon_to_geotiff
from polygon_to_tiff import invalid_area

app = Flask(__name__)
UPLOAD_FOLDER = 'tiff_results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# polygon_coords = [
#     (101.30000000, 15.50764175),
#     (101.58234912, 15.49990556), 
#     (101.58062997, 15.30478166),
#     (101.26774407, 15.44661181), 
#     (101.30000000, 15.50764175)
# ]

# data = {
#     "polygon_coords": [
#         [102.26539189185458, 16.54356817627857],
#         [101.95606037474194, 16.08328194532515],
#         [101.93394678768034, 16.647561388673765],
#         [102.36400115858939, 16.538869127991614],
#         [102.26539189185458, 16.54356817627857]
#     ]
# }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/band', methods=['GET'])
def get_band():
    lon = float(request.args.get('lon'))
    lat = float(request.args.get('lat'))
    result = lat_lon_to_plant_type(lon, lat)
    return jsonify(result)

@app.route('/area', methods=['GET'])
def get_area():
    data = request.get_json()
    polygon_coords = data.get('polygon_coords')
    result = polygon_to_area(polygon_coords)
    return jsonify(result)

@app.route('/download/', methods=['POST'])
def get_tiffname():
    data = request.get_json()
    polygon_coords = data.get('polygon_coords')
    result = polygon_to_geotiff(polygon_coords)
    filename = result[0]
    status = result[1]
    if filename == None:
        return jsonify({"file_url": "Not Found", "status": status})
    else:
        file_url = url_for('get_tiff', filename=filename)
        invalid = invalid_area(polygon_coords)
        return jsonify(
            {
                "status": status,
                "result": {
                    "raster": file_url,
                    "stats": {
                        "area": {
                            "rice": "...",
                            "sugarcane": "...",
                            "other": "...",
                            "out_of_raster": "..."
                        },
                        "area_unit": "sq.m."
                    }
                },
                "input_polygon": "coord"
            }
        )

@app.route('/downloads/<filename>')
def get_tiff(filename):
    tiff_path = f'/app/tiff_results/{filename}'
    return send_file(tiff_path, as_attachment=True, mimetype='image/tiff')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


