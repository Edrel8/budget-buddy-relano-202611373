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

def save_expense_history(action,*, index=None):
    sort_expense_history(expense_data)
    if action == 'Add':
        dl.add_expense(st.session_state.expense_entry)
    elif action == 'Edit':
        expense_data[index] = st.session_state.edited_entry
        dl.save_expense_data(expense_data)
    elif action == 'Delete':
        expense_data.pop(index)
        dl.save_expense_data(expense_data)

def show_expense_data():
    st.dataframe(expense_data, column_config=COLUMN_NAMES, height='content')

def customization_buttons():
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        if st.button('Add Expense Entry'):
            add_expense_entry()
    with col2:
        if st.button('Edit Expense Entry'):
            edit_expense_history()
    with col3:
        if st.button('Delete Expense Entry'):
            del_expense_entry()

@st.dialog('Add an Expense Entry')
def add_expense_entry():
    allow_submission = False

    date = st.date_input(
        'Input Date',
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
        step=100.0,
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
def edit_expense_history():
    index = st.number_input(
        'Select Index to Edit',
        min_value=0,
        max_value=len(expense_data) - 1,
    )

    date = st.date_input(
        'Input Date',
        value=expense_data[index]['date']
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
        index=categories.index(expense_data[index]['category'])
    )

    description = st.text_input(
        'Description',
        value=expense_data[index]['description']
    )

    amount = st.number_input(
        'Amount of Expense',
        min_value=0.0,
        value=expense_data[index]['amount'],
        step=100.0,
        format='%.1f'
    )
    
    st.session_state.edited_entry = {
        'date': date,
        'month': month,
        'category': category,
        'description': description,
        'amount': amount
    }

    if date and category and description and amount:
        if st.button('Save Edits'):
            save_expense_history('Edit', index=index)
            st.session_state.notification = 'Expense entry successfully edited!'
            st.rerun()
    else: st.warning('Do not leave anything blank.')

@st.dialog('Delete an Expense Entry')
def del_expense_entry():
    index = st.number_input(
        'Select Index to Edit',
        min_value=0,
        max_value=len(expense_data) - 1,
    )

    date = st.date_input(
        'Input Date',
        value=expense_data[index]['date'],
        disabled=True
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
        index=categories.index(expense_data[index]['category']),
        disabled=True
    )

    description = st.text_input(
        'Description',
        value=expense_data[index]['description'],
        disabled=True
    )

    amount = st.number_input(
        'Amount of Expense',
        min_value=0.0,
        value=expense_data[index]['amount'],
        step=100.0,
        format='%.1f',
        disabled=True
    )
    
    st.session_state.entry_to_del = {
        'date': date,
        'month': month,
        'category': category,
        'description': description,
        'amount': amount
    }

    if st.button('Delete Entry'):
        save_expense_history('Delete', index=index)
        st.session_state.notification = 'Expense entry successfully deleted!'
        st.rerun()

st.subheader('Actions:')
customization_buttons()

st.subheader('Expense History')
show_expense_data()