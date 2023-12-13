CREATE PROCEDURE add_reservation(IN _check_in_date VARCHAR(10), IN _check_out_date VARCHAR(10), IN _id_user INT, IN _name_type VARCHAR(20))
BEGIN
    DECLARE id_name INT;
    SELECT id_type INTO id_name FROM room_type WHERE name_type = _name_type;
    INSERT INTO reservation(id_reservation, check_in_date, check_out_date, reservation_date, start_date, end_date, id_user, id_type, room_number)
    VALUES (0, _check_in_date, _check_out_date, NOW(), null, null, _id_user, id_name, null);
end;
