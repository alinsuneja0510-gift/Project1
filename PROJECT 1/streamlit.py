import streamlit as st
import mysql.connector
import pandas as pd
import altair as alt


# Function to connect to the database
def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="P@sSw0rD051o",  # Update with your MySQL password
            database="expenses_project"  # Update with your database name
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None

# Function to execute queries
def execute_query(query):
    connection = get_connection()
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return pd.DataFrame(result)
        except mysql.connector.Error as err:
            st.error(f"Error executing query: {err}")
            return None
    else:
        return None
    

# Streamlit App
st.title("Welcome to My Streamlit App! 🎉")
st.subheader("Visualizing my spending patterns and get actionable insights.")


# Sidebar navigation
st.sidebar.title("Navigation")



# Batch 1 Queries
batch1_queries = {
    "Total Spent by Category": """
        SELECT category, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY category;
    """,
    "Total Spent by Payment Mode": """
        SELECT payment_mode, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY payment_mode;
    """,
    "Total Cashback": """
        SELECT SUM(cashback) AS total_cashback
        FROM expenses;
    """,
    "Top 5 Categories by Spending": """
        SELECT category, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY category
        ORDER BY total_spent DESC
        LIMIT 5;
    """,
    "Spending on Transportation by Payment Mode": """
        SELECT payment_mode, SUM(amount) AS total_spent
        FROM expenses
        WHERE category = 'Transportation'
        GROUP BY payment_mode;
    """,
    "Expenses with Cashback": """
        SELECT * 
        FROM expenses
        WHERE cashback > 0;
    """,
    "Monthly Spending": """
        SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY YEAR(date), MONTH(date);
    """,
    "Spending on Select Categories (Travel, Entertainment, Gifts)": """
        SELECT YEAR(date) AS year, MONTH(date) AS month, category, SUM(amount) AS total_spent
        FROM expenses
        WHERE category IN ('Travel', 'Entertainment', 'Gifts')
        GROUP BY YEAR(date), MONTH(date), category
        ORDER BY total_spent DESC;
    """,
    "Frequent Transactions for Subscription/Housing": """
        SELECT category, MONTH(date) AS month, COUNT(*) AS occurrences
        FROM expenses
        WHERE category IN ('Subscription', 'Housing')
        GROUP BY category, MONTH(date)
        HAVING COUNT(*) > 1;
    """,
    "Monthly Cashback": """
        SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(cashback) AS total_cashback
        FROM expenses
        GROUP BY YEAR(date), MONTH(date);
    """,
    "Yearly Spending": """
        SELECT YEAR(date) AS year, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY YEAR(date)
        ORDER BY year;
    """,
    "Average Cost by Category (Travel)": """
        SELECT category, AVG(amount) AS avg_cost
        FROM expenses
        WHERE category IN ('Flights', 'Accommodation', 'Transportation')
        GROUP BY category;
    """,
    "Food Spending by Day of the Week": """
        SELECT DAYOFWEEK(date) AS weekday, SUM(amount) AS total_spent
        FROM expenses
        WHERE category = 'Food'
        GROUP BY DAYOFWEEK(date);
    """,
    "Priority by Category": """
        SELECT category,
               CASE
                   WHEN category IN ('Rent', 'Bills') THEN 'High Priority'
                   ELSE 'Low Priority'
               END AS priority
        FROM expenses
        GROUP BY category;
    """,
    "Top Category by Spending Percentage": """
        SELECT category, 
               (SUM(amount) / (SELECT SUM(amount) FROM expenses) * 100) AS percentage_of_total
        FROM expenses
        GROUP BY category
        ORDER BY percentage_of_total DESC
        LIMIT 1;
    """
}



