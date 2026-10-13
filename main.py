import streamlit as st
import data_loader as dl

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

def filter_what_to_show():
    budget_data = dl.load_budget_data()
    st.subheader('Filter')
    
    filters = ['Show All', 'Show Selected Year Only', 'Show Selected Month Only']
    filter = st.radio(
        'Filter',
        options=filters,
        key='filter1',
        persist_state='session',
        label_visibility='collapsed'
    )

    if filter == 'Show Selected Year Only':
        years = list({budg['month'].split()[1] for budg in budget_data})
        selected_year = st.selectbox(
            'Select Year',
            options=years,
            key='sel_year',
            persist_state='session'
        )
        if st.button('Save Filter'):
            st.session_state.selected_filter = ('Year', selected_year)
    elif filter == 'Show Selected Month Only':
        months = list({budg['month'] for budg in budget_data})
        selected_month = st.selectbox(
            'Select Month',
            options = months,
            key='sel_month',
            persist_state='session'
        )
        if st.button('Save Filter'):
            st.session_state.selected_filter = ('Month', selected_month)
    else:
        if st.button('Save Filter'):
            st.session_state.selected_filter = 'All'

with st.sidebar:
    select_currency()
    st.divider()
    filter_what_to_show()
        
pages.run()