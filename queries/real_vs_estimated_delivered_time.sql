-- TODO: This query will return a table with the differences between the real 
-- and estimated delivery times by month and year. It will have different 
-- columns: month_no, with the month numbers going from 01 to 12; month, with 
-- the 3 first letters of each month (e.g. Jan, Feb); Year2016_real_time, with 
-- the average delivery time per month of 2016 (NaN if it doesn't exist); 
-- Year2017_real_time, with the average delivery time per month of 2017 (NaN if 
-- it doesn't exist); Year2018_real_time, with the average delivery time per 
-- month of 2018 (NaN if it doesn't exist); Year2016_estimated_time, with the 
-- average estimated delivery time per month of 2016 (NaN if it doesn't exist); 
-- Year2017_estimated_time, with the average estimated delivery time per month 
-- of 2017 (NaN if it doesn't exist) and Year2018_estimated_time, with the 
-- average estimated delivery time per month of 2018 (NaN if it doesn't exist).
-- HINTS
-- 1. You can use the julianday function to convert a date to a number.
-- 2. order_status == 'delivered' AND order_delivered_customer_date IS NOT NULL
-- 3. Take distinct order_id.

WITH delivered_orders AS (
    SELECT DISTINCT
        order_id,
        order_purchase_timestamp,
        order_delivered_customer_date,
        order_estimated_delivery_date
    FROM
        olist_orders
    WHERE
        order_status = 'delivered'
        AND order_delivered_customer_date IS NOT NULL
        AND order_estimated_delivery_date IS NOT NULL
        AND order_purchase_timestamp IS NOT NULL
),
times AS (
    SELECT
        strftime('%m', order_purchase_timestamp) AS month_no,
        strftime('%Y', order_purchase_timestamp) AS year,
        -- Real delivery time: days from purchase to real delivery
        julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp) AS real_time,
        -- Estimated delivery time: days from purchase to estimate
        julianday(order_estimated_delivery_date) - julianday(order_purchase_timestamp) AS estimated_time
    FROM delivered_orders
),
monthly_averages AS (
    SELECT
        month_no,
        CASE
            WHEN month_no = '01' THEN 'Jan'
            WHEN month_no = '02' THEN 'Feb'
            WHEN month_no = '03' THEN 'Mar'
            WHEN month_no = '04' THEN 'Apr'
            WHEN month_no = '05' THEN 'May'
            WHEN month_no = '06' THEN 'Jun'
            WHEN month_no = '07' THEN 'Jul'
            WHEN month_no = '08' THEN 'Aug'
            WHEN month_no = '09' THEN 'Sep'
            WHEN month_no = '10' THEN 'Oct'
            WHEN month_no = '11' THEN 'Nov'
            WHEN month_no = '12' THEN 'Dec'
        END AS month,
        AVG(CASE WHEN year = '2016' THEN real_time END) AS Year2016_real_time,
        AVG(CASE WHEN year = '2017' THEN real_time END) AS Year2017_real_time,
        AVG(CASE WHEN year = '2018' THEN real_time END) AS Year2018_real_time,
        AVG(CASE WHEN year = '2016' THEN estimated_time END) AS Year2016_estimated_time,
        AVG(CASE WHEN year = '2017' THEN estimated_time END) AS Year2017_estimated_time,
        AVG(CASE WHEN year = '2018' THEN estimated_time END) AS Year2018_estimated_time
    FROM
        times
    GROUP BY
        month_no
)
SELECT
    month_no,
    month,
    Year2016_real_time,
    Year2017_real_time,
    Year2018_real_time,
    Year2016_estimated_time,
    Year2017_estimated_time,
    Year2018_estimated_time
FROM
    monthly_averages
ORDER BY
    month_no;