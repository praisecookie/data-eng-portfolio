import functions_framework
from google.cloud import bigquery, storage
import pandas as pd
import io
import sys


@functions_framework.cloud_event
def process_gcs_to_bigquery(cloud_event):
    try:
        data = cloud_event.data
        bucket_name = data["bucket"]
        file_name = data["name"]

        print(f"⚡ WAKE UP! Event Received for file: {file_name}")
        sys.stdout.flush()  # Force the log to appear immediately!

        # Skip if it's not a CSV
        if not file_name.endswith('.csv'):
            print("Not a CSV file. Skipping execution.")
            sys.stdout.flush()
            return

        # 1. Read file directly from Google Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.get_blob(file_name)
        content = blob.download_as_bytes()

        df = pd.read_csv(io.BytesIO(content))
        print(f"📊 Successfully parsed {len(df)} rows. Sending to BigQuery...")
        sys.stdout.flush()

        # 2. Append data to BigQuery
        bq_client = bigquery.Client()
        table_id = "data-eng-portfolio-501916.retail_dw.serverless_events"

        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        load_job = bq_client.load_table_from_dataframe(
            df, table_id, job_config=job_config)
        load_job.result()  # Wait for job completion

        print(f"✅ SUCCESS! Loaded {len(df)} rows into BigQuery.")
        sys.stdout.flush()

    except Exception as e:
        # If ANYTHING goes wrong, catch it and scream it into the logs!
        print(f"❌ FATAL ERROR: {str(e)}")
        sys.stdout.flush()
        raise e
