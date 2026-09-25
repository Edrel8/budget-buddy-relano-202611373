import streamlit as st
import data_loader as dl

st.title('Budget Planner')

def show_budget_data():
    budget_data = dl.load_budget_data()
    st.dataframe(budget_data)

show_budget_data()