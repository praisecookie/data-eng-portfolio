-- 1. Create the Compute Engine (Virtual Warehouse)
-- We set it to Auto-Suspend after 60 seconds so it doesn't drain your free credits!
CREATE OR REPLACE WAREHOUSE portfolio_wh 
    WITH WAREHOUSE_SIZE = 'X-SMALL' 
    AUTO_SUSPEND = 60 
    AUTO_RESUME = TRUE 
    INITIALLY_SUSPENDED = TRUE;

-- 2. Create the Database & Schema
CREATE OR REPLACE DATABASE portfolio_db;
CREATE OR REPLACE SCHEMA portfolio_db.raw_data;

-- 3. Tell Snowflake to actively use the resources we just built
USE WAREHOUSE portfolio_wh;
USE DATABASE portfolio_db;
USE SCHEMA raw_data;

-- 4. Create the secure integration
CREATE OR REPLACE STORAGE INTEGRATION gcp_portfolio_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'GCS'
  ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('gcs://cookielou-data-lake-landing/');

-- 5. Ask Snowflake for the generated Service Account
DESCRIBE INTEGRATION gcp_portfolio_integration;

-- 6. Create the External Stage (This points Snowflake to the bucket using the integration)
CREATE OR REPLACE STAGE gcp_portfolio_stage
  URL = 'gcs://cookielou-data-lake-landing/'
  STORAGE_INTEGRATION = gcp_portfolio_integration;

-- 7. List the files!
LIST @gcp_portfolio_stage;

-- 8. Create a table to catch the data 
-- (We use generic VARCHAR columns here so it accepts your CSV regardless of what headers you used in Project 4)
CREATE OR REPLACE TABLE raw_csv_data (
    col1 VARCHAR,
    col2 VARCHAR,
    col3 VARCHAR,
    col4 VARCHAR,
    col5 VARCHAR,
    col6 VARCHAR,
    col7 VARCHAR
);

-- 9. The Data Engineer's favourite command: Pull the data from GCP to Snowflake
COPY INTO raw_csv_data
FROM @gcp_portfolio_stage
FILE_FORMAT = (
    TYPE = CSV 
    SKIP_HEADER = 1 
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE -- Tells Snowflake to ignore extra/missing columns
)
ON_ERROR = 'CONTINUE'; -- If a row is messy, just skip it and keep loading

-- 10. View your migrated data!
SELECT * FROM raw_csv_data;

-- 11. Create the Snowpipe (Updated with bulletproof formatting)
CREATE OR REPLACE PIPE gcp_auto_ingest_pipe
AUTO_INGEST = FALSE -- (If in real production, I will set this to TRUE and link it to a GCP Pub/Sub trigger)
AS
COPY INTO raw_csv_data
FROM @gcp_portfolio_stage
FILE_FORMAT = (
    TYPE = CSV 
    SKIP_HEADER = 1 
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
);

-- 12. Simulate a new file arriving and triggering the pipe
ALTER PIPE gcp_auto_ingest_pipe REFRESH;