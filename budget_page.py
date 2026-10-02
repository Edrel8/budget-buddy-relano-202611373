import streamlit as st
import data_loader as dl
import datetime

st.title('Budget Planner')

budget_data = dl.load_budget_data()
COLUMN_NAMES = {
        'month':'Month',
        'income_source':'Income Source',
        'income':'Income',
        'category':'Category',
        'planned_amount':'Planned Amount'
    }
MONTHS = [
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
CURR_YEAR = datetime.datetime.now().year

if 'notification' in st.session_state:
    st.toast(st.session_state.notification)
    del st.session_state.notification

def sort_budget_data(budget):
    budget.sort(key=lambda x: MONTHS.index(x['month'].split()[0]))
    budget.sort(key=lambda x: x['month'].split()[1])

def save_budget(action, *, edit_start_i=None, edit_stop_i=None):
    if action == 'Add':
        if type(st.session_state.new_budget) == list: 
            budget_data.extend(st.session_state.new_budget)
        elif type(st.session_state.new_budget) == dict:
            budget_data.append(st.session_state.new_budget)
    elif action == 'Edit':
        budget_data[edit_start_i: edit_stop_i + 1] = st.session_state.edited_budget
    sort_budget_data(budget_data)
    dl.save_budget_data(budget_data)

def show_budget_data(budget_data):
    st.dataframe(budget_data, column_config=COLUMN_NAMES)

def customization_buttons():
    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        if st.button('Add Budget'):
            add_budget_data()
    with col2:
        if st.button('Edit a Budget'):
            edit_budget_data()

@st.dialog('Add a Budget')
def add_budget_data():
    years = list(range(CURR_YEAR - 5, CURR_YEAR + 6))
    year = st.selectbox('Select Year', years)

    month = st.selectbox('Select Month', MONTHS)

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

@st.dialog('Edit Budget', width='medium')
def edit_budget_data():
    years = list({budg['month'].split()[1] for budg in budget_data})
    year = st.selectbox(
        'Select Year',
        options=years,
    )

    to_edit_data = []
    for budg in budget_data:
        if budg['month'].split()[1] == year:
            to_edit_data.append(budg)

    st.session_state.edited_budget = st.data_editor(
        to_edit_data, 
        column_config={
            'month': st.column_config.SelectboxColumn(
                'Month',
                options=[f'{month} {year}' for month in MONTHS],
                required=True
            ),
            'income_source': st.column_config.TextColumn(
                'Income Source',
                required=True
            ),
            'income': st.column_config.NumberColumn(
                'Income',
                format='%.1f',
                step=100.0,
                required=True
            ),
            'category': st.column_config.TextColumn(
                'Category',
                required=True
            ),
            'planned_amount': st.column_config.NumberColumn(
                'Planned Amount',
                format='%.1f',
                step=100.0,
                required=True
            )
        },
        num_rows='delete'
    )
    print(st.session_state.edited_budget)

    start_index = budget_data.index(to_edit_data[0])
    stop_index = budget_data.index(to_edit_data[-1])
    
    if st.button('Save'):
        save_budget('Edit', edit_start_i=start_index, edit_stop_i=stop_index)
        st.session_state.notification = 'Budget edited successfully!'
        st.rerun()

st.subheader('Actions:')
customization_buttons()
st.subheader('Allocated Budget')
show_budget_data(budget_data)
