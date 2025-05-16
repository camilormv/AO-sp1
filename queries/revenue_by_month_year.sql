-- TODO: This query will return a table with the revenue by month and year. It
-- will have different columns: month_no, with the month numbers going from 01
-- to 12; month, with the 3 first letters of each month (e.g. Jan, Feb);
-- Year2016, with the revenue per month of 2016 (0.00 if it doesn't exist);
-- Year2017, with the revenue per month of 2017 (0.00 if it doesn't exist) and
-- Year2018, with the revenue per month of 2018 (0.00 if it doesn't exist).

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
    COALESCE(SUM(CASE WHEN year = '2016' THEN revenue END), 0.00) AS Year2016,
    COALESCE(SUM(CASE WHEN year = '2017' THEN revenue END), 0.00) AS Year2017,
    COALESCE(SUM(CASE WHEN year = '2018' THEN revenue END), 0.00) AS Year2018
FROM (
    SELECT
        strftime('%m', o.order_purchase_timestamp) AS month_no,
        strftime('%Y', o.order_purchase_timestamp) AS year,
        p.payment_value AS revenue
    FROM
        olist_orders_dataset o
        JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
    WHERE
        o.order_purchase_timestamp IS NOT NULL
        AND p.payment_value IS NOT NULL
) t
GROUP BY
    month_no
ORDER BY
    month_no;