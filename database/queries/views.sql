-- @block
-- Create a view for current borrowers with active loans
CREATE VIEW CurrentBorrowings AS
SELECT 
    l.`Loan Number`,
    b.`Title`,
    b.`Author`,
    p.`Name` AS 'Borrower',
    p.`Contact Info` AS 'Contact',
    m.`Membership Type`,
    l.`Loan Date`,
    l.`Due Date`,
    DATEDIFF(l.`Due Date`, CURRENT_DATE()) AS 'Days Remaining',
    CASE
        WHEN l.`Due Date` < CURRENT_DATE() THEN 'Overdue'
        WHEN DATEDIFF(l.`Due Date`, CURRENT_DATE()) <= 3 THEN 'Due Soon'
        ELSE 'Active'
    END AS 'Status'
FROM 
    loans l
JOIN books b ON l.`Book ID` = b.`Book ID`
JOIN memberships m ON l.`Member ID` = m.`Membership Number`
JOIN persons p ON m.`ID Number` = p.`ID Number`
WHERE 
    l.`Return Date` = '0000-00-00';



-- @block
-- Create a view summarizing member activity statistics
CREATE VIEW MemberActivitySummary AS
SELECT 
    p.`ID Number`,
    p.`Name`,
    COUNT(DISTINCT m.`Membership Number`) AS 'Total Memberships',
    MAX(m.`Expiration Date`) AS 'Latest Expiration',
    CASE 
        WHEN MAX(m.`Expiration Date`) >= CURRENT_DATE() THEN 'Active'
        ELSE 'Expired'
    END AS 'Current Status',
    COUNT(l.`Loan Number`) AS 'Total Loans',
    SUM(CASE WHEN l.`Return Date` = '0000-00-00' THEN 1 ELSE 0 END) AS 'Current Loans',
    SUM(CASE 
        WHEN l.`Return Date` != '0000-00-00' AND l.`Return Date` > l.`Due Date` THEN 1 
        ELSE 0 
    END) AS 'Late Returns',
    ROUND(AVG(
        CASE 
            WHEN l.`Return Date` != '0000-00-00' 
            THEN DATEDIFF(l.`Return Date`, l.`Loan Date`)
            ELSE NULL
        END
    ), 1) AS 'Avg Loan Duration (Days)'
FROM 
    persons p
LEFT JOIN memberships m ON p.`ID Number` = m.`ID Number`
LEFT JOIN loans l ON m.`Membership Number` = l.`Member ID`
GROUP BY 
    p.`ID Number`, p.`Name`;





-- @block
-- Create a view for book popularity analytics
CREATE VIEW BookPopularityStats AS
SELECT 
    b.`Book ID`,
    b.`Title`,
    b.`Author`,
    b.`Genre`,
    b.`Copies Available`,
    COUNT(l.`Loan Number`) AS 'Total Loans',
    SUM(CASE WHEN l.`Return Date` = '0000-00-00' THEN 1 ELSE 0 END) AS 'Currently Loaned',
    ROUND(COUNT(l.`Loan Number`) / b.`Copies Available`, 2) AS 'Loans Per Copy',
    ROUND(AVG(
        CASE 
            WHEN l.`Return Date` != '0000-00-00' 
            THEN DATEDIFF(l.`Return Date`, l.`Loan Date`)
            ELSE NULL
        END
    ), 1) AS 'Avg Loan Duration (Days)',
    CASE
        WHEN COUNT(l.`Loan Number`) / b.`Copies Available` > 10 THEN 'Very High'
        WHEN COUNT(l.`Loan Number`) / b.`Copies Available` > 5 THEN 'High'
        WHEN COUNT(l.`Loan Number`) / b.`Copies Available` > 2 THEN 'Medium'
        ELSE 'Low'
    END AS 'Demand Level'
FROM 
    books b
LEFT JOIN loans l ON b.`Book ID` = l.`Book ID`
GROUP BY 
    b.`Book ID`, b.`Title`, b.`Author`, b.`Genre`, b.`Copies Available`;
