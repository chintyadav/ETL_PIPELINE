from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta   

## Task 1
def preprocess_data():
    print("Preprocessing data...")

## Task 2
def train_model():
    print("Training model...")

## Task 3
def evaluate_model():
    print("Evaluating model...")

## Define the DAG
with DAG(
    'ML_Pipeline',
    start_date=datetime(2024, 1, 1),
    schedule='@daily'

) as dag:
    preprocess=PythonOperator(
        task_id='preprocess_task',
        python_callable=preprocess_data
    )
    train=PythonOperator(
        task_id='train_task',
        python_callable=train_model
    )
    evaluate=PythonOperator(
        task_id='evaluate_task',
        python_callable=evaluate_model
    )

    ## define dependencies
    preprocess >> train >> evaluate