import psycopg2
from psycopg2 import OperationalError
from datetime import datetime
import os
class TaskMonitoring:
        def __init__(self):
                try:
                        # Edit connection
                        # self.conn = psycopg2.connect( host=os.getenv('HOST') ,
                        #             port=os.getenv('PORT'), 
                        #             database = os.getenv('DATABASE') , 
                        #             user=os.getenv('USER') , 
                        #             password=os.getenv('PASSWORD')
                        # )
                        self.conn = psycopg2.connect( host="localhost" ,
                                    port="5432", 
                                    database = "postgres" , 
                                    user="postgres"
                        )
                except OperationalError as e:
                        print(f"Error connecting to the database: {e}")
                        self.conn = None
        
        def get_conn(self):
                return self.conn

        def add_task(self, pid, filename, action):
                status = 'running'
                timestamp = datetime.now()
                cursor = self.conn.cursor()
                try:
                        query = """
                        INSERT INTO tasks (pid, filename, status, action, timestamp) VALUES (%s, %s, %s, %s, %s)
                        """
                        values = (pid, filename, status, action, timestamp)
                        cursor.execute(query, values)
                        print(f'Insert {pid} completed')
                except Exception as e:
                        print(f"Error: {e}")
                        return None

                finally:
                        self.conn.commit()
                        cursor.close()

        def finished_creation(self, filename, action):
                status = 'finished'
                timestamp = datetime.now()
                cursor = self.conn.cursor()
                try:
                        query = """
                        UPDATE tasks SET status = %s, action = %s, timestamp = %s WHERE filename = %s;
                        """
                        values = (status, action, timestamp, filename)
                        cursor.execute(query, values)
                        return 
                except Exception as e:
                        print(f"Error: {e}")
                        return None

                finally:
                        self.conn.commit()
                        cursor.close()

        def cancel_file_creation(self, pid):
                status = 'cancel'
                timestamp = datetime.now()
                action = ''
                cursor = self.conn.cursor()

                try:
                        query = """
                        UPDATE tasks SET status = %s, action = %s, timestamp = %s WHERE pid = %s;
                        """
                        values = (status, action, timestamp, pid)
                        cursor.execute(query, values)

                        query2 = """
                        SELECT filename FROM tasks WHERE pid = %s;
                        """
                        
                        cursor.execute(query2, (pid,))
                        result = cursor.fetchone()
                        file_delete = result[0]+'.tmp'
                        # Edit directory
                        # dir = './ai_results'
                        dir = "/Users/rawinnipha/Nectec_Trainee-Test1/Postgis_Raster_API/ai_results"
                        if os.path.exists(os.path.join(dir, file_delete)):
                                os.remove(os.path.join(dir, file_delete))
                                print(f"File {file_delete} has been deleted.")
                        else:
                                print("No filename found for the given PID.")
                        print('')
                except Exception as e:
                        print(f"Error: {e}")
                        return None

                finally:
                        self.conn.commit()
                        cursor.close()

        def display_tasks(self):

                cursor = self.conn.cursor()

                try:
                        query = """
                        SELECT * FROM tasks;
                        """
                        cursor.execute(query)
                        result = cursor.fetchall()
                        return result
                except Exception as e:
                        print(f"Error: {e}")
                        return None

                finally:
                        self.conn.commit()
                        cursor.close()

        def check_finished_status(self):
                cursor = self.conn.cursor()
                try:
                        query = """
                        SELECT filename FROM tasks WHERE status = 'running';
                        """                        
                        cursor.execute(query)
                        result = cursor.fetchall()
                        return result
                except Exception as e:
                        print(f"Error: {e}")
                        return None

                finally:
                        self.conn.commit()
                        cursor.close()

        