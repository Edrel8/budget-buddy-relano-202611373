import streamlit as st
import data_loader as dl

st.title('Expenses')

def show_expense_data():
    expense_data = dl.load_expense_data()
    st.dataframe(expense_data)

show_expense_data()