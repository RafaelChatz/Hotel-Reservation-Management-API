-- Return Hotel, Number of Reservations, Revenue
-- Only ACTIVE reservations.

SELECT
    h.name as hotel_name,
    COUNT(*) as number_of_reservations,
    SUM(r.total_price) as revenue
FROM hotels h
INNER JOIN reservations r
    ON r.hotel_id = h.id
WHERE r.status = 'ACTIVE'
GROUP BY h.id;