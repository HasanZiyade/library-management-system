-- @block
-- Step 1: Create Persons table (stores unique persons based on ID Number)
CREATE TABLE IF NOT EXISTS persons (
    `ID Number` VARCHAR(10) PRIMARY KEY,
    `Name` VARCHAR(100) NOT NULL,
    `Contact Info` VARCHAR(20)
);

-- Step 2: Create Memberships table (stores membership details)
CREATE TABLE IF NOT EXISTS memberships (
    `Membership Number` VARCHAR(10) PRIMARY KEY,
    `ID Number` VARCHAR(10) NOT NULL,
    `Membership Type` VARCHAR(20) NOT NULL,
    `Join Date` DATE NOT NULL,
    `Expiration Date` DATE NOT NULL,
    FOREIGN KEY (`ID Number`) REFERENCES persons(`ID Number`)
);

-- Step 3: Migrate data from the original members table
-- First, populate the persons table with unique ID Numbers
INSERT INTO persons (`ID Number`, `Name`, `Contact Info`)
SELECT DISTINCT `ID Number`, `Name`, `Contact Info` 
FROM members;

-- Then, populate the memberships table
INSERT INTO memberships (`Membership Number`, `ID Number`, `Membership Type`, `Join Date`, `Expiration Date`)
SELECT `Membership Number`, `ID Number`, `Membership Type`, `Join Date`, `Expiration Date`
FROM members;

-- Step 4: Update the loans table to reference the new memberships table
-- (This step isn't needed because we're keeping the same Membership Number as PK)

-- @block
-- Step 5: Verify the migrated data
SELECT COUNT(*) AS 'Number of Unique Persons' FROM persons;
SELECT COUNT(*) AS 'Number of Memberships' FROM memberships;

-- @block
-- Step 6: Display sample data from normalized tables
SELECT * FROM persons LIMIT 5;
SELECT * FROM memberships LIMIT 5;

-- Find all memberships for a specific person(Example)
SELECT p.`Name`, p.`Contact Info`, m.`Membership Type`, m.`Join Date`, m.`Expiration Date`
FROM persons p
JOIN memberships m ON p.`ID Number` = m.`ID Number`
WHERE p.`ID Number` = '78463'
ORDER BY m.`Join Date` DESC;

-- Find all current active memberships(Example)
SELECT p.`Name`, p.`Contact Info`, m.`Membership Type`, m.`Join Date`, m.`Expiration Date`
FROM persons p
JOIN memberships m ON p.`ID Number` = m.`ID Number`
WHERE m.`Expiration Date` >= CURDATE()
ORDER BY m.`Expiration Date`;


-- @block
-- Step 1: Find the name of the foreign key constraint
-- This gets the constraint name that we need to drop
SELECT CONSTRAINT_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'library' 
AND TABLE_NAME = 'loans'
AND REFERENCED_TABLE_NAME = 'members'
AND REFERENCED_COLUMN_NAME = 'Membership Number';

-- @block
-- Step 2: Drop the foreign key constraint (replace 'constraint_name' with the actual name from step 1)
-- For example, it might be loans_ibfk_2 or something similar
ALTER TABLE loans
DROP FOREIGN KEY loans_ibfk_2; -- Replace with actual constraint name from step 1

-- @block
-- Step 3: Add new foreign key constraint referencing memberships table
ALTER TABLE loans
ADD CONSTRAINT fk_loans_memberships
FOREIGN KEY (`Member ID`) REFERENCES memberships(`Membership Number`);

-- @block
-- Step 4: Now we can safely drop the redundant members table
DROP TABLE IF EXISTS members;

-- @block
-- Step 6: Verify relationships are working correctly
SELECT l.`Loan Number`, b.`Title`, p.`Name`
FROM loans l
JOIN books b ON l.`Book ID` = b.`Book ID`
JOIN memberships m ON l.`Member ID` = m.`Membership Number`
JOIN persons p ON m.`ID Number` = p.`ID Number`
LIMIT 5;
