from flask import Flask
# from flask_swagger_ui import get_swaggerui_blueprint
import rasterio
import requests
from rasterio.mask import mask
from shapely.geometry import Polygon, mapping
import numpy as np

app = Flask(__name__)


tiff_file = '/home/kea-trainee-punpun/Week3/Flask/data/CPM_lstm_2023_2.tiff'

@app.route('/')
def hello():
  return { "message": "Hello!" }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8102, debug=True)