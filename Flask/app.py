from flask import Flask, request, jsonify, send_file, render_template, url_for
import json, os, signal

from lat_lon_db import lat_lon_to_plant_type
# from polygon_to_area import polygon_to_area
#from polygon_to_tiff import polygon_to_geotiff
#from polygon_to_tiff import out_raster_area
from polygon_to_tiff import TiffFactory

app = Flask(__name__)
UPLOAD_FOLDER = 'tiff_results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

tiff_factory = TiffFactory()

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
    return jsonify({"Hello": "World!"})

@app.route('/band', methods=['GET'])
def get_band():
    lon = float(request.args.get('lon'))
    lat = float(request.args.get('lat'))
    result = lat_lon_to_plant_type(lon, lat)
    return jsonify(result)

# @app.route('/area', methods=['GET'])
# def get_area():
#     data = request.get_json()
#     polygon_coords = data.get('polygon_coords')
#     results = polygon_to_area(polygon_coords)
#     return jsonify(results)

@app.route('/download/', methods=['POST'])
def tiff_output():
    data = request.get_json()
    polygon_coords = data.get('polygon_coords')
    result = tiff_factory.polygon_to_geotiff(polygon_coords)
    filename = result[0]
    status = result[1]
    if filename == None:
        return jsonify({"file_url": "Not Found", "status": status})
    else:
        file_url = url_for('get_tiff', filename=filename)
        plant_area = tiff_factory.polygon_to_area(polygon_coords)
        out_of_raster = tiff_factory.out_raster_area(polygon_coords)
        return jsonify(
            {
                "status": status,
                "results": {
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

@app.route('/downloads/<filename>')
def get_tiff(filename):
    tiff_path = f'/app/tiff_results/{filename}'
    return send_file(tiff_path, as_attachment=True, mimetype='image/tiff')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)