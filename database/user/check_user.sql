CREATE PROCEDURE check_user(IN username CHAR(16), IN password VARCHAR(20), OUT found INT)
BEGIN
    SELECT count(*) INTO found
    FROM student s
    WHERE fiscal_code=username and s.password=password;
end;