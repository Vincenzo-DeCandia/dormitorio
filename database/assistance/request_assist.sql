CREATE PROCEDURE request_assist(IN _id_staff INT, IN _id_user INT, IN _feedback INT)
BEGIN
    INSERT INTO assistance(assistance_date, feedback, id_staff, id_user) VALUES (NOW(), _feedback, _id_staff, _id_user);
end;