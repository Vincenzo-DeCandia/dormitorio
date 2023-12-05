CREATE PROCEDURE create_user(IN matr CHAR(10),IN _email VARCHAR(60), IN _fiscal_code CHAR(16),IN _password VARCHAR(20), IN _name VARCHAR(20), IN _surname VARCHAR(20), IN email VARCHAR(20), IN _gender CHAR(1), IN _role VARCHAR(15))
BEGIN
    INSERT INTO user (id_user, matriculation_number, email, fiscal_code, password, name, surname, gender, role)
    VALUES (default, matr, _email, _fiscal_code, _password, _name, _surname, _gender, _role);
end;

