import psycopg2
from psycopg2 import OperationalError
from datetime import datetime
import uuid

class TiffFactory:
    def __init__(self):
        try:
            self.conn = psycopg2.connect( host="10.223.72.83" ,
                                    port="5433", 
                                    database = "postgres" , 
                                    user="postgres" , 
                                    password="punpuntpasswd"
            )
        except OperationalError as e:
            print(f"Error connecting to the database: {e}")
            self.conn = None
  
    def get_conn(self):
        return self.conn

    def polygon_to_geotiff(self, polygon_coords):
        status = ''
        cursor = self.conn.cursor()
        try:
            polygon_wkt = "POLYGON((" + ",".join([f"{lon} {lat}" for lon, lat in polygon_coords]) + "))"

            query = f"""
            SELECT ST_AsTIFF(ST_UNION(
                ST_Clip(rast, ST_SetSRID(ST_MakeValid(ST_GeomFromText('{polygon_wkt}')), 4326))
            )) AS clipped_tiff
            FROM raster_results_1
            WHERE ST_Intersects(ST_SetSRID(ST_GeomFromText('{polygon_wkt}'), 4326), rast);
            """
      
      
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
            #conn.close()


    def out_raster_area(self, polygon_coords):
      
        cursor = self.conn.cursor()
    
        try:

            polygon_wkt = "POLYGON((" + ",".join([f"{lon} {lat}" for lon, lat in polygon_coords]) + "))"

            query = f"""
            WITH intersected AS (
                SELECT ST_Intersection(rast::geometry, ST_Transform(ST_GeomFromText('{polygon_wkt}', 4326), 4326)) AS geom
                FROM raster_results_1
                WHERE ST_Intersects(rast::geometry, ST_Transform(ST_GeomFromText('{polygon_wkt}', 4326), 4326))
            ),
            difference_geom AS (
                SELECT ST_Transform(ST_Difference(ST_Transform(ST_GeomFromText('{polygon_wkt}', 4326), 4326), ST_Union(geom)), 32647) AS geom
                    FROM intersected
            )
            SELECT ST_Area(geom) AS area_not_overlapping_sqm
            FROM difference_geom;
            """
      
            cursor.execute("SET postgis.gdal_enabled_drivers = 'ENABLE_ALL';")
            cursor.execute(query)
            out_area = cursor.fetchone()
            out_area_output = round(out_area[0], 2)

            return out_area_output
        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            #conn.close()


    def polygon_to_area(self, polygon_coords):
        cursor = self.conn.cursor()
        try:
            polygon_wkt = "POLYGON((" + ",".join([f"{lon} {lat}" for lon, lat in polygon_coords]) + "))"

            query1 = f"""
            WITH pixel_size AS (
            SELECT
                ST_PixelWidth(rast) AS pixel_width,
                ST_PixelHeight(rast) AS pixel_height
            FROM raster_results_1
            LIMIT 1
            ),
            count_value AS (
                SELECT 
                    SUM(ST_ValueCount(rast,1,1)) AS value1, 
                    SUM(ST_ValueCount(rast,1,2)) As value2, 
                    SUM(ST_ValueCount(rast,1,0)) As value0
                FROM 
                    raster_results_1
                WHERE 
                    ST_Intersects(rast, ST_GeomFromText('{polygon_wkt}', 4326)
                ) 
            ),
            pixel_area AS (
            SELECT
                (pixel_width * pixel_height) AS area_per_pixel
            FROM pixel_size
            )
            SELECT
                100 * value0 AS area0,
                100 * value1 AS area1,
                100 * value2 AS area2
            FROM pixel_area, count_value;
            """

            # query2 = f"""
            # SELECT ST_Area(ST_Transform(ST_GeomFromText('{polygon_wkt}', 4326), 3857)) AS geom
            # """
    
            cursor.execute(query1, (polygon_wkt,))
            result = cursor.fetchone()

            # cursor.execute(query2, (polygon_wkt,))
            # poly_area = cursor.fetchone()
        
            if result:
                none_type = round(result[0], 2)
                rice_area = round(result[1], 2)
                sugarcane_area = round(result[2], 2)
                # area = round(poly_area[0], 2)
        
            return none_type, rice_area, sugarcane_area
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            cursor.close()
            # conn.close()

  # polygon_coords = [
  #     (101.5, 15.5),
  #     (102.0, 15.5),
  #     (102.0, 16.0),
  #     (101.5, 16.0),
  #     (101.5, 15.5)
  # ]

  # print(out_raster_area(polygon_coords))