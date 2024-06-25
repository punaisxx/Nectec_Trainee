import rasterio
from pyproj import Transformer

def lat_lon_to_band(file_path, lon, lat):
    with rasterio.open(file_path) as src:
        # Transformer to convert coordinates
        transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
        x, y = transformer.transform(lon, lat)

        # Convert coordinates to pixel indices
        row, col = src.index(x, y)

        # Read the band data
        band_data = src.read(1)

        # Check if indices are within the raster bounds
        if 0 <= row < band_data.shape[0] and 0 <= col < band_data.shape[1]:
            value_at_location = band_data[row, col]

            # Thresholds
            threshold_rice = 1
            threshold_sugarcane = 2

            # Determine crop type based on value
            if value_at_location < threshold_rice:
                result = "rice"
            elif value_at_location < threshold_sugarcane:
                result = "sugarcane"
            else:
                result = "none"
        else:
            result = "out of bounds"

    return {
        'latitude': lat,
        'longitude': lon,
        'result': result
}