# Batch 2 Queries
batch2_queries = {
    "Total Transactions by Category": """
        SELECT category, COUNT(*) AS total_transactions
        FROM expenses
        GROUP BY category
        ORDER BY total_transactions DESC;
    """,
    "Average Expense Per Transaction by Payment Mode": """
        SELECT payment_mode, AVG(amount) AS avg_expense_per_transaction
        FROM expenses
        GROUP BY payment_mode;
    """,
    "Total Cashback by Category": """
        SELECT category, SUM(cashback) AS total_cashback
        FROM expenses
        GROUP BY category
        ORDER BY total_cashback DESC;
    """,
    "Top 3 Most Expensive Transactions": """
        SELECT * FROM expenses
        ORDER BY amount DESC
        LIMIT 3;
    """,
    "Total Spent on Healthcare in 2024": """
        SELECT SUM(amount) AS total_spent_on_healthcare
        FROM expenses
        WHERE category = 'Healthcare' AND YEAR(date) = 2024;
    """,
    "Total Transactions Last Week": """
        SELECT COUNT(*) AS total_transactions_last_week
        FROM expenses
        WHERE date BETWEEN CURDATE() - INTERVAL 7 DAY AND CURDATE();
    """,
    "Total Spending in Last 3 Months by Category": """
        SELECT category, YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
        FROM expenses
        WHERE date > CURDATE() - INTERVAL 3 MONTH
        GROUP BY category, YEAR(date), MONTH(date)
        ORDER BY total_spent DESC;
    """,
    "Spending on Food by Day of the Week": """
        SELECT DAYOFWEEK(date) AS weekday, SUM(amount) AS total_spent
        FROM expenses
        WHERE category = 'Food'
        GROUP BY DAYOFWEEK(date)
        ORDER BY weekday;
    """,
    "Category Spending (Limited to 5000)": """
        SELECT category, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY category
        LIMIT 0, 5000;
    """,
    "Top 5 Most Frequent Descriptions": """
        SELECT description, COUNT(*) AS occurrence_count
        FROM expenses
        GROUP BY description
        ORDER BY occurrence_count DESC
        LIMIT 5;
    """,
    "Average Cashback Percentage by Payment Mode": """
        SELECT payment_mode, AVG(cashback / amount) * 100 AS avg_cashback_percentage
        FROM expenses
        GROUP BY payment_mode;
    """,
    "Total Entertainment and Travel Spending in 2024": """
        SELECT SUM(amount) AS total_entertainment_and_travel_spending
        FROM expenses
        WHERE category IN ('Entertainment', 'Travel') AND YEAR(date) = 2024;
    """,
    "Total Weekend Spending by Category": """
        SELECT category, SUM(amount) AS total_spent_on_weekends
        FROM expenses
        WHERE DAYOFWEEK(date) IN (1, 7)
        GROUP BY category
        ORDER BY total_spent_on_weekends DESC;
    """,
    "Percentage Change in Spending by Month": """
        SELECT 
            current_month.year,
            current_month.month,
            (current_month.total_spent - previous_month.total_spent) / previous_month.total_spent * 100 AS percentage_change
        FROM
            (SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
             FROM expenses
             WHERE date > CURDATE() - INTERVAL 2 MONTH
             GROUP BY YEAR(date), MONTH(date)) AS current_month
        JOIN
            (SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
             FROM expenses
             WHERE date > CURDATE() - INTERVAL 3 MONTH
             GROUP BY YEAR(date), MONTH(date)) AS previous_month
        ON current_month.year = previous_month.year
        AND current_month.month = previous_month.month;
    """,
    "Category Spending in 2024": """
        SELECT category, SUM(amount) AS total_spent
        FROM expenses
        WHERE YEAR(date) = 2024
        GROUP BY category
        ORDER BY total_spent DESC;
    """
}

batch = st.sidebar.selectbox("Select Batch", ["Batch 1", "Batch 2"])
if batch == "Batch 1":
    selected_query_name = st.sidebar.selectbox("Select a Query", list(batch1_queries.keys()))
    query = batch1_queries[selected_query_name]
else:
    selected_query_name = st.sidebar.selectbox("Select a Query", list(batch2_queries.keys()))
    query = batch2_queries[selected_query_name]

# Fetch and Visualize Data
if selected_query_name:
    st.subheader(selected_query_name)
    result_df = execute_query(query)

    if result_df is not None and not result_df.empty:
        st.write(result_df)

        chart = None  # Initialize chart as None to avoid undefined errors

        # Visualization with colors
        if "category" in result_df.columns and "total_spent" in result_df.columns:
            chart = alt.Chart(result_df).mark_bar().encode(
                x=alt.X("category:N", sort="-y", title="Category"),
                y=alt.Y("total_spent:Q", title="Total Spent"),
                color=alt.Color("category:N", legend=alt.Legend(title="Category"), scale=alt.Scale(scheme="tableau20")),
                tooltip=list(result_df.columns)
            ).properties(
                title="Category Spending",
                width=700,
                height=400
            )

        elif "payment_mode" in result_df.columns and "total_spent" in result_df.columns:
            chart = alt.Chart(result_df).mark_bar().encode(
                x=alt.X("payment_mode:N", sort="-y", title="Payment Mode"),
                y=alt.Y("total_spent:Q", title="Total Spent"),
                color=alt.Color("payment_mode:N", legend=alt.Legend(title="Payment Mode"), scale=alt.Scale(scheme="category10")),
                tooltip=list(result_df.columns)
            ).properties(
                title="Spending by Payment Mode",
                width=700,
                height=400
            )

        elif "weekday" in result_df.columns and "total_spent" in result_df.columns:
            chart = alt.Chart(result_df).mark_line(point=True).encode(
                x=alt.X("weekday:O", title="Day of the Week"),
                y=alt.Y("total_spent:Q", title="Total Spent"),
                color=alt.Color("weekday:O", legend=alt.Legend(title="Weekday"), scale=alt.Scale(scheme="accent")),
                tooltip=list(result_df.columns)
            ).properties(
                title="Spending by Day of the Week",
                width=700,
                height=400
            )

        # Check if chart is defined before trying to display it
        if chart is not None:
            st.altair_chart(chart)
        else:
            st.warning("No suitable columns found for visualization.")
    else:
        st.warning("No data returned for this query. Please try a different query or check your database.")