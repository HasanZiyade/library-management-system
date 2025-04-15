-- @block
-- Basic query: Find all books in the "Science Fiction" genre with more than 5 copies available
SELECT `Book ID`, `Title`, `Author`, `Copies Available`
FROM books
WHERE `Genre` = 'Science Fiction' AND `Copies Available` > 5
ORDER BY `Title`;

-- @block
-- Multi-table JOIN query: Find all currently borrowed books (not returned) with borrower information
SELECT b.`Title`, b.`Author`, p.`Name` AS "Borrower", 
       l.`Loan Date`, l.`Due Date`,
       CASE WHEN l.`Return Date` = '0000-00-00' THEN 'Not Returned' ELSE 'Returned' END AS "Status"
FROM loans l
JOIN books b ON l.`Book ID` = b.`Book ID`
JOIN memberships m ON l.`Member ID` = m.`Membership Number`
JOIN persons p ON m.`ID Number` = p.`ID Number`
WHERE l.`Return Date` = '0000-00-00'
ORDER BY l.`Due Date`;

-- @block
-- GROUP BY with aggregates: Find the most popular genres by number of loans:
SELECT b.`Genre`, COUNT(*) AS "Total Loans", 
       COUNT(DISTINCT l.`Member ID`) AS "Unique Borrowers"
FROM loans l
JOIN books b ON l.`Book ID` = b.`Book ID`
GROUP BY b.`Genre`
ORDER BY COUNT(*) DESC;

-- @block
-- Subquery example: Find members who have borrowed more books than the average borrower:
SELECT p.`Name`, COUNT(*) AS "Books Borrowed"
FROM loans l
JOIN memberships m ON l.`Member ID` = m.`Membership Number`
JOIN persons p ON m.`ID Number` = p.`ID Number`
GROUP BY p.`ID Number`, p.`Name`
HAVING COUNT(*) > (
    SELECT AVG(book_count) 
    FROM (
        SELECT COUNT(*) AS book_count
        FROM loans l2
        JOIN memberships m2 ON l2.`Member ID` = m2.`Membership Number`
        GROUP BY m2.`ID Number`
    ) AS borrower_counts
)
ORDER BY COUNT(*) DESC;

-- @block
-- EXISTS clause: Find all books that have never been borrowed
SELECT b.`Book ID`, b.`Title`, b.`Author`
FROM books b
WHERE NOT EXISTS (
    SELECT 1
    FROM loans l
    WHERE l.`Book ID` = b.`Book ID`
)
ORDER BY b.`Title`;


-- @block
-- Complex query: Analyze overdue books with lateness categories and calculate potential fines:
SELECT 
    b.`Title`,
    p.`Name` AS "Borrower",
    l.`Due Date`,
    DATEDIFF(CURDATE(), l.`Due Date`) AS "Days Overdue",
    CASE 
        WHEN DATEDIFF(CURDATE(), l.`Due Date`) <= 7 THEN 'Slightly Overdue'
        WHEN DATEDIFF(CURDATE(), l.`Due Date`) <= 30 THEN 'Moderately Overdue'
        ELSE 'Severely Overdue'
    END AS "Overdue Status",
    CASE 
        WHEN m.`Membership Type` = 'Student' THEN DATEDIFF(CURDATE(), l.`Due Date`) * 0.10
        WHEN m.`Membership Type` = 'Senior' THEN DATEDIFF(CURDATE(), l.`Due Date`) * 0.05
        ELSE DATEDIFF(CURDATE(), l.`Due Date`) * 0.25
    END AS "Estimated Fine ($)"
FROM loans l
JOIN books b ON l.`Book ID` = b.`Book ID`
JOIN memberships m ON l.`Member ID` = m.`Membership Number`
JOIN persons p ON m.`ID Number` = p.`ID Number`
WHERE l.`Return Date` = '0000-00-00' 
AND l.`Due Date` < CURDATE()
ORDER BY DATEDIFF(CURDATE(), l.`Due Date`) DESC;
