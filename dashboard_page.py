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

def filter_by_month():
    st.session_state.month_budget = [
        budg for budg in budget_data
        if budg['month'] == st.session_state.month
    ]
    st.session_state.month_expense = [
        exp for exp in expense_data
        if exp['month'] == st.session_state.month
    ]

def display_month_summary():
    pass

def budget_categ_pie(budget_data):
    categ_amounts = {}
    for budg in budget_data:
        if budg['category'] not in categ_amounts:
            categ_amounts[budg['category']] = budg['planned_amount']
        else:
            categ_amounts[budg['category']] += budg['planned_amount']
    amounts = categ_amounts.values()
    categories = categ_amounts.keys()
    fig1, ax1 = plt.subplots()
    ax1.set_title(
        'Budget Distribution',
        fontsize='14',
        fontweight='bold',
        color='white'
        )
    fig1.patch.set_alpha(0.0)
    budg_pie = ax1.pie(
        amounts,
        labels=categories,
        textprops={'color': 'white'}
        )
    ax1.pie_label(budg_pie, amounts)
    st.pyplot(fig1)
    

select_month()
filter_by_month()
budget_categ_pie(st.session_state.month_budget)
