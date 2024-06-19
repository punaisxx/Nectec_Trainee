docker run -it \
--name punpun_python \
-p 8102:5000 \
-v /home/kea-trainee-punpun/Week3/Flask/:/app \
-v /trainee_data/punpun_data:/app/data \
python:3.10.12-slim bash