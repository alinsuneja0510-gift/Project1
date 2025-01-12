USE expenses_project;

SELECT * FROM expenses_project.expenses;

SELECT category, SUM(amount) AS total_spent
FROM expenses
GROUP BY category;

SELECT payment_mode, SUM(amount) AS total_spent
FROM expenses
GROUP BY payment_mode;

SELECT SUM(cashback) AS total_cashback
FROM expenses;

SELECT category, SUM(amount) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC
LIMIT 5;

SELECT payment_mode, SUM(amount) AS total_spent
FROM expenses
WHERE category = 'Transportation'
GROUP BY payment_mode;

SELECT * 
FROM expenses
WHERE cashback > 0;

SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
FROM expenses
GROUP BY YEAR(date), MONTH(date);

SELECT YEAR(date) AS year, MONTH(date) AS month, category, SUM(amount) AS total_spent
FROM expenses
WHERE category IN ('Travel', 'Entertainment', 'Gifts')
GROUP BY YEAR(date), MONTH(date), category
ORDER BY total_spent DESC;

SELECT category, MONTH(date) AS month, COUNT(*) AS occurrences
FROM expenses
WHERE category IN ('Subscription', 'Housing') -- Adjust the categories if needed
GROUP BY category, MONTH(date)
HAVING COUNT(*) > 1;

SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(cashback) AS total_cashback
FROM expenses
GROUP BY YEAR(date), MONTH(date);

SELECT YEAR(date) AS year, SUM(amount) AS total_spent
FROM expenses
GROUP BY YEAR(date)
ORDER BY year;

SELECT category, AVG(amount) AS avg_cost
FROM expenses
WHERE category IN ('Housing', 'Food', 'Transportation')
GROUP BY category;

SELECT DAYOFWEEK(date) AS weekday, SUM(amount) AS total_spent
FROM expenses
WHERE category = 'Food'
GROUP BY DAYOFWEEK(date);

SELECT category,
       CASE
           WHEN category IN ('Rent', 'Bills') THEN 'High Priority'
           ELSE 'Low Priority'
       END AS priority
FROM expenses
GROUP BY category;

SELECT category, 
       (SUM(amount) / (SELECT SUM(amount) FROM expenses) * 100) AS percentage_of_total
FROM expenses
GROUP BY category
ORDER BY percentage_of_total DESC
LIMIT 1;

