import streamlit as st
import data_loader as dl

st.title('Budget Planner')

budget_data = dl.load_budget_data()

def show_budget_data():
    column_names = {
        'month':'Month',
        'income_source':'Income Source',
        'income':'Income',
        'category':'Category',
        'planned_amount':'Planned Amount'
    }
    st.dataframe(budget_data, column_config=column_names)

def add_budget_data():
    with st.form('Add Budget'):
        pass

def edit_budget_data():
    pass

def del_budget_data():
    pass

def add_edit_del_buttons():
    col1, col2, col3, col4 = st.columns([1,1,1,2])
    with col1:
        add_pressed = st.button('Add Budget', on_click=add_budget_data())
    with col2:
        edit_pressed = st.button('Edit a Budget', on_click=edit_budget_data())
    with col3:
        del_pressed = st.button('Delete a Budget', on_click=del_budget_data())

show_budget_data()
add_edit_del_buttons()