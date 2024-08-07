import psycopg2
from psycopg2 import OperationalError
from datetime import datetime
import os
class TaskMonitoring:
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
                        # result = cursor.fetchone()
                        print(f'Insert {pid} completed')
                except Exception as e:
                        print(f"Error: {e}")
                        return None, status

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
                        # result = cursor.fetchone()
                        return 
                except Exception as e:
                        print(f"Error: {e}")
                        return None, status

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
                        dir = './results'
                        if os.path.exists(os.path.join(dir, file_delete)):
                                os.remove(os.path.join(dir, file_delete))
                                print(f"File {file_delete} has been deleted.")
                        else:
                                print("No filename found for the given PID.")
                        print('')
                except Exception as e:
                        print(f"Error: {e}")
                        return None, status

                finally:
                        self.conn.commit()
                        cursor.close()

        def display_tasks(self):
                status = ''
                cursor = self.conn.cursor()

                try:
                        query = """
                        SELECT * FROM tasks;
                        """
                        cursor.execute(query)
                        # result = cursor.fetchone()
                        result = cursor.fetchall()
                        return result
                except Exception as e:
                        print(f"Error: {e}")
                        return None, status

                finally:
                        self.conn.commit()
                        cursor.close()

        def check_finished_status(self):
                status = 'finished'
                timestamp = datetime.now()
                cursor = self.conn.cursor()
                dir = "./results"
                try:
                        query = """
                        SELECT filename FROM tasks WHERE status = 'running';
                        """
                        
                        cursor.execute(query)
                        result = cursor.fetchall()
                        return result
                except Exception as e:
                        print(f"Error: {e}")
                        return None, status

                finally:
                        self.conn.commit()
                        cursor.close()


# if __name__ == "__main__":
#         task_monitor = TaskMonitoring()
#         action = 'url'
#         task_monitor.check_finished_status(action)
#         # task_monitor.add_task()
#         # task_monitor.cancel_file_creation()
        # task_monitor.display_tasks()
#         task_monitor.find_file('33708')
#         pid = 33708
#         filename = task_monitor.find_file(pid)
#         if filename:
#                 print(f"Filename: {filename}")
#         else:
#                 print("No filename found for the given PID.")