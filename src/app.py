import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')

def fetch_data():
    """Fetch cryptocurrency data from the PostgreSQL database."""
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    query = """
        SELECT 
            name, 
            symbol, 
            price, 
            market_cap,
            market_cap_dominance,
            percentage_change_24h, 
            percentage_change_30d,
            timestamp
        FROM student.sn_crypto_data;
    """
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df


st.title("Cryptocurrency Comparison Dashboard")


df = fetch_data()


st.sidebar.header("Select Cryptocurrencies")
selected_cryptos = st.sidebar.multiselect(
    "Choose cryptocurrencies to compare:", options=df["name"].unique(), default=["Bitcoin", "Ethereum"]
)

metric_to_plot = st.sidebar.selectbox(
    "Select a metric to visualize:", ["price", "market_cap", "percentage_change_24h", "percentage_change_30d"]
)

st.sidebar.header("Insights")
st.sidebar.write("Select cryptocurrencies from the sidebar to compare their performance across various metrics.")
st.sidebar.write("Use the dropdown menu above to visualize specific metrics like price, market capitalization, and percentage changes.")

filtered_data = df[df["name"].isin(selected_cryptos)]

most_recent_data = filtered_data.loc[filtered_data.groupby("name")["timestamp"].idxmax()]

tab1, tab2 = st.tabs(["Selected Data", "Visualizations"])

with tab1:
    st.header("Selected Cryptocurrencies Data")
    st.dataframe(filtered_data)

with tab2:
    st.header("Cryptocurrency Performance")

    if not filtered_data.empty:
        st.subheader("Line Graph of Selected Metric Over Time")
        for crypto in selected_cryptos:
            crypto_data = filtered_data[filtered_data["name"] == crypto]
            plt.plot(crypto_data["timestamp"], crypto_data[metric_to_plot], label=crypto)
        plt.xlabel("Timestamp")
        plt.ylabel(metric_to_plot.replace('_', ' ').title())
        plt.title(f"{metric_to_plot.replace('_', ' ').title()} Over Time")
        plt.legend()
        st.pyplot(plt)

        st.subheader("Bar Chart of Current Metric Values")
        fig, ax = plt.subplots()
        ax.bar(most_recent_data["name"], most_recent_data[metric_to_plot], color="skyblue")
        ax.set_title(f"{metric_to_plot.replace('_', ' ').title()} Comparison (Most Recent)")
        ax.set_ylabel(metric_to_plot.replace('_', ' ').title())
        ax.set_xlabel("Cryptocurrency")
        st.pyplot(fig)

        st.subheader("Market Dominance Pie Chart (Normalised)")
        fig, ax = plt.subplots()
        ax.pie(
            most_recent_data["market_cap_dominance"], 
            labels=most_recent_data["name"], 
            autopct="%1.1f%%", 
            startangle=90, 
            colors=plt.cm.Paired.colors
        )
        ax.set_title("Market Cap Dominance")
        st.pyplot(fig)
    else:
        st.warning("No cryptocurrencies selected for comparison.")
