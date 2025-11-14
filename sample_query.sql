-- sample_query.sql
-- Run in sqlite3 or Cursor IDE: .open ecom.db then run this SQL

-- 1) Orders with customer info and items (joined) - flattened
SELECT
  o.order_id,
  o.order_date,
  o.status,
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer_name,
  COUNT(oi.order_item_id) AS items_count,
  SUM(oi.quantity * oi.unit_price) AS calc_total,
  o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id
ORDER BY o.order_date DESC
LIMIT 50;

-- 2) Top 10 products by revenue
SELECT p.product_id, p.name, p.category,
       SUM(oi.quantity * oi.unit_price) AS revenue,
       COUNT(DISTINCT oi.order_id) AS orders_count,
       AVG( r.rating ) AS avg_rating
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN reviews r ON p.product_id = r.product_id
GROUP BY p.product_id
ORDER BY revenue DESC
LIMIT 10;

-- 3) Customer lifetime value (LTV) top 10
SELECT c.customer_id, c.first_name || ' ' || c.last_name AS customer_name,
       COUNT(DISTINCT o.order_id) AS num_orders,
       SUM(o.total_amount) AS lifetime_value,
       MAX(o.order_date) AS last_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY lifetime_value DESC
LIMIT 10;