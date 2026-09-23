import streamlit as st

dashboard_page = st.Page('dashboard_page.py', title='Dashboard')
budget_page = st.Page('budget_page.py', title='Budget Planner', url_path='budget-planner')
expense_page = st.Page('expense_page.py', title='Expense Tracker', url_path='expense-tracker')

pages = st.navigation([dashboard_page, budget_page, expense_page])
pages.run()