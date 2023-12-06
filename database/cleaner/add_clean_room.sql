CREATE PROCEDURE add_clean_room(IN _id_staff INT, IN _room_number CHAR(3))
BEGIN
    INSERT INTO cleaning(cleaning_date, room_number, id_staff) VALUES (NOW(), _room_number, _id_staff);
end;