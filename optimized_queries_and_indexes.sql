-- Part 1: Index Creation

-- Index for Customer Lookups by Name and Email
CREATE NONCLUSTERED INDEX IX_Customers_LastName ON Customers(LastName) INCLUDE (FirstName);
CREATE NONCLUSTERED INDEX IX_Customers_Email ON Customers(Email);

-- Index for Foreign Keys (Crucial for Joins)
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID ON Orders(CustomerID);
CREATE NONCLUSTERED INDEX IX_OrderDetails_OrderID ON OrderDetails(OrderID);
CREATE NONCLUSTERED INDEX IX_OrderDetails_ProductID ON OrderDetails(ProductID);

-- Index for Date Range Searches (Covering Index for the aggregation query)
CREATE NONCLUSTERED INDEX IX_Orders_OrderDate_TotalAmount ON Orders(OrderDate) INCLUDE (TotalAmount);


-- Part 2: Optimized Queries

-- Optimized Query 1: Email Search
SELECT * 
FROM Customers 
WHERE Email LIKE '%@gmail.com'; 

-- Optimized Query 2: SARGable Date Range
SELECT SUM(TotalAmount) 
FROM Orders 
WHERE OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01';

-- Optimized Query 3: Efficient Joins
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

-- Optimized Query 4: EXISTS instead of IN
SELECT p.ProductName
FROM Products p
WHERE EXISTS (
    SELECT 1 
    FROM OrderDetails od 
    WHERE od.ProductID = p.ProductID
);
