-- Creates database candy_test_db
CREATE DATABASE IF NOT EXISTS candy_test_db;
USE candy_test_db;
CREATE USER IF NOT EXISTS 'candy_test'@'localhost';
SET PASSWORD FOR 'candy_test'@'localhost' = 'candy_test_pwd';
GRANT ALL PRIVILEGES ON candy_test_db.* TO 'candy_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'candy_test'@'localhost';
