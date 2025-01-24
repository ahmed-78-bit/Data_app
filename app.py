import sqlite3
import pandas as pd
import streamlit as st

def streamlit_app():
    # Connect to the SQLite database
    conn = sqlite3.connect('Köksglädje.db')

    # Load the necessary tables into DataFrames
    transactions = pd.read_sql_query("SELECT * FROM Transactions", conn)
    transaction_details = pd.read_sql_query("SELECT * FROM TransactionDetails", conn)
    stores = pd.read_sql_query("SELECT * FROM Stores", conn)

    # Merge the DataFrames to get the required columns
    merged_df = pd.merge(transactions, transaction_details, on='TransactionID')
    merged_df = pd.merge(merged_df, stores, on='StoreID')

    # Group by StoreID and StoreName, and calculate the total sales volume
    sales_volume = merged_df.groupby(['StoreID', 'StoreName']).agg({'TotalPrice': 'sum'}).reset_index()

    # Sort the result by TotalPrice in descending order
    sales_volume = sales_volume.sort_values(by='TotalPrice', ascending=False)

    # Streamlit app
    st.title('Sales Volume by Store')
    st.write('This app presents the sales volume for each store.')

    # Display the sales volume data
    st.dataframe(sales_volume)

    # Plot the sales volume data
    st.bar_chart(sales_volume.set_index('StoreName')['TotalPrice'])

# Call the function to run the Streamlit app
if __name__ == '__main__':
    streamlit_app()
