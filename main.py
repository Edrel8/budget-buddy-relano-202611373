import streamlit as st

dashboard_page = st.Page('dashboard_page.py', title='Dashboard')
budget_page = st.Page('budget_page.py', title='Budget Planner', url_path='budget-planner')
expense_page = st.Page('expense_page.py', title='Expense Tracker', url_path='expense-tracker')

pages = st.navigation([dashboard_page, budget_page, expense_page])

def select_currency():
    currency_names = ['Dollar ($)', 'Euro (€)', 'Yen/Yuan (¥)', 'Pound (£)', 'Peso (₱)']
    currencies = {
        'Dollar ($)': '$',
        'Euro (€)': '€',
        'Yen/Yuan (¥)': '¥',
        'Pound (£)': '£',
        'Peso (₱)': '₱'
    }

    currency = st.selectbox(
        'Select Currency to Use',
        currency_names,
        index=4,
        key='currency1',
        persist_state='session'
    )

    if st.button('Save Currency'):
        st.session_state.currency = currencies[currency]

with st.sidebar:
    select_currency()
        
pages.run()