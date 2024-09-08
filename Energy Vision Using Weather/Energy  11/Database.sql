CREATE DATABASE Energy;
 
USE Energy;

CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100)
);
INSERT INTO Users (firstname, lastname, email, password) 
VALUES 
('John', 'Doe', 'john@example.com', 'password123'),
('Jane', 'Doe', 'jane@example.com', 'securepassword456'),
('Alice', 'Smith', 'alice@example.com', 'strongpassword789');

SELECT * FROM Users;




