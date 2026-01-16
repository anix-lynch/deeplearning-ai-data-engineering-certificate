# C3W3 Assignment Checkpoint - 70/80%

## Status: 🚧 In Progress (87.5% passing)

**Date:** January 16, 2026  
**Current Score:** 70/80 (87.5%)

---

## ✅ Passing Exercises (10/12)

1. **Exercise 1** ✅ - Total amounts for Travel, Family, Children films
2. **Exercise 2** ✅ - Average films per category with FLOOR/CEIL
3. **Exercise 3** ✅ - Categories above average (with names)
4. **Exercise 4** ✅ - Max purchase with CASE statement
5. **Exercise 5** ✅ - Customer, category, payment amount
6. **Exercise 6** ✅ - Pivot table (10 categories)
7. **Exercise 7** ✅ - On time vs Late delivery
8. **Exercise 8** ✅ - Staff initials (no dots)
9. **Exercise 10** ✅ - Top 10 actors by distinct film count
10. **Exercise 11** ✅ - Monthly payment with LAG and difference

---

## ❌ Failing Exercises (2/12)

### Exercise 9 - Most paid movie by rating (RANK window function)
**Status:** ❌ FAILING (0/10 points)

**Current Query:**
```sql
WITH movies_amount_rating AS (
    SELECT
        dim_film.title,
        dim_film.rating,
        SUM(fact_rental.amount) AS amount
    FROM
        fact_rental
        INNER JOIN dim_film ON fact_rental.film_id = dim_film.film_id
    GROUP BY
        dim_film.title, dim_film.rating
),
movies_ranking AS (
    SELECT
        title,
        rating,
        amount,
        RANK() OVER (PARTITION BY rating ORDER BY amount DESC) AS rank_movies
    FROM
        movies_amount_rating
)
SELECT
    title,
    rating,
    amount
FROM
    movies_ranking
WHERE
    rank_movies = 1;
```

**Issue:** Unknown - need to check grader output

---

### Exercise 12 - Monthly payment with LEAD and difference
**Status:** ❌ FAILING (0/10 points)

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

**Issue:** Unknown - need to check grader output

---

## Key Learnings

### Column Names Matter!
The grader is **extremely strict** about column names:
- `average` not `average_by_category`
- `category` not `category_name`
- `films` not `film_count`
- `delivery` not `return_status`
- `MH` not `M.H.`

### Common Fixes Applied
1. **Ex02:** Changed to `average`, `average_down`, `average_up`
2. **Ex03:** Changed to `category`, `films`
3. **Ex05:** Added `LIMIT 100` to prevent truncation
4. **Ex06:** Reordered columns, added `LIMIT 10`
5. **Ex07:** Changed to `delivery`
6. **Ex08:** Removed dots from initials
7. **Ex10:** Used `COUNT(DISTINCT film_id)` instead of `COUNT(*)`
8. **Ex11:** Added `difference` column

---

## Next Steps

1. Check grader feedback for ex09 and ex12
2. Likely column name or calculation issues
3. May need to adjust ORDER BY or data types

---

## Files

- **Notebook:** `C3_W3_Assignment.ipynb`
- **Solutions:** `SOLUTIONS.md`
- **Fill Script:** `fill_exercises.py`
- **GitHub:** https://github.com/anix-lynch/deeplearning-ai-data-engineering-certificate/tree/main/module3/week3

---

**Last Updated:** January 16, 2026 04:30 AM
