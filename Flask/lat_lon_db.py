import psycopg2
import numpy as np

def lat_lon_to_plant_type(longitude, latitude):
    plant_type = ''
    conn = psycopg2.connect(host="10.223.72.83" ,port="5433", database = "postgres" , user="postgres" , password="punpuntpasswd")

    try:
        cursor = conn.cursor()
        query = """SELECT ARRAY_AGG(ST_Value(rast, 1, p.geom)) AS pixel_values FROM raster_results_1, (SELECT ST_SetSRID(ST_MakePoint(%s, %s), 4326) AS geom) AS p WHERE ST_Intersects(rast, p.geom);"""
        
        cursor.execute(query, (longitude, latitude))
        result = cursor.fetchone()
        pixel_values = result[0] if result else []
    
        if np.round(pixel_values[0]) == 1:
            plant_type = 'rice'
        elif np.round(pixel_values[0]) == 2:
            plant_type = 'sugarcane'
        else:
            plant_type = 'none'

        return {
            'Plant type': plant_type
        }

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()