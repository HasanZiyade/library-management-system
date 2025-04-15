-- @block
-- Delete library database
DROP DATABASE IF EXISTS library;

-- @block
-- Create the library database
CREATE DATABASE IF NOT EXISTS library;
USE library;

-- Create the books table
CREATE TABLE IF NOT EXISTS books (
    `Book ID` VARCHAR(20) PRIMARY KEY,
    `Title` VARCHAR(255) NOT NULL,
    `Author` VARCHAR(100) NOT NULL,
    `Genre` VARCHAR(50) NOT NULL,
    `Publication Year` INT,
    `Copies Available` INT NOT NULL
);

-- Create the members table
CREATE TABLE IF NOT EXISTS members (
    `ID Number` VARCHAR(10) NOT NULL,
    `Membership Number` VARCHAR(10) PRIMARY KEY,
    `Name` VARCHAR(100) NOT NULL,
    `Contact Info` VARCHAR(20),
    `Membership Type` VARCHAR(20) NOT NULL,
    `Join Date` DATE NOT NULL,
    `Expiration Date` DATE NOT NULL,
    INDEX (`ID Number`)  -- Add index for faster lookups by ID Number
);

-- Create the loans table
CREATE TABLE IF NOT EXISTS loans (
    `Loan Number` VARCHAR(10) PRIMARY KEY,
    `Book ID` VARCHAR(20) NOT NULL,
    `Member ID` VARCHAR(10) NOT NULL,
    `Loan Date` DATE NOT NULL,
    `Due Date` DATE NOT NULL,
    `Return Date` DATE,
    FOREIGN KEY (`Book ID`) REFERENCES books(`Book ID`),
    FOREIGN KEY (`Member ID`) REFERENCES members(`Membership Number`)
);



-- @block
-- Copy books data from backup
INSERT INTO library.books
SELECT * FROM backup.books;

-- Copy members data from backup
INSERT INTO library.members
SELECT * FROM backup.members;

-- Copy loans data from backup
INSERT INTO library.loans
SELECT * FROM backup.loans;

-- @block
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);
-- @block
USE library;
-- Verify the data was imported correctly
SELECT COUNT(*) AS 'Number of Books' FROM books;
SELECT COUNT(*) AS 'Number of Members' FROM members;
SELECT COUNT(*) AS 'Number of Loans' FROM loans;

