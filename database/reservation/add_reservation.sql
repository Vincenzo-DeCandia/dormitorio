CREATE PROCEDURE add_reservation(IN _check_in_date VARCHAR(10), IN _check_out_date VARCHAR(10), IN _id_user INT, IN _name_type VARCHAR(10))
BEGIN
    INSERT INTO reservation(check_in_date, check_out_date, reservation_date, start_date, end_date, id_user, name_type, room_number)
    VALUES (_check_in_date, _check_out_date, NOW(), null, null, _id_user, _name_type, null);
end;