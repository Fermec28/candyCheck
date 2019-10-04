-- Creates database candy_check_db
CREATE DATABASE IF NOT EXISTS candy_check_db;
USE candy_check_db;
CREATE USER IF NOT EXISTS 'candy_check'@'localhost';
SET PASSWORD FOR 'candy_check'@'localhost' = 'candy_check_pwd';
GRANT ALL PRIVILEGES ON candy_check_db.* TO 'candy_check'@'localhost';
GRANT SELECT ON performance_schema.* TO 'candy_check'@'localhost';
