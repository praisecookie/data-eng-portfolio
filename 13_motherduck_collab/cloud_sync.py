import duckdb
import pandas as pd
import os

print("🦆 Connecting to MotherDuck Cloud...")

# 1. Connect to MotherDuck (It automatically finds the MOTHERDUCK_TOKEN in my terminal environment)
# The 'md:' tells DuckDB to connect to the MotherDuck cloud instead of a local file.
con = duckdb.connect('md:')

# 2. Create a fresh Cloud Database for this project
con.sql("CREATE DATABASE IF NOT EXISTS remote_portfolio_db")
con.sql("USE remote_portfolio_db")

print("✅ Connected! Generating local data...")

# 3. Create a local Pandas DataFrame representing some daily engineering metrics
data = {
    'engineer_name': ['Praise', 'Alice', 'Bob'],
    'pipelines_built': [13, 4, 7],
    'coffee_cups_consumed': [42, 15, 20]
}
local_df = pd.DataFrame(data)

print("☁️ Pushing local data to the cloud...")

# 4. Magically write the local DataFrame directly into a MotherDuck Cloud Table!
con.sql("CREATE TABLE IF NOT EXISTS engineering_stats AS SELECT * FROM local_df")

# 5. Query the cloud database to prove it worked
print("\n📊 Data successfully stored in MotherDuck! Here is the cloud data:")
result = con.sql(
    "SELECT * FROM engineering_stats ORDER BY pipelines_built DESC").df()
print(result)
