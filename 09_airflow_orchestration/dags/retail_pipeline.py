from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

# Default settings applied to all tasks
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'retail_end_to_end_pipeline',
    default_args=default_args,
    description='Orchestrates the GCS upload and dbt transformations',
    schedule_interval='@daily',  # Runs once a day at midnight
    catchup=False,
) as dag:

    # Task 1: A simple starting point
    start_pipeline = EmptyOperator(task_id='start_pipeline')

    # Task 2: Simulate the Bash script uploading to the GCS Data Lake
    extract_and_load = BashOperator(
        task_id='extract_and_load_gcs',
        bash_command='echo "Triggering Bash Script: Extracting API data and loading to Google Cloud Storage..." && sleep 2'
    )

    # Task 3: Simulate dbt transforming the data in BigQuery
    transform_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='echo "Triggering dbt: Running transformations in BigQuery..." && sleep 2'
    )

    # Task 4: An endpoint to signify completion
    end_pipeline = EmptyOperator(task_id='end_pipeline')

    # Define the dependencies using bitshift operators (>>).
    # This dictates the exact order the tasks must run.
    start_pipeline >> extract_and_load >> transform_dbt >> end_pipeline
