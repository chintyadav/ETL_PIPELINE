from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from  airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import json

## Defing the DAG
with DAG(
    dag_id="nasa_apod_postgres",
    start_date=datetime(2024, 1, 1),
    schedule='@daily'
) as dag:
    
    ## step1: Creating a table if it doesn't exists
    @task
    def create_table():
        pg_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """
        pg_hook.run(create_table_query)

    ## step2: Fetching data from NASA APOD API
    extract_data = HttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',  ## Connection ID defined in Airflow Connections for NASA API
        endpoint='planetary/apod', ## API endpoint for Astronomy Picture of the Day
        method='GET',
        data={'api_key': "{{conn.nasa_api.extra_dejson.api_key}}"}, ## Pass the API key from Airflow Connections
        response_filter=lambda response: response.json(), ## Parse the JSON response
        do_xcom_push=True,
    )



    ## steps3: Transforming the data(pick the informaqtion that i need to save)
    @task
    def transform_data(response):
        apod_data = {
            'title': response['title'],
            'explanation': response['explanation'],
            'url': response['url'],
            'date': response['date'],
            'media_type': response['media_type']
        }
        return apod_data
    

    ## step4: Load the data into Postgres SQL
    @task
    def load_data_to_postgres(apod_data):
        pg_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """
        pg_hook.run(insert_query, parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))
        return "Data loaded successfully"
    ## step5: Verify the data DBViewer

    ## step 6: Define the dependencies
    create_table() >> extract_data 
    api_response = extract_data.output
    transformed_data = transform_data(api_response)
    load_data_to_postgres(transformed_data)