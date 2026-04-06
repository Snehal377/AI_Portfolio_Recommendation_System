CREATE DATABASE portfolio_db;

use portfolio_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100),users
    role VARCHAR(50)
);

select * from users;

UPDATE users SET username = TRIM(username);
UPDATE users SET password = TRIM(password);

