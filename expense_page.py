import streamlit as st
import data_loader as dl
import datetime

st.title('Expenses')

expense_data = dl.load_expense_data()
BUDGET_DATA = dl.load_budget_data()
COLUMN_NAMES = {
        'date':'Date',
        'month':'Month',
        'category':'Category',
        'description':'Description',
        'amount':'Amount'
        }

if 'notification' in st.session_state:
    st.toast(st.session_state.notification)
    del st.session_state.notification

def sort_expense_history(data):
    data.sort(key=lambda x: x['date'])

def save_expense_history(action):
    sort_expense_history(expense_data)
    if action == 'Add':
        dl.add_expense(st.session_state.expense_entry)
    if action == 'Edit':
        pass

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
    allow_submission = False

    date = st.date_input(
        'Input Date',
        max_value=datetime.date.today()
        )

    month = st.text_input(
        'Month',
        value=datetime.date.strftime(date, '%B %Y'),
        disabled=True
        )

    categories = list({budg['category'] for budg in BUDGET_DATA})
    category = st.selectbox(
        'Select Category',
        categories,
    )

    description = st.text_input(
        'Description'
    )

    amount = st.number_input(
        'Amount of Expense',
        min_value=0.0,
        format='%.1f'
    )

    st.session_state.expense_entry = {
        'date': date,
        'month': month,
        'category': category,
        'description': description,
        'amount': amount
    }

    if date and category and description and amount:
        if st.button('Add Entry'):
            save_expense_history('Add')
            st.session_state.notification = 'Expense entry successfully added!'
            st.rerun()
    else: st.warning('Do not leave anything blank.')

@st.dialog('Edit Expense History')
def edit_expense_data():
    pass

st.subheader('Actions:')
customization_buttons()

st.subheader('Expense History')
show_expense_data()