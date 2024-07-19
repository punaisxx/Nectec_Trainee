import subprocess
from datetime import datetime
import os
import shutil

source_dir = '/data/raster_results'
target_dir = '/used_data'

tif_files = [f for f in os.listdir(source_dir) if f.endswith(('.tif', '.tiff'))]
file_count = len(tif_files)
print(f"Number of .tif files: {file_count}")

if file_count > 0:
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    for tif_file in tif_files:
        file_name = os.path.splitext(tif_file)[0]
        table_name = f"{file_name}_{timestamp}"

        # Run raster2pgsql command
        command = raster2pgsql_command = f"raster2pgsql -s 4326 -I -C {os.path.join(source_dir, tif_file)} -F -t 100x100 public.{table_name} | psql -d postgres -U postgres -h 10.223.72.83 -p 5433"

        # Execute the command using subprocess
        try:
                subprocess.run(command, shell=True, check=True)
                print('Raster data imported successfully.')
        except subprocess.CalledProcessError as e:
                print(f'Error: Raster data import failed: {e}')

        # Move the processed file to the target directory
        shutil.move(os.path.join(source_dir, tif_file), os.path.join(target_dir, tif_file))
        print(f"{tif_file} has been moved to {target_dir}")

        # Remove file in the target directory
        os.remove(os.path.join(target_dir, tif_file))
        print(f"{tif_file} has been deleted from {target_dir}")
else:
    print("No .tif files found to process.")