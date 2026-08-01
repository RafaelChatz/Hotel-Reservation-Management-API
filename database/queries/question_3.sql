-- Return the five hotels with the highest revenue.

SELECT
    h.id,
    h.name,
    SUM(r.total_price) AS revenue
FROM hotels h
INNER JOIN reservations r
    ON r.hotel_id = h.id
GROUP BY h.id
ORDER BY revenue DESC
LIMIT 5;