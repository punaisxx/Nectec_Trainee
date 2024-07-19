import os
import json
def check_process():
        dir = "./results"
        process_files = [f for f in os.listdir(dir) if f.endswith(('.txt.tmp'))]
        for filename in os.listdir(dir):
                if filename.endswith(('.txt.tmp')):
                        print(filename)
        process_count = len(process_files)
        print(process_count)
        finished_files = [f for f in os.listdir(dir) if f.endswith(('.txt'))]
        for filename in os.listdir(dir):
                if filename.endswith(('.txt')):
                        print(f"{filename}")
        finished_count = len(finished_files)
        print(finished_count)

# check_process()

def classified_files(dir):
        classified_files = {"processing": [], "finished": []}

        for filename in os.listdir(dir):
                if os.path.isfile(os.path.join(dir, filename)):
                        # count = 0
                        if filename.endswith(('.txt.tmp')):
                                file_details = {
                                        "name": filename,
                                        "time_used": "...",
                                }
                                classified_files["processing"].append(file_details)

                        if filename.endswith(('.txt')):
                                file_details = {
                                        "name": filename,
                                        "URL": "..."
                                }
                                classified_files["finished"].append(file_details)
        
        return classified_files

def create_json(classified_files):
        return json.dumps(classified_files, indent=4)

dir = "./results"
# print(type(classified_files(dir)))
classified_files = classified_files(dir)
print(type(create_json(classified_files)))