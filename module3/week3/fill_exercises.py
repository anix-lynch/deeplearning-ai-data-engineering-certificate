#!/usr/bin/env python3
"""Fill in C3W3 SQL exercises"""

import json

# Read the notebook
with open('C3_W3_Assignment.ipynb', 'r') as f:
    nb = json.load(f)

# Exercise solutions
solutions = {
    'ex01': """%%sql
SELECT
    store_id,
    dim_category.name AS category_name,
    SUM(amount) AS total_amount
FROM
    fact_rental
    INNER JOIN dim_category ON fact_rental.category_id = dim_category.category_id
WHERE
    dim_category.name IN ('Travel', 'Family', 'Children')
    AND rental_date BETWEEN '2005-06-01' AND '2005-08-01'
GROUP BY
    store_id, dim_category.name
ORDER BY
    store_id, category_name;""",
    
    'ex02': """%%sql
WITH distinct_films AS (
    SELECT DISTINCT 
        category_id,
        film_id
    FROM
        fact_rental
),
films_per_category AS (
    SELECT
        category_id,
        COUNT(*) AS film_count
    FROM
        distinct_films
    GROUP BY
        category_id
),
films_average_by_category AS (
    SELECT
        AVG(film_count) AS average_by_category
    FROM
        films_per_category
)
SELECT
    average_by_category AS average,
    FLOOR(average_by_category) AS average_down,
    CEIL(average_by_category) AS average_up
FROM
    films_average_by_category;""",
    
    'ex03': """%%sql
WITH distinct_films AS (
    SELECT DISTINCT 
        category_id,
        film_id
    FROM
        fact_rental
),
films_per_category AS (
    SELECT
        category_id,
        COUNT(*) AS film_count
    FROM
        distinct_films
    GROUP BY
        category_id
),
categories_above_average AS (
    SELECT
        category_id,
        film_count
    FROM
        films_per_category
    WHERE
        film_count > (
            SELECT CEIL(AVG(film_count))
            FROM films_per_category
        )
)
SELECT
    dim_category.name AS category,
    categories_above_average.film_count AS films
FROM
    categories_above_average
    INNER JOIN dim_category ON categories_above_average.category_id = dim_category.category_id
ORDER BY
    category;""",
    
    'ex04': """%%sql
WITH max_amount_customer AS (
    SELECT
        customer_id,
        MAX(amount) AS max_amount,
        DATE(payment_date) AS payment_date
    FROM
        fact_rental
    WHERE
        payment_date BETWEEN '2007-04-30 15:00:00' AND '2007-04-30 16:00:00'
    GROUP BY
        customer_id, DATE(payment_date)
)
SELECT
    UPPER(CONCAT(dim_customer.first_name, ' ', dim_customer.last_name)) AS full_name,
    max_amount_customer.max_amount,
    max_amount_customer.payment_date,
    CASE
        WHEN max_amount_customer.max_amount BETWEEN 0 AND 3 THEN 'low'
        WHEN max_amount_customer.max_amount BETWEEN 3 AND 6 THEN 'mid'
        WHEN max_amount_customer.max_amount > 6 THEN 'high'
    END AS value_rate
FROM
    max_amount_customer
    INNER JOIN dim_customer ON max_amount_customer.customer_id = dim_customer.customer_id
ORDER BY
    max_amount_customer.max_amount DESC, full_name ASC;""",
    
    'ex05': """%%sql
SELECT
    CONCAT(dim_customer.first_name, ' ', dim_customer.last_name) AS full_name,
    dim_category.name AS category_name,
    fact_rental.amount
FROM
    fact_rental
    INNER JOIN dim_customer ON fact_rental.customer_id = dim_customer.customer_id
    INNER JOIN dim_category ON fact_rental.category_id = dim_category.category_id
ORDER BY
    full_name, category_name, amount
LIMIT 100;""",
    
    'ex06': """%%sql
SELECT
    full_name,
    COALESCE(SUM(CASE WHEN category_name = 'Family' THEN amount END), 0) AS Family,
    COALESCE(SUM(CASE WHEN category_name = 'Games' THEN amount END), 0) AS Games,
    COALESCE(SUM(CASE WHEN category_name = 'Animation' THEN amount END), 0) AS Animation,
    COALESCE(SUM(CASE WHEN category_name = 'Classics' THEN amount END), 0) AS Classics,
    COALESCE(SUM(CASE WHEN category_name = 'Documentary' THEN amount END), 0) AS Documentary,
    COALESCE(SUM(CASE WHEN category_name = 'Sports' THEN amount END), 0) AS Sports,
    COALESCE(SUM(CASE WHEN category_name = 'New' THEN amount END), 0) AS New,
    COALESCE(SUM(CASE WHEN category_name = 'Children' THEN amount END), 0) AS Children,
    COALESCE(SUM(CASE WHEN category_name = 'Music' THEN amount END), 0) AS Music,
    COALESCE(SUM(CASE WHEN category_name = 'Travel' THEN amount END), 0) AS Travel
FROM (
    SELECT
        CONCAT(dim_customer.first_name, ' ', dim_customer.last_name) AS full_name,
        dim_category.name AS category_name,
        fact_rental.amount
    FROM
        fact_rental
        INNER JOIN dim_customer ON fact_rental.customer_id = dim_customer.customer_id
        INNER JOIN dim_category ON fact_rental.category_id = dim_category.category_id
) AS customer_category_amounts
GROUP BY
    full_name
ORDER BY
    full_name
LIMIT 10;""",
    
    'ex07': """%%sql
SELECT
    customer_id,
    CASE
        WHEN DATE_PART('day', return_date - rental_date) <= rental_duration THEN 'On time'
        ELSE 'Late'
    END AS delivery
FROM
    fact_rental
    INNER JOIN dim_film ON fact_rental.film_id = dim_film.film_id
WHERE
    payment_date BETWEEN '2007-04-30 15:00:00' AND '2007-04-30 16:00:00'
ORDER BY
    customer_id;""",
    
    'ex08': """%%sql
SELECT
    CONCAT(SUBSTRING(first_name, 1, 1), SUBSTRING(last_name, 1, 1)) AS initials
FROM
    dim_staff
ORDER BY
    initials;""",
    
    'ex09': """%%sql
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
    rank_movies = 1;""",
    
    'ex10': """%%sql
WITH actor_film AS (
    SELECT
        dim_actor.actor_id,
        dim_actor.first_name,
        dim_actor.last_name,
        fact_rental.film_id
    FROM
        dim_actor
        INNER JOIN bridge_actor ON dim_actor.actor_id = bridge_actor.actor_id
        INNER JOIN fact_rental ON bridge_actor.rental_id = fact_rental.rental_id
),
actor_film_count AS (
    SELECT
        actor_id,
        first_name,
        last_name,
        COUNT(DISTINCT film_id) AS films
    FROM
        actor_film
    GROUP BY
        actor_id, first_name, last_name
),
actors_rank AS (
    SELECT
        first_name,
        last_name,
        films,
        ROW_NUMBER() OVER (ORDER BY films DESC, first_name ASC, last_name ASC) AS actor_rank
    FROM
        actor_film_count
)
SELECT
    first_name,
    last_name,
    films,
    actor_rank
FROM
    actors_rank
WHERE
    actor_rank <= 10
ORDER BY
    actor_rank;""",
    
    'ex11': """%%sql
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
    LAG(amount, 1) OVER (ORDER BY month) AS previous_month_amount
FROM
    total_payment_amounts_sum
ORDER BY
    month;""",
    
    'ex12': """%%sql
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
    LEAD(amount, 1) OVER (ORDER BY month) AS next_month_amount
FROM
    total_payment_amounts_sum
ORDER BY
    month;"""
}

# Find and replace exercise cells
for cell in nb['cells']:
    if 'metadata' in cell and 'tags' in cell['metadata']:
        tags = cell['metadata']['tags']
        for ex_num in solutions:
            if ex_num in tags and 'graded' in tags:
                print(f"Filling {ex_num}")
                cell['source'] = [solutions[ex_num]]

# Write back
with open('C3_W3_Assignment.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("✅ All exercises filled!")
