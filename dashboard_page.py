import matplotlib.pyplot as plt
import streamlit as st
import data_loader as dl

st.title('Dashboard')

budget_data = dl.load_budget_data()
expense_data = dl.load_expense_data()

def select_month():
    months = list({budg['month'] for budg in budget_data})
    month = st.selectbox(
        'Select Month',
        months,
    )
    st.session_state.month = month

select_month()