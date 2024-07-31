docker run -it \
--name punpun_flask2 \
-p 8103:5000 \
-v /home/kea-trainee-punpun/git/Nectec_Trainee/Landuse_API/:/app \
-v /trainee_data/punpun_data:/app/data \
-v /home/kea-trainee-punpun/DATA/landuse_results:/data/landuse_results \
python:3.10.12-slim python