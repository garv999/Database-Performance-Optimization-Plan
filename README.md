# Database Performance Optimization Plan

## Contents

### 1. Reports & Analysis
- **`optimization_report.md`**: The main deliverable. A Markdown report detailing:
  - Executive Summary of findings.
  - Root cause analysis for performance bottlenecks (Full Table Scans, Non-SARGable predicates).
  - Specific recommendations for indexing and query refactoring.
- **`performance_comparison.csv`**: A dataset comparing estimated CPU costs and Logical Reads before and after optimization. Use this file in Excel to generate performance improvement charts.

### 2. Technical Scripts
- **`schema.sql`**: SQL script to generate the mock E-Commerce database tables (`Customers`, `Products`, `Orders`, `OrderDetails`).
- **`slow_queries.sql`**: SQL script containing the unoptimized, resource-intensive queries used for the baseline analysis.
- **`optimized_queries_and_indexes.sql`**: The solution script. Run this to:
  - Create the recommended Non-Clustered Indexes.
  - Execute the rewritten, optimized versions of the queries.

## Instructions
1. **Setup:** Run `schema.sql` in a SQL Server environment to create the tables.
2. **Baseline:** Run `slow_queries.sql` and observe the execution plan/costs.
3. **Fix:** Run `optimized_queries_and_indexes.sql` to apply fixes.
4. **Review:** Read `optimization_report.md` for the theoretical explanation and open `performance_comparison.csv` to see the projected metrics.
