import streamlit as st
import data_loader as dl
import datetime

st.title('Budget Planner')

budget_data = dl.load_budget_data()

if 'will_add' not in st.session_state:
    st.session_state.will_add = False
if 'will_edit' not in st.session_state:
    st.session_state.will_edit = False
if 'will_del' not in st.session_state:
    st.session_state.will_del = False

def sort_budget_data():
    pass

def go_to_add():
    st.session_state.will_add = True
    st.session_state.will_edit = False
    st.session_state.will_del = False

def go_to_edit():
    st.session_state.will_edit = True
    st.session_state.will_add = False
    st.session_state.will_del = False

def go_to_del():
    st.session_state.will_del = True
    st.session_state.will_edit = False
    st.session_state.will_add = False

def save_budget():
    st.session_state.will_add = False
    st.session_state.will_edit = False
    st.session_state.will_del = False

    budget_data.append(st.session_state.new_budget)
    dl.save_budget_data(budget_data)

def show_budget_data():
    column_names = {
        'month':'Month',
        'income_source':'Income Source',
        'income':'Income',
        'category':'Category',
        'planned_amount':'Planned Amount'
    }
    st.dataframe(budget_data, column_config=column_names)

def customization_buttons():
    col1, col2, col3, col4 = st.columns([1,1,1,2])
    with col1:
        st.button('Add Budget', on_click=go_to_add)
    with col2:
        st.button('Edit a Budget', on_click=go_to_edit)
    with col3:
        st.button('Delete a Budget', on_click=go_to_del)

def add_budget_data():
    curr_year = datetime.datetime.now().year
    curr_month = datetime.datetime.now().month

    years = list(range(curr_year, curr_year + 6))
    year = st.selectbox('Select Year', years)

    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    month = st.selectbox('Select Month', months)

    income_sources = list({budg['income_source'] for budg in budget_data})
    income_source = st.selectbox('Income Source', income_sources + ['Other'])
    if income_source == 'Other':
        income_source = st.text_input('If Other Income Source')

    income = st.text_input('Income')
    if not income.isdigit():
        st.warning('Please enter a positive integer.')
    else: income = int(income)

    categories = list({budg['category'] for budg in budget_data})
    category = st.selectbox('Category', categories + ['Other'])
    if category == 'Other':
        category = st.text_input('If Other Category:')

    planned_amount = st.text_input('Planned Amount')
    if not planned_amount.isdigit():
        st.warning('Please enter a positive integer')
    else: planned_amount = int(planned_amount)

    st.session_state.new_budget = {
        'month': f'{month} {year}',
        'income_source': income_source,
        'income': income,
        'category': category,
        'planned_amount': planned_amount
    }
    print(st.session_state.added_budget)
    if type(income) == int and type(planned_amount) == int:
        st.button('Add', on_click=save_budget)

def edit_budget_data():
    pass

def del_budget_data():
    pass

customization_buttons()
if st.session_state.will_add:
    add_budget_data()
elif st.session_state.will_edit:
    edit_budget_data()
elif st.session_state.will_del:
    del_budget_data()
else:
    show_budget_data()
