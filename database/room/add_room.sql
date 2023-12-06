CREATE PROCEDURE add_room(IN _room_number CHAR(3), _type_room VARCHAR(10))
BEGIN
    INSERT INTO room(room_number, name_type) VALUES (_room_number, _type_room);
end;