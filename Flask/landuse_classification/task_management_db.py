import psycopg2
from psycopg2 import OperationalError
from datetime import datetime
class TaskMonitoring:
        def __init__(self):
                try:
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

        def add_task(self):
                pid = 2
                filename = 'text2.txt'
                status = 'running'
                action = ''
                timestamp = datetime.now()
                cursor = self.conn.cursor()
                try:
                        query = """
                        INSERT INTO task (pid, filename, status, action, timestamp) VALUES (%s, %s, %s, %s, %s)
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
                pid = 1
                filename = ''
                status = 'finished'
                timestamp = datetime.now()
                cursor = self.conn.cursor()
                try:
                        query = """
                        UPDATE task SET status = %s, action = %s, timestamp = %s WHERE pid = %s;
                        """
                        values = (pid, filename, status, timestamp)
                        cursor.execute(query, values)
                        # result = cursor.fetchone()
                        return 'Add task to '
                except Exception as e:
                        print(f"Error: {e}")
                        return None, status

                finally:
                        self.conn.commit()
                        cursor.close()

        def cancel_file_creation(self, pid):
                # pid = 1
                filename = ''
                status = 'canceled'
                timestamp = datetime.now()
                action = ''
                cursor = self.conn.cursor()

                try:
                        query = """
                        UPDATE task SET status = %s, action = %s, timestamp = %s WHERE pid = %s;
                        """
                        values = (status, action, timestamp, pid)
                        cursor.execute(query, values)
                        # result = cursor.fetchone()
                        print('')
                except Exception as e:
                        print(f"Error: {e}")
                        return None, status

                finally:
                        self.conn.commit()
                        cursor.close()

        def display_tasks(self):
                status = 'canceled'
                cursor = self.conn.cursor()

                try:
                        query = """
                        SELECT * FROM task;
                        """
                        cursor.execute(query)
                        # result = cursor.fetchone()
                        result = cursor.fetchall()
                        # print(result)
                        # print(type(result))
                        # for task in result:
                        #         print(type(task))
                        formatted_data = [
                                {
                                        "pid": row[0],  # filename
                                        "filename": row[1],  # size
                                        "status": row[2],
                                        "action": row[3],
                                        "timestamp": row[4].strftime("%Y%m%d-%H%M%S")
                                }
                                for row in result
                        ]
                        print(formatted_data)
                        return 
                except Exception as e:
                        print(f"Error: {e}")
                        return None, status

                finally:
                        self.conn.commit()
                        cursor.close()

if __name__ == "__main__":
        task_monitor = TaskMonitoring()
        # task_monitor.add_task()
        # task_monitor.cancel_file_creation()
        task_monitor.display_tasks()
