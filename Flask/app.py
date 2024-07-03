from flask import Flask, request, jsonify

from lat_lon_db import lat_lon_to_plant_type
from polygon_to_area import polygon_to_area
from polygon_to_tiff import polygon_to_geotiff

app = Flask(__name__)

@app.route('/')
def hello():
    return { "message": "Hello!" }

@app.route('/api/band', methods=['GET'])
def get_band():
    lon = float(request.args.get('lon'))
    lat = float(request.args.get('lat'))
    result = lat_lon_to_plant_type(lon, lat)
    return jsonify(result)

@app.route('/api/area', methods=['GET'])
def get_area():
    data = request.get_json()
    polygon_coords = data.get('polygon_coords')
    result = polygon_to_area(polygon_coords)
    return jsonify(result)

# @app.route('/api/tiff', methods=['GET'])
# def get_tiff():
#     data = request.get_json()
#     polygon_coords = data.get('polygon_coords')
#     result = polygon_to_geotiff(polygon_coords)
#     return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)