# Database Performance Optimization Report

**Date:** January 8, 2026
**Target Database:** E-Commerce Mock DB
**Analyst:** Gemini CLI

## Executive Summary
An analysis of the database schema and frequently executed queries revealed several performance bottlenecks. The primary issues stem from missing non-clustered indexes on foreign key columns, use of non-SARGable functions in `WHERE` clauses, and inefficient string matching patterns. Implementing the recommended indexing strategy and query rewrites is expected to significantly reduce CPU usage and I/O operations.

## Identified Issues & Recommendations

### 1. Inefficient String Search (Full Table Scan)
**Query:** Finding customers by email domain (`WHERE Email LIKE '%@gmail.com'`).
**Issue:** The leading wildcard (`%`) prevents the SQL Server optimizer from seeking an index. It forces a scan of the entire `Customers` table.
**Recommendation:** 
- If searching by domain is critical, consider adding a computed column for `EmailDomain` and indexing it.
- Generally, ensure an index exists on `Email` to speed up exact match lookups or prefix searches.

### 2. Non-SARGable Date Filter
**Query:** aggregating sales by year (`WHERE YEAR(OrderDate) = 2024`).
**Issue:** Applying the `YEAR()` function to the `OrderDate` column prevents the use of any index on that column (Non-SARGable).
**Recommendation:** 
- **Rewrite:** Change the condition to a range check (`OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01'`).
- **Index:** Create a Non-Clustered Index on `OrderDate` including `TotalAmount`.

### 3. Missing Foreign Key Indexes
**Query:** Customer Order History (Multi-table `JOIN`).
**Issue:** While Primary Keys are indexed by default, the Foreign Key columns (`Orders.CustomerID`, `OrderDetails.OrderID`, `OrderDetails.ProductID`) are not. This leads to inefficient Join operations (e.g., Hash Joins or Scans instead of Nested Loop Seeks).
**Recommendation:** Create Non-Clustered indexes on all Foreign Key columns.

### 4. Subquery Optimization
**Query:** List products with orders.
**Issue:** The use of `IN` with a subquery combined with `DISTINCT` can be less efficient than `EXISTS`.
**Recommendation:** Rewrite using `EXISTS` which allows the engine to stop scanning the child table once a match is found.

## Implementation Plan
Please execute the scripts provided in `optimized_queries_and_indexes.sql` to apply the index changes and view the rewritten queries.
