-- Simulated Slow Queries

-- Query 1: Full Table Scan on Customers due to leading wildcard
-- Goal: Find customers with Gmail accounts
SELECT * 
FROM Customers 
WHERE Email LIKE '%@gmail.com';

-- Query 2: Function on indexed column (SARGable issue) & Missing Index on OrderDate
-- Goal: Calculate total sales for the year 2024
SELECT SUM(TotalAmount) 
FROM Orders 
WHERE YEAR(OrderDate) = 2024;

-- Query 3: Missing Foreign Key Indexes causing nested loop join inefficiencies
-- Goal: Get order details for a specific customer
SELECT 
    c.FirstName, 
    c.LastName, 
    o.OrderDate, 
    p.ProductName, 
    od.Quantity, 
    od.UnitPrice
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN OrderDetails od ON o.OrderID = od.OrderID
JOIN Products p ON od.ProductID = p.ProductID
WHERE c.LastName = 'Smith';

-- Query 4: Inefficient Subquery / DISTINCT
-- Goal: List products that have been ordered at least once
SELECT DISTINCT p.ProductName
FROM Products p
WHERE p.ProductID IN (SELECT ProductID FROM OrderDetails);
