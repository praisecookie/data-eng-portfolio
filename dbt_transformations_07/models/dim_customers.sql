-- In dbt, we configure the model to materialize as a physical table
{{ config(materialized='table') }}

WITH raw_data AS (
    -- We select from the raw data we loaded in Project 6
    SELECT * FROM `retail_dw.raw_customers`
),

cleaned_data AS (
    SELECT 
        customer_id,
        INITCAP(TRIM(name)) AS name,
        LOWER(TRIM(email)) AS email,
        COALESCE(phone, 'Unknown') AS phone,
        CURRENT_TIMESTAMP() AS processed_at
    FROM 
        raw_data
    WHERE 
        email IS NOT NULL
)

SELECT * FROM cleaned_data