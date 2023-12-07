CREATE FUNCTION gen_key(IN len INT, IN table_name VARCHAR(20), IN column_name VARCHAR(20)) RETURNS VARCHAR(20)
BEGIN
    DECLARE str VARCHAR(20);
    DECLARE str_query VARCHAR(20);
    DECLARE v1 INT;
    SET v1 = 1;

    WHILE v1>0 DO
        SELECT LEFT(MD5(RAND()), len) INTO str;
        SET str_query = CONCAT('SELECT COUNT(*) FROM ', table_name, ' WHERE ', column_name, '=', str);
        IF execute_immediate(str_query) = 0 THEN
            SET v1 = 0;
        end if;
    END WHILE;

    return str;
END;

CREATE PROCEDURE execute_immediate(IN query MEDIUMTEXT)
	MODIFIES SQL DATA
	SQL SECURITY DEFINER
BEGIN
	SET @q = query;
	PREPARE stmt FROM @q;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
END