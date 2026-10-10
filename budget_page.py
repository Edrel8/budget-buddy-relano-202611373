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
        'planned_amount':'Planned Expenses',
        'unallocated': 'Unallocated Amount',
        'exceeded': 'Exceeded Amount'
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

def filter_by_month(month, year,*,budget_data=budget_data):
    month_year = f'{month} {year}'
    filtered_data = []
    for budg in budget_data:
        if (budg['month'] == month_year) and (budg not in filtered_data):
            filtered_data.append(budg)
    return filtered_data

def filter_by_income_source(income_source,*,budget_data=budget_data):
    filtered_data = []
    for budg in budget_data:
        if (budg['income_source'] == income_source) and (budg not in filtered_data):
            filtered_data.append(budg)
    return filtered_data

def save_budget(action, *, edit_start_i=None, edit_stop_i=None, delete_index=None):
    if action == 'Add':
        budget_data.extend(st.session_state.new_budget)
    elif action == 'Edit':
        budget_data[edit_start_i: edit_stop_i + 1] = st.session_state.edited_budget
    elif action == 'Delete':
        budget_data.pop(delete_index)
    sort_budget_data(budget_data)
    dl.save_budget_data(budget_data)

def show_budget_data(budget_data):
    st.dataframe(budget_data, column_config=COLUMN_NAMES)

def customization_buttons():
    col1, col2, col3, col4 = st.columns([1,1,1,2])
    with col1:
        if st.button('Add Budget'):
            add_budget_data()
    with col2:
        if st.button('Edit Budget'):
            edit_budget_data()
    with col3:
        if st.button('Delete Budget'):
            delete_budget_data()

@st.dialog('Add Budget')
def add_budget_data():
    allow_submission=False

    years = list(range(CURR_YEAR - 5, CURR_YEAR + 6))
    year = st.selectbox('Select Year', years, index=5)

    month = st.selectbox('Select Month', MONTHS)

    curr_month_budget = filter_by_month(month, year)

    income_sources = list({budg['income_source'] for budg in curr_month_budget})

    income_source = st.selectbox(
        'Income Source',
        income_sources,
        accept_new_options=True
        )

    source_budget = filter_by_income_source(income_source)

    if income_source not in income_sources:
        income = st.number_input(
            'Income',
            min_value=0.0,
            value=0.0,
            step=100.0,
            format='%.1f'
            )
    else:
        income = st.number_input(
            'Income',
            min_value=0.0,
            value=source_budget[0]['income'],
            step=100.0,
            format='%.1f',
            disabled=True
            )

    categories = list({budg['category'] for budg in budget_data})
    selected_categories = st.multiselect(
        'Select Categories',
        categories,
        accept_new_options=True
        )

    if len(selected_categories) > 0:
        planned_amounts = []
        for category in selected_categories:
            planned_amount = st.number_input(
                f'Planned Amount on {category}',
                value=0.0,
                step=100.0,
                format='%.1f'
                )
            planned_amounts.append(planned_amount)

    if len(selected_categories) > 0:
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
            allow_submission = True
    else: st.warning('Please select at least one category.')
    
    if allow_submission:
        if st.button('Add'):
            save_budget('Add')
            st.session_state.notification = 'Budget added successfully!'
            st.rerun()

@st.dialog('Edit Budget', width='medium', on_dismiss='rerun')
def edit_budget_data():
    allow_submission = True

    years = list({budg['month'].split()[1] for budg in budget_data})
    year = st.selectbox(
        'Select Year',
        options=years,
        )

    months = list({
        budg['month'].split()[0]
        for budg in budget_data
        if budg['month'].split()[1] == year
    })
    month = st.selectbox(
        'Select Month',
        options=months
    )

    to_edit_data = []
    for budg in budget_data:
        if budg['month'] == f'{month} {year}':
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
                min_value=0.0,
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
                min_value=0.0,
                step=100.0,
                required=True
            )
        },
        num_rows='fixed'
    )

    unique_incomes = set()
    month_list = list({budg['month'] for budg in st.session_state.edited_budget})
    for month in month_list:
        monthly_budget_data = filter_by_month(
            *month.split(),
            budget_data=st.session_state.edited_budget
            )
        for month_budg in monthly_budget_data:
            income_source = month_budg['income_source']
            source_budget_data = filter_by_income_source(
                income_source,
                budget_data=monthly_budget_data
                )
            for source_budg in source_budget_data:
                unique_incomes.add(source_budg['income'])
            if len(unique_incomes) > 1:
                    allow_submission = False
                    break
            unique_incomes.clear()

    start_index = budget_data.index(to_edit_data[0])
    stop_index = budget_data.index(to_edit_data[-1])

    if allow_submission == True:
        if st.button('Save'):
            save_budget('Edit', edit_start_i=start_index, edit_stop_i=stop_index)
            st.session_state.notification = 'Budget edited successfully!'
            st.rerun()
    else: st.warning('Incomes from same sources must be equal.')

