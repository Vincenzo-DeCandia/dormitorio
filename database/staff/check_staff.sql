CREATE PROCEDURE check_staff(IN username CHAR(16), IN password VARCHAR(20), OUT found INT)
BEGIN
    SELECT count(*) INTO found
    FROM staff s
    WHERE s_fiscal_code=username and s.password=password;
end;