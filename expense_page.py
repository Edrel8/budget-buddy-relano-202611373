import streamlit as st
import data_loader as dl

st.title('Expenses')

expense_data = dl.load_expense_data()
COLUMN_NAMES = {
        'date':'Date',
        'month':'Month',
        'category':'Category',
        'description':'Description',
        'amount':'Amount'
        }

def show_expense_data():
    st.dataframe(expense_data, column_config=COLUMN_NAMES)

def customization_buttons():
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        if st.button('Add Expense Entry'):
            add_expense_entry()
    with col2:
        if st.button('Edit Expense History'):
            edit_expense_data()

@st.dialog('Add an Expense Entry')
def add_expense_entry():
    pass

@st.dialog('Edit Expense History')
def edit_expense_data():
    pass

st.subheader('Actions:')
customization_buttons()

st.subheader('Expense History')
show_expense_data()