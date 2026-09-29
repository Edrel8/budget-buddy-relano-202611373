import streamlit as st
import data_loader as dl

st.title('Expenses')

def show_expense_data():
    column_names = {
        'date':'Date',
        'month':'Month',
        'category':'Category',
        'description':'Description',
        'amount':'Amount'
        }
    
    expense_data = dl.load_expense_data()
    st.dataframe(expense_data, column_config=column_names)

show_expense_data()