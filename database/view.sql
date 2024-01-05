DELIMITER //

CREATE VIEW view_promotion as
SELECT p.id_promotion, p.promotion_name, p.p_start_date, p.p_end_date, p.percent_discount, r.name_type
FROM
(promotion p
JOIN apply_promotion a on p.id_promotion = a.id_promotion
JOIN room_type r on a.id_type = r.id_type);

CREATE VIEW view_room_not_cleaned AS
SELECT r.room_number
FROM
(SELECT r.room_number, max(check_out_date) as max_check_out
FROM reservation r
GROUP BY r.room_number) r
LEFT JOIN
(SELECT c.room_number, max(cleaning_date) as max_clean_date
FROM cleaning c
GROUP BY c.room_number
) c on r.room_number = c.room_number
WHERE c.max_clean_date is null or r.max_check_out > c.max_clean_date and max_check_out <= now();

delimiter ;