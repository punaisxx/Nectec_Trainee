import psycopg2
from psycopg2 import sql

def polygon_to_area(polygon_coords):
    conn = psycopg2.connect(host="10.223.72.83" ,port="5433", database = "postgres" , user="postgres" , password="punpuntpasswd")
    try:
        polygon_wkt = "POLYGON((" + ",".join([f"{lon} {lat}" for lon, lat in polygon_coords]) + "))"
        query = f"""
        WITH polygon_geom AS (
            SELECT ST_SetSRID(ST_GeomFromText('{polygon_wkt}'), 4326) AS geom
        )
        SELECT
            SUM(CASE WHEN value = 1 THEN count END) AS count_value1,
            SUM(CASE WHEN value = 2 THEN count END) AS count_value2
        FROM (
            SELECT
                value,
                count
            FROM (
                SELECT
                    (ST_ValueCount(ST_Clip(rast, geom))).*
                FROM
                    raster_results_1,
                    polygon_geom
                WHERE
                    ST_Intersects(rast, geom)
            ) AS counts
        ) AS summary;

        """
        cursor = conn.cursor()
    
        cursor.execute(query, (polygon_wkt,))
    
        result = cursor.fetchone()

        if result:
            rice_area = result[0]*100
            sugarcane_area = result[1]*100
        
        return {
            'rice area': rice_area,
            'sugarcane area': sugarcane_area
        }
        
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