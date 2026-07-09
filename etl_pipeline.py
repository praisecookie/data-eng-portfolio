import pandas as pd
import duckdb
from datetime import datetime


def run_pipeline():
    print(f"[{datetime.now()}] Starting ETL Pipeline...")

    # ==========================================
    # 1. EXTRACT
    # ==========================================
    print("EXTRACT: Reading dirty data from CSV...")
    # Load the CSV into a Pandas DataFrame (think of it like an invisible Excel sheet)
    df = pd.read_csv("dirty_customers.csv")

    # ==========================================
    # 2. TRANSFORM
    # ==========================================
    print("TRANSFORM: Cleaning the data...")

    # Clean names: strip extra whitespace and make Title Case
    df['name'] = df['name'].str.strip().str.title()

    # Clean emails: make everything lowercase
    df['email'] = df['email'].str.lower()

    # Drop rows where 'email' is missing (NaN), because marketing can't email them!
    df = df.dropna(subset=['email'])

    # Fill missing phone numbers with a default value
    df['phone'] = df['phone'].fillna('Unknown')

    # Add metadata: Track when this record was processed
    df['processed_at'] = datetime.now()

    # ==========================================
    # 3. LOAD
    # ==========================================
    print("LOAD: Saving clean data to DuckDB database...")

    # Connect to a DuckDB database file (this will create 'retail.db' if it doesn't exist)
    conn = duckdb.connect('retail.db')

    # DuckDB is magical: it can read a Pandas DataFrame directly!
    # We use 'CREATE OR REPLACE' so we can run this script multiple times safely (Idempotency)
    conn.execute("CREATE OR REPLACE TABLE clean_customers AS SELECT * FROM df")

    # Close the connection
    conn.close()

    print("Pipeline Success! Clean data loaded into retail.db")


if __name__ == "__main__":
    run_pipeline()
