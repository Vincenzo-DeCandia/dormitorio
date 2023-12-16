CREATE PROCEDURE add_promotion(IN name_room VARCHAR(20), IN p_name VARCHAR(20), IN start TIMESTAMP, IN end TIMESTAMP, IN discount INT, IN _desc VARCHAR(400))
BEGIN

    DECLARE id_p INT;
    DECLARE id_room INT;
    SELECT id_type INTO id_room
    FROM room_type
    WHERE name_type=name_room;

    INSERT INTO promotion(id_promotion, promotion_name, p_start_date, p_end_date, percent_discount)
    VALUES (0, p_name, start, end, discount);


    INSERT INTO apply_promotion(id_promotion, id_type, description) VALUES (id_p, id_room, _desc);
end;