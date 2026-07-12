CREATE OR REPLACE TABLE `retail_dw.clean_customers` AS
SELECT 
  customer_id,
  INITCAP(TRIM(name)) AS name,
  LOWER(TRIM(email)) AS email,
  COALESCE(phone, 'Unknown') AS phone,
  CURRENT_TIMESTAMP() AS processed_at
FROM 
  `retail_dw.raw_customers`
WHERE 
  email IS NOT NULL;