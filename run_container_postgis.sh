docker run -itd \
--name punpun_postgis_db \
-p 5433:5432 \
-e POSTGRES_PASSWORD=punpuntpasswd \
-e PGDATA=/var/lib/postgresql/data \
-e POSTGRES_HOST_AUTH_METHOD=md5 \
-v /home/kea-trainee-punpun/Week3/Data_postgres:/var/lib/postgresql/data \
postgis/postgis:14-master 