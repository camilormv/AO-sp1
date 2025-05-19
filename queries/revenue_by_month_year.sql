-- TODO: This query will return a table with the revenue by month and year. It
-- will have different columns: month_no, with the month numbers going from 01
-- to 12; month, with the 3 first letters of each month (e.g. Jan, Feb);
-- Year2016, with the revenue per month of 2016 (0.00 if it doesn't exist);
-- Year2017, with the revenue per month of 2017 (0.00 if it doesn't exist) and
-- Year2018, with the revenue per month of 2018 (0.00 if it doesn't exist).


SELECT 
    A.month_no,
    CASE A.month_no
        WHEN '01' THEN 'Jan' WHEN '02' THEN 'Feb' WHEN '03' THEN 'Mar'
        WHEN '04' THEN 'Apr' WHEN '05' THEN 'May' WHEN '06' THEN 'Jun'
        WHEN '07' THEN 'Jul' WHEN '08' THEN 'Aug' WHEN '09' THEN 'Sep'
        WHEN '10' THEN 'Oct' WHEN '11' THEN 'Nov' WHEN '12' THEN 'Dec'
    END AS month,
    SUM(CASE WHEN year = '2016' THEN payment_value ELSE 0 END) AS Year2016,
    SUM(CASE WHEN year = '2017' THEN payment_value ELSE 0 END) AS Year2017,
    SUM(CASE WHEN year = '2018' THEN payment_value ELSE 0 END) AS Year2018
FROM 
    (
        SELECT
            order_id,
            STRFTIME('%m', order_delivered_customer_date) AS month_no,
            STRFTIME('%Y', order_delivered_customer_date) AS year
        FROM olist_orders 
        WHERE order_delivered_customer_date IS NOT NULL AND order_status = 'delivered'
        ) A
    JOIN 
        (
            SELECT 
                order_id,
                MIN(payment_value) AS payment_value
            FROM olist_order_payments 
            GROUP BY order_id
        ) B
    ON B.order_id = A.order_id
GROUP BY month_no
ORDER BY month_no;