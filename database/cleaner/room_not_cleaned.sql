CREATE VIEW view_room_not_cleaned AS
SELECT l.room_number
FROM
(SELECT room_number, max(end_date) -- CAMERE LIBERE
FROM reservation
WHERE NOW() >= end_date and (end_date is not null)
GROUP BY room_number) l
LEFT JOIN
(SELECT room_number, max(cleaning_date) -- CAMERE GIA' PULITE
FROM cleaning
GROUP BY room_number) p ON p.room_number = l.room_number
WHERE p.room_number is null
