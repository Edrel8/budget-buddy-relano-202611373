import streamlit as st
import data_loader as dl
import datetime

st.title('Budget Planner')

budget_data = dl.load_budget_data()

if 'notification' in st.session_state:
    st.toast(st.session_state.notification)
    del st.session_state.notification

def sort_budget_data():
    pass

def save_budget(action):
    if action == 'Add':
        if type(st.session_state.new_budget) == list: 
            budget_data.extend(st.session_state.new_budget)
        elif type(st.session_state.new_budget) == dict:
            budget_data.append(st.session_state.new_budget)
    elif action == 'Edit':
        pass
    elif action == 'Delete':
        pass
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
        if st.button('Add Budget'):
            add_budget_data()
    with col2:
        st.button('Edit a Budget')
    with col3:
        st.button('Delete a Budget')

@st.dialog('Add a Budget')
def add_budget_data():
    curr_year = datetime.datetime.now().year
    curr_month = datetime.datetime.now().month

    years = list(range(curr_year, curr_year + 6))
    year = st.selectbox('Select Year', years)

    months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
        ]
    month = st.selectbox('Select Month', months)

    income_sources = list({budg['income_source'] for budg in budget_data})
    income_source = st.selectbox(
        'Income Source',
        income_sources,
        accept_new_options=True
        )

    income = st.number_input(
        'Income',
        value=0.0,
        step=100.0,
        format='%.1f')

    categories = list({budg['category'] for budg in budget_data})
    selected_categories = st.multiselect(
        'Select Categories',
        categories,
        accept_new_options=True
        )

    if len(selected_categories) > 1:
        planned_amounts = []
        for category in selected_categories:
            planned_amount = st.number_input(
                f'Planned Amount on {category}',
                value=0.0,
                step=100.0,
                format='%.1f'
                )
            planned_amounts.append(planned_amount)
    elif len(selected_categories) == 1:
        category = selected_categories[0]
        planned_amount = st.number_input(
            f'Planned Amount on {category}',
            value=0.0,
            step=100.0,
            format='%.1f'
            )

    if len(selected_categories) > 1:
        st.session_state.new_budget = []
        for i, category in enumerate(selected_categories):
            new_budget = {
                'month': f'{month} {year}',
                'income_source': income_source,
                'income': income,
                'category': category,
                'planned_amount': planned_amounts[i]
            }
            st.session_state.new_budget.append(new_budget)
    elif len(selected_categories) == 1:
        st.session_state.new_budget = {
            'month': f'{month} {year}',
            'income_source': income_source,
            'income': income,
            'category': category,
            'planned_amount': planned_amount
        }
    
    if st.button('Add'):
        save_budget('Add')
        st.session_state.notification = 'Budget added successfully!'
        st.rerun()

def edit_budget_data():
    pass

def del_budget_data():
    pass

st.subheader('Actions:')
customization_buttons()
st.subheader('Allocated Budget')
show_budget_data()
