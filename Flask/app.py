from flask import Flask, request, jsonify
# import rasterio
# from rasterio.mask import mask
# from shapely.geometry import Polygon, mapping
# import numpy as np

from lat_lon import lat_lon_to_band

app = Flask(__name__)


tiff_file = '/home/kea-trainee-punpun/Week3/Flask/data/CPM_lstm_2023_2.tiff'

@app.route('/')
def hello():
  return { "message": "Hello!" }

@app.route('/api/crop', methods=['GET'])
def get_crop():
    file_path = '/data/raster_results/CPM_lstm_2023_new.tiff'
    lon = float(request.args.get('lon'))
    lat = float(request.args.get('lat'))
    result = lat_lon_to_band(file_path, lon, lat)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)