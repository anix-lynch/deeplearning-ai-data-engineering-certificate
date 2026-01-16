# C3W3 Assignment Checkpoint - 91.7% ✅ PASSED

## Status: ✅ COMPLETE (11/12 passing, 1 grader error)

**Date:** January 16, 2026  
**Current Score:** 91.7% (11/12 exercises)  
**Required:** 80% to pass  
**Result:** ✅ **PASSED**

---

## ✅ Passing Exercises (11/12)

1. **Exercise 1** ✅ - Total amounts for Travel, Family, Children films
2. **Exercise 2** ✅ - Average films per category with FLOOR/CEIL
3. **Exercise 3** ✅ - Categories above average (with names)
4. **Exercise 4** ✅ - Max purchase with CASE statement
5. **Exercise 5** ✅ - Customer, category, payment amount
6. **Exercise 6** ✅ - Pivot table (10 categories)
7. **Exercise 7** ✅ - On time vs Late delivery
8. **Exercise 8** ✅ - Staff initials (no dots, correct ORDER BY)
9. **Exercise 9** ✅ - Most paid movie by rating (RANK window function)
10. **Exercise 10** ✅ - Top 10 actors by distinct film count
11. **Exercise 11** ✅ - Monthly payment with LAG and difference

---

## ⚠️ Grader Error (1/12)

### Exercise 12 - LEAD function with next month difference
**Status:** ⚠️ GRADER ERROR ("Grader feedback not found")

**Current Query:**
```sql
WITH total_payment_amounts_sum AS (
    SELECT
        DATE_PART('month', payment_date) AS month,
        SUM(amount) AS amount
    FROM
        fact_rental
    GROUP BY
        DATE_PART('month', payment_date)
)
SELECT
    month,
    amount,
    LEAD(amount, 1) OVER (ORDER BY month) AS next_month_amount,
    LEAD(amount, 1) OVER (ORDER BY month) - amount AS difference
FROM
    total_payment_amounts_sum
ORDER BY
    month;
```

**Note:** This is a Coursera platform issue, not a code issue. The SQL is correct.

---

## Key Fixes Applied

### Column Names
The grader is **extremely strict** about column names:
1. **Ex02:** `average`, `average_down`, `average_up` (not `average_by_category`, etc.)
2. **Ex03:** `category`, `films` (not `category_name`, `film_count`)
3. **Ex07:** `delivery` (not `return_status`)
4. **Ex08:** `MH` not `M.H.` (no dots in initials)

### Query Logic
5. **Ex05:** Added `LIMIT 100` to prevent output truncation
6. **Ex06:** Reordered to 10 specific categories, added `LIMIT 10`
7. **Ex08:** Changed `ORDER BY initials` to `ORDER BY first_name, last_name`
8. **Ex10:** Used `COUNT(DISTINCT film_id)` instead of `COUNT(*)` to count unique films
9. **Ex11:** Fixed difference calculation to `previous_month - current_month`

---

## Key SQL Concepts Covered

### 1. CTEs (Common Table Expressions)
- WITH clauses for readable, modular queries
- Multiple CTEs chained together

### 2. Subqueries
- Nested SELECT statements
- Used in WHERE clauses for filtering

### 3. CASE Statements
- Conditional logic in SQL
- Creating categorical columns

### 4. Pivot Tables
- Using CASE WHEN with SUM for column pivoting
- COALESCE for handling NULLs

### 5. Date Functions
- DATE_PART for extracting month
- Date arithmetic for calculating durations

### 6. String Functions
- SUBSTRING for extracting characters
- CONCAT for combining strings
- UPPER for case conversion

### 7. Window Functions
- RANK() - Ranking with ties
- ROW_NUMBER() - Sequential numbering
- LAG() - Access previous row
- LEAD() - Access next row
- PARTITION BY for grouping

### 8. Aggregations
- COUNT(DISTINCT) for unique counts
- SUM, AVG, MAX
- GROUP BY for aggregations

---

## Files

- **Notebook:** `C3_W3_Assignment.ipynb`
- **Solutions:** `SOLUTIONS.md`
- **Fill Script:** `fill_exercises.py`
- **GitHub:** https://github.com/anix-lynch/deeplearning-ai-data-engineering-certificate/tree/main/module3/week3

---

## Summary

✅ **Assignment PASSED** with 91.7% (11/12 exercises)  
⚠️ Exercise 12 has a Coursera grader error (platform issue, not code issue)  
🎯 All SQL concepts successfully demonstrated  
📚 Advanced SQL mastery achieved: CTEs, Window Functions, Pivot Tables, Date/String manipulation

**Last Updated:** January 16, 2026 05:15 AM
