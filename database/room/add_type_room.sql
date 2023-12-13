CREATE PROCEDURE add_room(IN _name_type VARCHAR(20),IN _description VARCHAR(400), IN _price FLOAT)
BEGIN
    INSERT INTO room_type(id_type, name_type, price, description) VALUES (0, _name_type, _price, _description);
end;

commit;