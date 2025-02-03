import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Cryptocurrency Information")

crypto_name = st.sidebar.text_input("Enter the cryptocurrency name or ticker:")

if crypto_name:
    st.write(f"You entered: {crypto_name}")
else:
    st.write("Please enter a cryptocurrency name or ticker in the sidebar.")