@st.dialog('Delete a Budget')
def delete_budget_data():
    index = st.slider(
        'Select an Index to Delete',
        min_value=0,
        max_value=len(budget_data) - 1
    )

    month = st.text_input(
        'Month',
        value=budget_data[index]['month'],
        disabled=True
    )

    income_source = st.text_input(
        'Income Source',
        value=budget_data[index]['income_source'],
        disabled=True
    )

    income = st.number_input(
        'Income',
        value=budget_data[index]['income'],
        disabled=True
    )

    category = st.text_input(
        'Category',
        value=budget_data[index]['category'],
        disabled=True
    )

    planned_amount = st.number_input(
        'Planned Expense',
        value=budget_data[index]['planned_amount'],
        disabled=True
    )

    if st.button('Delete'):
        save_budget('Delete', delete_index=index)
        st.session_state.notification = 'Budget deleted successfully!'
        st.rerun()

def calc_income_per_source():
    budg_sources = [
        {
        'month':budg['month'],
        'income_source':budg['income_source'],
        'income':budg['income']
        }
        for budg in budget_data
        ]
    
    income_per_source = []
    for row in budg_sources:
        if row not in income_per_source:
            income_per_source.append(row)

    return income_per_source

def calc_planned_expenses_per_source():
    budg_sources = [
        {
        'month':budg['month'],
        'income_source':budg['income_source'],
        'planned_amount':budg['planned_amount']
        }
        for budg in budget_data
        ]
    
    planned_expenses_per_source = []
    for row in budg_sources:
        for i, planned_expense in enumerate(planned_expenses_per_source):
            if planned_expense['month'] == row['month'] and planned_expense['income_source'] == row['income_source']:
                planned_expenses_per_source[i]['planned_amount'] += row['planned_amount']
                break
        else: planned_expenses_per_source.append(row)
    
    return planned_expenses_per_source
    
def calc_unallocated_budget():
    income = calc_income_per_source()
    planned_expenses = calc_planned_expenses_per_source()
    
    unallocated_budgets = []
    for i, row in enumerate(income):
        unallocated = row['income'] - planned_expenses[i]['planned_amount']
        if unallocated <= 0: continue
        unallocated_per_source = {
            'month': row['month'],
            'income_source': row['income_source'],
            'unallocated': unallocated
        }
        unallocated_budgets.append(unallocated_per_source)
    
    st.session_state.unallocated_budgets = unallocated_budgets

def check_exceed_planned_expenses():
    income = calc_income_per_source()
    planned_expenses = calc_planned_expenses_per_source()

    exceeded_budgets = []
    for i, row in enumerate(income):
        exceeded = planned_expenses[i]['planned_amount'] - row['income']
        if exceeded <= 0: continue
        exceeded_per_source = {
            'month': row['month'],
            'income_source': row['income_source'],
            'exceeded': exceeded
        }
        exceeded_budgets.append(exceeded_per_source)

    if len(exceeded_budgets) > 0:
        st.session_state.exceeded_planned_expenses = exceeded_budgets
        st.session_state.there_exceeds = True
        st.warning('Your planned expenses exceed your income.')
    else:
        st.session_state.there_exceeds = False

st.subheader('Actions:')
customization_buttons()

check_exceed_planned_expenses()

st.subheader('Allocated Budget')
show_budget_data(budget_data)

if st.session_state.there_exceeds:
    st.subheader('Exceeded Planned Expenses')
    show_budget_data(st.session_state.exceeded_planned_expenses)

st.subheader('Unallocated Budget')
calc_unallocated_budget()
show_budget_data(st.session_state.unallocated_budgets)
