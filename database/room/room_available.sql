CREATE VIEW room_available AS
SELECT t1.name_type, (total_room - busy_room) as available
FROM
(SELECT name_type, count(*) AS busy_room
FROM reservation
WHERE check_in_date <= CURDATE() and check_out_date >= CURDATE()
GROUP BY name_type) t1
JOIN
(SELECT name_type, count(*) AS total_room
FROM room
GROUP BY name_type) t2 ON t1.name_type = t2.name_type