CREATE PROCEDURE add_room(IN _name_type VARCHAR(10),IN _description VARCHAR(400), IN _price FLOAT)
BEGIN
    INSERT INTO room_type(name_type, price, description) VALUES (_name_type, _price, _description);
end;