CREATE PROCEDURE update_room(IN _room_number CHAR(3), IN _room_type VARCHAR(10))
BEGIN
    UPDATE room
    SET room_number = _room_number,
        name_type = IF(_room_type is null, name_type, _room_type)
    WHERE room_number = _room_number;
end;