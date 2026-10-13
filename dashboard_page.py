import matplotlib.pyplot as plt
import streamlit as st
import data_loader as dl
import pandas as pd
import datetime as dt

st.title('Dashboard')

budget_data = dl.load_budget_data()
expense_data = dl.load_expense_data()
PESO = '\u20B1'
COLUMNS = {
    'category': 'Category',
    'planned': 'Planned Amount',
    'actual': 'Actual Amount',
    'remaining': 'Money Remaining'
}

def select_month():
    months = list({budg['month'] for budg in budget_data})
    month = st.selectbox(
        'Select Month',
        months,
    )
    st.session_state.month = month

def filter_by_month():
    st.session_state.month_budget = [
        budg for budg in budget_data
        if budg['month'] == st.session_state.month
    ]
    st.session_state.month_expense = [
        exp for exp in expense_data
        if exp['month'] == st.session_state.month
    ]

def display_month_summary(budg_data, exp_data):
    incomes = {}
    for budg in budg_data:
        if budg['income_source'] not in incomes:
            incomes[budg['income_source']] = budg['income']
    total_income = sum(incomes.values())

    planned_expenses = [
        budg['planned_amount']
        for budg in budg_data
    ]
    total_planned_expenses = sum(planned_expenses)

    actual_expenses = [
        exp['amount']
        for exp in exp_data
    ]
    total_expenses = sum(actual_expenses)

    money_remaining = total_income - total_expenses

    month_summary = {
        'Total Income': f'= {PESO}{total_income}',
        'Total Planned Expenses': f'= {PESO}{total_planned_expenses}',
        'Total Expenses': f'= {PESO}{total_expenses}',
        'Money Remainig': f'= {PESO}{money_remaining}'
    }

    st.subheader('This Month\'s Summary', text_alignment='center')
    left, mid, right = st.columns([1,1,1])
    with mid:
        st.table(
            month_summary,
            width='content',
            border=False,
            hide_header=True
            )

    if money_remaining < 0:
        st.warning('Expenses exceeds income.')

def calc_budget_breakdown(budg_data, exp_data):
    planned = {}
    for budg in budg_data:
        if budg['category'] not in planned:
            planned[budg['category']] = budg['planned_amount']
        else:
            planned[budg['category']] += budg['planned_amount']

    actual = {}
    for exp in exp_data:
        if exp['category'] not in actual:
            actual[exp['category']] = exp['amount']
        else:
            actual[exp['category']] += exp['amount']
    
    planned_categories = planned.keys()
    actual_categories = actual.keys()
    
    budget_breakdown = []
    for category in planned_categories:
        category_breakdown = {}
        category_breakdown['category'] = category
        
        category_breakdown['planned'] = planned[category]
        if category in actual_categories:
            category_breakdown['actual'] = actual[category]
        else: category_breakdown['actual'] = 0
        
        difference = category_breakdown['planned'] - category_breakdown['actual']
        category_breakdown['remaining'] = difference
        
        budget_breakdown.append(category_breakdown)

    return budget_breakdown

def display_budget_breakdown(budg_data, exp_data):
    budg_breakdown = calc_budget_breakdown(budg_data, exp_data)
    
    df_budg_bd = pd.DataFrame(budg_breakdown)
    df_budg_bd = df_budg_bd.style.apply(highlight_row, axis=1)
    
    st.subheader('Budget Breakdown',text_alignment='center')
    st.dataframe(
        df_budg_bd,
        column_config={
            'category': 'Category',
            'planned': st.column_config.NumberColumn(
                'Planned Budget',
                format=f'{PESO}'+'%.1f',
            ),
            'actual': st.column_config.NumberColumn(
                'Actual Expense',
                format=f'{PESO}'+'%.1f',
            ),
            'remaining': st.column_config.NumberColumn(
                'Money Remaining',
                format=f'{PESO}'+'%.1f',
            )
        },
        hide_index=True
    )

    for budg in budg_breakdown:
        if budg['remaining'] < 0:
            st.warning(f'{budg['category']} expenses exceeds its planned budget.')

def highlight_row(row):
    if row['remaining'] < 0:
        return ['color: red'] * len(row)
    return [''] * len(row)

def budget_categ_pie(budg_data):
    st.subheader('Budget Distribution', text_alignment='center')
    
    categ_amounts = {}
    for budg in budg_data:
        if budg['category'] not in categ_amounts:
            categ_amounts[budg['category']] = budg['planned_amount']
        else:
            categ_amounts[budg['category']] += budg['planned_amount']
    
    amounts = categ_amounts.values()
    categories = categ_amounts.keys()
    
    fig1, ax1 = plt.subplots()
    
    fig1.patch.set_alpha(0.0)
    
    budg_pie = ax1.pie(
        amounts,
        labels=categories,
        textprops={'color': 'gray'}
        )
    ax1.pie_label(budg_pie, f'{PESO}'+"{absval:,.0f}")
    
    st.pyplot(fig1)

def planned_and_actual_expenses_chart(budg_data, exp_data):
    st.subheader('Planned vs. Actual Expenses', text_alignment='center')

    budg_breakdown = calc_budget_breakdown(budg_data, exp_data)

    categories = [budg['category'] for budg in budg_breakdown]
    planned_budg_data = [budg['planned'] for budg in budg_breakdown]
    actual_exp_data = [budg['actual'] for budg in budg_breakdown]

    fig2, ax2 = plt.subplots()
    fig2.patch.set_alpha(0.0)
    ax2.patch.set_alpha(0.0)

    ax2.set_ylabel(f'Amount (in {PESO})', fontsize=12, color='gray')

    ax2.grouped_bar(
        [planned_budg_data, actual_exp_data],
        tick_labels=categories,
        labels=['Planned', 'Actual'],
        colors=["#1f57fe", "#ff411b"]
    )

    ax2.tick_params(axis='x', labelsize=7)
    ax2.tick_params(axis='both', color='gray', labelcolor='gray')
    for spine in ax2.spines.values():
        spine.set_edgecolor('gray')

    ax2.legend()
    st.pyplot(fig2)

def visualize_expense_history(exp_data):
    st.subheader('Expense History', text_alignment='center')
    
    expenses_per_day = []
    for exp in exp_data:
        day = dt.date.strptime(exp['date'],'%Y-%m-%d').day
        amount = exp['amount']
        day_expense = {
            'Day': day,
            'Amount': amount
        }
        expenses_per_day.append(day_expense)
    
    st.line_chart(
        expenses_per_day,
        x='Day',
        y='Amount',
        x_label='Days of the Month',
        y_label=f'Amount of Expenses (in {PESO})',
        color='red'
        )

select_month()
filter_by_month()

display_month_summary(st.session_state.month_budget, st.session_state.month_expense)
st.divider()
display_budget_breakdown(st.session_state.month_budget, st.session_state.month_expense)
st.divider()
budget_categ_pie(st.session_state.month_budget)
st.divider()
planned_and_actual_expenses_chart(st.session_state.month_budget, st.session_state.month_expense)
st.divider()
visualize_expense_history(st.session_state.month_expense)
