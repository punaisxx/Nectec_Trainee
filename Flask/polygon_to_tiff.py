import psycopg2
from datetime import datetime
import uuid

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
        WHERE ST_Intersects(ST_SetSRID(ST_GeomFromText('{polygon_wkt}'), 4326), rast);
        """
        
        cursor = conn.cursor()
    
        cursor.execute("SET postgis.gdal_enabled_drivers = 'ENABLE_ALL';")
        cursor.execute(query)
        result = cursor.fetchone()
        cropped_tiff = result[0] if result else None
    
        out_image = cropped_tiff

        if cropped_tiff:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            uid = uuid.uuid4()
            filename = f"{timestamp}_{uid}.tiff"
            with open(f'/app/tiff_results/{filename}', 'wb') as f:
                f.write(out_image.tobytes())
            status = f"File '{filename}' created."
            return filename, status
        else:
            status = "No cropped raster data found."
            return None, status

    except Exception as e:
        print(f"Error: {e}")
        return None, status

    finally:
        cursor.close()
        conn.close()


def invalid_area(polygon_coords):
    status = ''
    conn = psycopg2.connect(host="10.223.72.83" ,port="5433", database = "postgres" , user="postgres" , password="punpuntpasswd")
    cursor = conn.cursor()
    try:
        polygon_wkt = "POLYGON((" + ",".join([f"{lon} {lat}" for lon, lat in polygon_coords]) + "))"

        query1 = f"""
        SELECT ST_Area(ST_GeomFromText('{polygon_wkt}')::geography) AS area;
        """

        query2 = f"""
        WITH wkt_polygon AS (
          SELECT ST_GeomFromText('{polygon_wkt}', 4326) AS geom
        ),
        clipped_polygons AS (
          SELECT
            ST_Intersection(wkt.geom, ST_Envelope(r.rast)) AS clipped_geom
          FROM
            wkt_polygon wkt,
            raster_results_1 r
          WHERE
            ST_Intersects(wkt.geom, r.rast)
        )
        SELECT
          SUM(ST_Area(ST_Transform(clipped_geom, 3857))) AS total_valid_area
        FROM
          clipped_polygons
        WHERE
          clipped_geom IS NOT NULL;
        """
    
        cursor.execute("SET postgis.gdal_enabled_drivers = 'ENABLE_ALL';")

        cursor.execute(query1)
        poly_area = cursor.fetchone()

        cursor.execute(query2)
        valid_poly_area = cursor.fetchone()

        invalid_area = abs(valid_poly_area[0])

        return invalid_area
    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()