docker run -it \
--name punpun_flask \
-p 8102:5000 \
-v /home/kea-trainee-punpun/git/Nectec_Trainee/Flask/:/app \
-v /trainee_data/punpun_data:/app/data \
-v /home/kea-trainee-punpun/DATA/raster_results:/data/raster_results \
python:3.10.12-slim python