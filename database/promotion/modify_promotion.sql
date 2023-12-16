CREATE PROCEDURE modify_promotion(IN id_p INT, IN name_room VARCHAR(20), IN name_p VARCHAR(20), IN start_date TIMESTAMP, IN end_date TIMESTAMP, IN percent INT, IN _desc VARCHAR(20))
BEGIN

    -- if id is not null and name promotion is not null
    DECLARE id_room INT;
    SELECT id_type INTO id_room
    FROM room_type
    WHERE name_type=name_room;

    UPDATE apply_promotion
    SET id_type = IF(id_room, id_room, id_type),
        description = IF(_desc, _desc, description)
    WHERE id_promotion=id_p;

    UPDATE promotion
    SET promotion_name = IF(name_p, name_p, promotion_name),
        p_start_date = IF(start_date, start_date, p_start_date),
        p_end_date = IF(end_date, end_date, p_end_date),
        percent_discount = IF(percent, percent, percent_discount)
    WHERE id_promotion=id_p;
end;