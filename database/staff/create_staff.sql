CREATE PROCEDURE create_staff(IN fiscal_code CHAR(16),IN _password VARCHAR(20), IN name VARCHAR(20), IN surname VARCHAR(20), IN email VARCHAR(20), IN gender CHAR(1), IN _role VARCHAR(15))
BEGIN
    INSERT INTO staff(id_staff, s_fiscal_code, s_name, s_surname, s_email, s_gender, role, password)
    VALUES (default, fiscal_code, sha2(_password, 256), name, surname, email, gender, _role);
end;