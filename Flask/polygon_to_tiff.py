import psycopg2
from datetime import datetime

def polygon_to_geotiff(polygon_coords):
    status = ''
    conn = psycopg2.connect(host="10.223.72.83" ,port="5433", database = "postgres" , user="postgres" , password="punpuntpasswd")
    try:
        polygon_wkt = "POLYGON((" + ",".join([f"{lon} {lat}" for lon, lat in polygon_coords]) + "))"

        query = f"""
        SELECT ST_AsTIFF(ST_UNION(
            ST_Clip(rast, ST_SetSRID(ST_MakeValid(ST_GeomFromText('{polygon_wkt}')), 4326))
        )) AS clipped_tiff
        FROM raster_results_1
        WHERE ST_Intersects(ST_SetSRID(ST_MakeValid(ST_GeomFromText('{polygon_wkt}')), 4326), rast);
        """
        
        cursor = conn.cursor()
    
        cursor.execute("SET postgis.gdal_enabled_drivers = 'ENABLE_ALL';")
        cursor.execute(query)

        result = cursor.fetchone()
        cropped_tiff = result[0] if result else None
    
        out_image = cropped_tiff

        if cropped_tiff:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output_{timestamp}.tiff"
            with open(f'/home/kea-trainee-punpun/Week2/polygon_tiff_output/{filename}', 'wb') as f:
                f.write(out_image.tobytes())
            status = f"File '{filename}' created."
        else:
            status = "No cropped raster data found."

        return {
            'status': status
        }

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()
