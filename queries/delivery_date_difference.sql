-- TODO: This query will return a table with two columns; State, and 
-- Delivery_Difference. The first one will have the letters that identify the 
-- states, and the second one the average difference between the estimate 
-- delivery date and the date when the items were actually delivered to the 
-- customer.
-- HINTS:
-- 1. You can use the julianday function to convert a date to a number.
-- 2. You can use the CAST function to convert a number to an integer.
-- 3. You can use the STRFTIME function to convert a order_delivered_customer_date to a string removing hours, minutes and seconds.
-- 4. order_status == 'delivered' AND order_delivered_customer_date IS NOT NULL


WITH diffs AS (
  SELECT
    c.customer_state AS State,
    -- 1. Resta correcta (entregado - estimado) y formatea fechas
    julianday(STRFTIME('%Y-%m-%d', o.order_delivered_customer_date))
    - julianday(STRFTIME('%Y-%m-%d', o.order_estimated_delivery_date)) AS diff
  FROM olist_orders o
  JOIN olist_customers c
    ON o.customer_id = c.customer_id
  WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL
)
SELECT
  State,
  -- 2. Aplica CEIL correctamente al promedio
  CAST(
    CASE
      WHEN (AVG(diff) - CAST(AVG(diff) AS INTEGER)) > 0 
        THEN CAST(AVG(diff) AS INTEGER) + 1
      ELSE CAST(AVG(diff) AS INTEGER)*-1
    END
  AS INTEGER) AS Delivery_Difference
FROM diffs
GROUP BY State
ORDER BY Delivery_Difference ASC;