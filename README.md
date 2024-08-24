---

# API Environment Setup Guide

## Prerequisites

Before using the API environment, ensure you have the following prepared:

- **Architecture**: `amd64` (or `x86-64`) to support pulling PostGIS images.
- **Text Editor or IDE**: `VS Code` or other code editing tools.
- **Package Manager**: `pip` (Python 3.8 or higher).
- **Database**: `PostgreSQL` with the `PostGIS` extension.

## Clone Repository

Clone the source code from the GitHub repository [Nectec_Trainee](https://github.com/punaisxx/Nectec_Trainee.git) to your local machine or server:

```bash
git clone https://github.com/punaisxx/Nectec_Trainee.git
cd Nectec_Trainee
```

## Create Docker Containers

Docker containers encapsulate the application and isolate it in a separate environment, ensuring consistency across different processing environments. This enables rapid deployment, scalability, and efficient resource usage.

### Creating Flask Container

1. **Start Docker Container with Interactive Bash Shell**  
   Begin by using the `docker run` command to start a Docker container. Name the container, map the host port to the container port, set the working directory to `/app`, map the host directory to the container directory, and use the official Python runtime as the parent image.

   Example Bash file:
   ```bash
   docker run -it \
   --name your_container_name \
   -p 8100:5000 \
   -v /your/app/path/:/app \
   python:3.10.12-slim python
   ```

2. **Run Bash Shell**

3. **Install Packages**  
   Install the packages listed in `requirements.txt`.

### Creating PostGIS Container

1. **Start Docker Container with Interactive Bash Shell**  
   Start the Docker container using the `docker run` command. Name the container, set the password, and define the container path `/var/lib/postgresql/data` for database storage. Set the authentication method to `md5` for password verification when connecting to PostgreSQL. Map the host directory to the container directory for both `/var/lib/postgresql/data` and `/raster_data`. Use the official PostGIS runtime as the parent image.

2. **Run Bash Shell**

## Database Setup

1. **Connect to PostgreSQL Server**  
   Command:
   ```bash
   psql -U postgres -d postgres
   ```

2. **Enable PostGIS Extension**  
   Command:
   ```sql
   CREATE EXTENSION postgis_raster;
   ```

3. **Create Table for Raster Data**  
   Command:
   ```sql
   CREATE TABLE raster_results_1;
   ```

4. **Load Rasters into PostGIS Raster Table**  
   Command:
   ```bash
   raster2pgsql -s 4326 -I -C -M *.tif -F -t 100x100 public.raster_results_1 | psql -d gisdb
   ```

5. **Create Table for Tasks Monitoring and Management**  
   Command:
   ```sql
   CREATE TABLE tasks (
       id SERIAL PRIMARY KEY,
       pid INT,
       filename VARCHAR(255),
       status VARCHAR(255),
       action VARCHAR(255),
       timestamp TIMESTAMP
   );
   ```

## Add Database Connection Information

1. **Create `.env` File**  
   Create a `.env` file in the `/app` directory.

2. **Add Database Connection Information**  
   Add the following details to the `.env` file:
   ```bash
   HOST=your_host
   PORT=your_port
   DATABASE=your_database
   USER=your_user
   PASSWORD=your_password
   ```

## Start API Server

Run the API server using the following command:

```bash
python app.py
```

## Test with Postman

Test the API endpoints using Postman or any other API testing tool.

---
