import streamlit as st
import data_loader as dl

st.title('Budget Planner')

def show_budget_data():
    column_names = {
        'month':'Month',
        'income_source':'Income Source',
        'income':'Income',
        'category':'Category',
        'planned_amount':'Planned Amount'
    }
    budget_data = dl.load_budget_data()
    st.dataframe(budget_data, column_config=column_names)

show_budget_data()