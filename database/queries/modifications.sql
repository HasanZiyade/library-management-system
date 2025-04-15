-- @block
-- Create Restocking Table for Low-Copy Books with High Demand
-- Creates a table of books that need to be ordered based on their circulation statistics

-- Create a table to track books needing restock
CREATE TABLE books_to_restock (
    `Book ID` VARCHAR(20) PRIMARY KEY,
    `Title` VARCHAR(255) NOT NULL,
    `Author` VARCHAR(100) NOT NULL,
    `Genre` VARCHAR(50) NOT NULL,
    `Current Copies` INT NOT NULL,
    `Total Loans` INT NOT NULL,
    `Current Loans` INT NOT NULL,
    `Recommended Purchase` INT NOT NULL,
    `Added Date` DATE DEFAULT (CURRENT_DATE)
);

-- Populate with books that have high demand but limited copies
INSERT INTO books_to_restock (
    `Book ID`, `Title`, `Author`, `Genre`, `Current Copies`, 
    `Total Loans`, `Current Loans`, `Recommended Purchase`
)
SELECT 
    b.`Book ID`, 
    b.`Title`, 
    b.`Author`, 
    b.`Genre`,
    b.`Copies Available` AS current_copies,
    COUNT(l.`Loan Number`) AS total_loans,
    SUM(CASE WHEN l.`Return Date` = '0000-00-00' THEN 1 ELSE 0 END) AS current_loans,
    -- Recommend purchases based on absolute demand vs supply
    CASE
        WHEN COUNT(l.`Loan Number`) > 20 AND b.`Copies Available` <= 5 THEN 5  -- High demand, low supply
        WHEN COUNT(l.`Loan Number`) > 15 AND b.`Copies Available` <= 8 THEN 3  -- Medium demand, medium supply
        WHEN COUNT(l.`Loan Number`) > 10 AND b.`Copies Available` <= 10 THEN 2 -- Moderate demand
        ELSE 1                                                                -- Low priority
    END AS recommended_purchase
FROM 
    books b
JOIN 
    loans l ON b.`Book ID` = l.`Book ID`
GROUP BY 
    b.`Book ID`, b.`Title`, b.`Author`, b.`Genre`, b.`Copies Available`
HAVING 
    -- Either has many loans overall
    COUNT(l.`Loan Number`) > 10
    -- OR has a high percentage of copies currently loaned out
    OR (SUM(CASE WHEN l.`Return Date` = '0000-00-00' THEN 1 ELSE 0 END) >= b.`Copies Available` * 0.3)
ORDER BY 
    COUNT(l.`Loan Number`) DESC;




-- @block
-- Update Books with Upcoming Renewal Reminders for Members
-- Flag books that are due soon and update them with renewal eligibility based on library policies:

-- First, add columns to track renewal information
ALTER TABLE loans 
ADD COLUMN `Renewal Status` VARCHAR(30) NULL;
-- First check which loans should be updated
SELECT COUNT(*) AS 'Loans meeting criteria'
FROM loans l
WHERE l.`Return Date` = '0000-00-00' 
AND DATEDIFF(l.`Due Date`, CURRENT_DATE()) BETWEEN -30 AND 7;

-- Update loans with renewal information - Fixed version
UPDATE loans l
JOIN books b ON l.`Book ID` = b.`Book ID`
JOIN memberships m ON l.`Member ID` = m.`Membership Number`
JOIN persons p ON m.`ID Number` = p.`ID Number`
LEFT JOIN (
    -- LEFT JOIN ensures we get results even for books with no current loans
    SELECT `Book ID`, COUNT(*) AS current_loan_count
    FROM loans
    WHERE `Return Date` = '0000-00-00'
    GROUP BY `Book ID`
) AS loan_counts ON loan_counts.`Book ID` = l.`Book ID`
SET 
    -- Make sure to handle NULL values in the CASE conditions
    l.`Renewal Status` = CASE 
        WHEN l.`Due Date` < CURRENT_DATE() THEN 'Ineligible - Overdue'
        WHEN COALESCE(loan_counts.current_loan_count, 0) >= b.`Copies Available` THEN 'Ineligible - High Demand'
        WHEN m.`Expiration Date` < CURRENT_DATE() THEN 'Ineligible - Expired Membership'
        WHEN DATEDIFF(l.`Due Date`, CURRENT_DATE()) <= 7 THEN 'Eligible - Due Soon'
        ELSE 'Eligible'
    END
WHERE 
    l.`Return Date` = '0000-00-00';  -- Remove the date range to update ALL current loans

-- Check the results of the update
SELECT 
    `Renewal Status`, 
    COUNT(*) AS 'Number of Books'
FROM 
    loans
WHERE 
    `Return Date` = '0000-00-00'
GROUP BY 
    `Renewal Status`
ORDER BY 
    COUNT(*) DESC;






-- @block
-- Delete old loan records that meet specific criteria to clean up the database while preserving important historical data:
-- Delete loan records that meet specific criteria
DELETE l FROM loans l
JOIN memberships m ON l.`Member ID` = m.`Membership Number`
JOIN books b ON l.`Book ID` = b.`Book ID`
WHERE 
    -- Only returned books (not currently on loan)
    l.`Return Date` != '0000-00-00' 
    -- For expired memberships (no longer active)
    AND m.`Expiration Date` < DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
    -- For common books with many copies available
    AND b.`Copies Available` > 5
    -- And the loans are old
    AND l.`Loan Date` < DATE_SUB(CURRENT_DATE(), INTERVAL 2 YEAR)
    -- Limit deletion to avoid removing too much history
    LIMIT 500;
