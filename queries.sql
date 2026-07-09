SELECT *
FROM read_csv_auto('sales.csv') LIMIT 5;

SELECT Region, SUM(Sales) AS Total_Revenue
FROM read_csv_auto('sales.csv')
GROUP BY Region
ORDER BY Total_Revenue DESC;