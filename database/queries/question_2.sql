-- Find customers that never booked.

-- Preferred solution using NOT EXISTS.

SELECT
    c.id,
    c.first_name,
    c.last_name,
    c.email
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM reservations r
    WHERE r.customer_id = c.id
);

-- Alternative solutions are shown below for reference.

--SELECT
--    c.id,
--    c.first_name,
--    c.last_name,
--    c.email
--FROM customers c
--LEFT JOIN reservations r
--    ON r.customer_id = c.id
--WHERE r.id IS NULL;
--
--
--SELECT
--    c.id,
--    c.first_name,
--    c.last_name,
--    c.email
--FROM customers c
--WHERE c.id NOT IN (
--    SELECT r.customer_id
--    FROM reservations r
--);