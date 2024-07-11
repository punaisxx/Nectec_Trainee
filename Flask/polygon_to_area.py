import psycopg2
from psycopg2 import sql

def polygon_to_area(polygon_coords):
    conn = psycopg2.connect(host="10.223.72.83" ,port="5433", database = "postgres" , user="postgres" , password="punpuntpasswd")
    try:
        polygon_wkt = "POLYGON((" + ",".join([f"{lon} {lat}" for lon, lat in polygon_coords]) + "))"
        # query = f"""
        # WITH polygon_geom AS (
        #     SELECT ST_SetSRID(ST_GeomFromText('{polygon_wkt}'), 4326) AS geom
        # )
        # SELECT
        #     SUM(CASE WHEN value = 1 THEN count END) AS count_value1,
        #     SUM(CASE WHEN value = 2 THEN count END) AS count_value2
        # FROM (
        #     SELECT
        #         value,
        #         count
        #     FROM (
        #         SELECT
        #             (ST_ValueCount(ST_Clip(rast, geom))).*
        #         FROM
        #             raster_results_1,
        #             polygon_geom
        #         WHERE
        #             ST_Intersects(rast, geom)
        #     ) AS counts
        # ) AS summary;

        # """

        query1 = f"""
        WITH pixel_size AS (
        SELECT
            ST_PixelWidth(rast) AS pixel_width,
            ST_PixelHeight(rast) AS pixel_height
        FROM raster_results_1
        LIMIT 1
        ),
        count_value AS (
            SELECT SUM(ST_ValueCount(rast,1,1)) AS value1, SUM(ST_ValueCount(rast,1,2)) As value2, SUM(ST_ValueCount(rast,1,0)) As value0
            FROM raster_results_1
            WHERE ST_Intersects(rast,
                    ST_GeomFromText('{polygon_wkt}', 4326)
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

        query2 = f"""
        SELECT ST_Area(ST_Transform(ST_GeomFromText('{polygon_wkt}', 4326), 3857)) AS geom
        """

        cursor = conn.cursor()
    
        cursor.execute(query1, (polygon_wkt,))
        result = cursor.fetchone()

        cursor.execute(query2, (polygon_wkt,))
        poly_area = cursor.fetchone()
        


        if result:
            none_type = f"{result[0]:.2f} m²"
            rice_area = f"{result[1]:.2f} m²"
            sugarcane_area = f"{result[2]:.2f} m²"
            area = f"{poly_area[0]:.2f} m²"
        
        return none_type, rice_area, sugarcane_area, area
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        cursor.close()
        conn.close()

# polygon_coords = [
#     (101.5, 15.5),
#     (102.0, 15.5),
#     (102.0, 16.0),
#     (101.5, 16.0),
#     (101.5, 15.5)
# ]

# print(polygon_to_area(polygon_coords))