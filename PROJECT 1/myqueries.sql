USE expenses_project;

SELECT * FROM expenses_project.expenses;

SELECT category, COUNT(*) AS total_transactions
FROM expenses
GROUP BY category
ORDER BY total_transactions DESC;

SELECT payment_mode, AVG(amount) AS avg_expense_per_transaction
FROM expenses
GROUP BY payment_mode;

SELECT category, SUM(cashback) AS total_cashback
FROM expenses
GROUP BY category
ORDER BY total_cashback DESC;

SELECT * FROM expenses
ORDER BY amount DESC
LIMIT 3;

SELECT SUM(amount) AS total_spent_on_healthcare
FROM expenses
WHERE category = 'Healthcare' AND YEAR(date) = 2024;

SELECT COUNT(*) AS total_transactions_last_week
FROM expenses
WHERE date BETWEEN CURDATE() - INTERVAL 7 DAY AND CURDATE();

SELECT category, YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
FROM expenses
WHERE date > CURDATE() - INTERVAL 3 MONTH
GROUP BY category, YEAR(date), MONTH(date)
HAVING total_spent > (SELECT SUM(amount)
                       FROM expenses
                       WHERE category = expenses.category
                       AND YEAR(date) = YEAR(CURDATE()) - 1
                       AND MONTH(date) = MONTH(CURDATE()) - 1)
ORDER BY total_spent DESC;

SELECT DAYOFWEEK(date) AS weekday, SUM(amount) AS total_spent
FROM expenses
WHERE category = 'Food'
GROUP BY DAYOFWEEK(date)
ORDER BY weekday;

SELECT category, SUM(amount) AS total_spent
FROM expenses
GROUP BY category
LIMIT 0, 5000;

SELECT description, COUNT(*) AS occurrence_count
FROM expenses
GROUP BY description
ORDER BY occurrence_count DESC
LIMIT 5;

SELECT payment_mode, AVG(cashback / amount) * 100 AS avg_cashback_percentage
FROM expenses
GROUP BY payment_mode;

SELECT SUM(amount) AS total_entertainment_and_travel_spending
FROM expenses
WHERE category IN ('Entertainment', 'Travel') AND YEAR(date) = 2024;

SELECT category, SUM(amount) AS total_spent_on_weekends
FROM expenses
WHERE DAYOFWEEK(date) IN (1, 7) -- 1 is Sunday and 7 is Saturday
GROUP BY category
ORDER BY total_spent_on_weekends DESC;

SELECT 
    current_month.year,
    current_month.month,
    (current_month.total_spent - previous_month.total_spent) / previous_month.total_spent * 100 AS percentage_change
FROM
    (SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
     FROM expenses
     WHERE YEAR(date) = YEAR(CURDATE()) AND MONTH(date) = MONTH(CURDATE()) 
     GROUP BY YEAR(date), MONTH(date)) AS current_month
JOIN
    (SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
     FROM expenses
     WHERE YEAR(date) = YEAR(CURDATE()) AND MONTH(date) = MONTH(CURDATE()) - 1
     GROUP BY YEAR(date), MONTH(date)) AS previous_month
ON current_month.year = previous_month.year
AND current_month.month = previous_month.month;

SELECT category, SUM(amount) AS total_spent
FROM expenses
WHERE YEAR(date) = 2024
GROUP BY  category
ORDER BY total_spent DESC;
