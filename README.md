Overview
========

This is an ETL Pipeline project built with Apache Airflow and Astronomer. It contains multiple data pipelines including NASA APOD data extraction and an ML pipeline for model training and evaluation.

Project Contents
================

Your Astro project contains the following files and folders:

- **dags**: This folder contains the Python files for your Airflow DAGs:
    - `etl.py`: NASA APOD ETL Pipeline - Fetches Astronomy Picture of the Day data from NASA API, transforms it, and loads it into PostgreSQL database
    - `mlpipeline.py`: ML Pipeline - Includes data preprocessing, model training, and model evaluation tasks
    - `exampledag.py`: Example DAG for reference
- **Dockerfile**: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- **include**: This folder contains any additional files that you want to include as part of your project.
- **packages.txt**: Install OS-level packages needed for your project by adding them to this file.
- **requirements.txt**: Install Python packages needed for your project (includes apache-airflow-providers-http and apache-airflow-providers-postgres).
- **plugins**: Add custom or community plugins for your project to this file.
- **airflow_settings.yaml**: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.
- **tests**: Contains DAG testing files to ensure pipeline integrity.

Prerequisites
==============

Before running this project, ensure you have:

- Docker and Docker Compose installed
- Astronomer CLI installed (`pip install astronomer`)
- Python 3.9+
- NASA API key (for the ETL pipeline - get it from https://api.nasa.gov/)
- PostgreSQL connection configured in Airflow (connection ID: `my_postgres_connection`)

Setup Instructions
==================

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chintyadav/ETL_PIPELINE.git
   cd Airflow-astro
   ```

2. **Configure Airflow Connections**:
   Edit `airflow_settings.yaml` to add your connections:
   - PostgreSQL Connection (ID: `my_postgres_connection`)
   - NASA API Connection (ID: `nasa_api`) with your API key

3. **Install dependencies**:
   Dependencies are automatically installed from `requirements.txt` during Docker build.

Deploy Your Project Locally
===========================

Start Airflow on your local machine by running 'astro dev start'.

This command will spin up five Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- DAG Processor: The Airflow component responsible for parsing DAGs
- API Server: The Airflow component responsible for serving the Airflow UI and API
- Triggerer: The Airflow component responsible for triggering deferred tasks

When all five containers are ready the command will open the browser to the Airflow UI at http://localhost:8080/. You should also be able to access your Postgres Database at 'localhost:5432/postgres' with username 'postgres' and password 'postgres'.

Note: If you already have either of the above ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

Pipeline Details
================

### NASA APOD ETL Pipeline (etl.py)
- **Purpose**: Automates the extraction of Astronomy Picture of the Day data from NASA API
- **Schedule**: Daily execution
- **Tasks**:
  1. Create table in PostgreSQL (if not exists)
  2. Extract APOD data from NASA API
  3. Transform data (extract relevant fields)
  4. Load data into PostgreSQL database
- **Data Stored**: Title, explanation, URL, date, and media type

### ML Pipeline (mlpipeline.py)
- **Purpose**: Demonstrates a machine learning workflow with data preprocessing, training, and evaluation
- **Schedule**: Daily execution
- **Tasks**:
  1. Preprocess data
  2. Train model
  3. Evaluate model

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://www.astronomer.io/docs/astro/deploy-code/

Support & Contact
=================

For questions or issues related to this project, please refer to:
- Astronomer Support: https://www.astronomer.io/docs/
- Apache Airflow Documentation: https://airflow.apache.org/docs/
- This Repository: https://github.com/chintyadav/ETL_PIPELINE
