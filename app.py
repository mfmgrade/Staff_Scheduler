import streamlit as st
import pandas as pd
from scheduling_model import create_schedule

def app():
    # Pre-populate employees dictionary
    employees = st.session_state.get("employees", {
        "E1": (["Monday-Morning", "Tuesday-Afternoon"], 3),
        "E2": (["Wednesday-Morning"], 5),
        "E3": ([], 4),
        "E4": (["Friday-Afternoon", "Sunday-Morning"], 3),
        "E5": (["Saturday-Morning"], 4),
        "E6": (["Monday-Morning", "Tuesday-Afternoon"], 3),
        "E7": (["Wednesday-Morning"], 5),
        "E8": ([], 4),
        "E9": (["Friday-Afternoon", "Sunday-Morning"], 3),
        "E10": (["Saturday-Morning"], 4)
    })

    with st.form(key='employee_form'):
        st.header('Input Employee Constraints')
        employee_id = st.text_input('Employee ID')
        restrictions = st.multiselect('Shift Restrictions', options=['Monday-Morning', 'Monday-Afternoon', 'Tuesday-Morning', 'Tuesday-Afternoon', 'Wednesday-Morning', 'Wednesday-Afternoon', 'Thursday-Morning', 'Thursday-Afternoon', 'Friday-Morning', 'Friday-Afternoon', 'Saturday-Morning', 'Saturday-Afternoon', 'Sunday-Morning', 'Sunday-Afternoon'])
        max_shifts = st.number_input('Max Shifts Per Week', min_value=1, max_value=14)
        submit_button = st.form_submit_button(label='Add/Update Employee')

    if submit_button:
        employees[employee_id] = (restrictions, max_shifts)
        st.session_state.employees = employees  # Save updated employees data in session state

    if employees:
        schedule, shifts_per_employee = create_schedule(employees, min_employees_per_shift=2, max_employees_per_shift=4)

        # Convert shifts_per_employee into a DataFrame
        df_shifts_per_employee = pd.DataFrame.from_records([(employee, shifts) for employee, shifts in shifts_per_employee.items()], columns=['Employee', 'Shifts'])

        # Convert schedule into a DataFrame
        df_schedule = pd.DataFrame.from_dict(schedule, orient='index').transpose()

        # Display the shifts per employee dataframe
        st.header('Shifts per Employee')
        st.dataframe(df_shifts_per_employee)

        # Display the schedule dataframe
        st.header('Schedule')
        st.dataframe(df_schedule)

if __name__ == '__main__':
    app()
