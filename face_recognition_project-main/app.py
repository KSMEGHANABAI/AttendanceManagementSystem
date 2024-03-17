import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def read_attendance_data(selected_person, start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        try:
            formatted_date = current_date.strftime("%d-%m-%Y")
            df = pd.read_csv(f"C:\\Users\\91911\\OneDrive\\Desktop\\face_recognition_project-main\\face_recognition_project-main\\Attendance\\AttendanceDate.csv{formatted_date}.csv")

            if 'NAME' in df.columns:
                if selected_person:
                    df = df[df['NAME'].str.lower() == selected_person.lower()]  # Case-insensitive match

                st.header(f"Attendance for {formatted_date} ({selected_person if selected_person else 'All'}):")
                if not df.empty:
                    st.dataframe(df.style.highlight_max(axis=0))
                else:
                    st.warning(f"absent for this day")
            else:
                st.warning(f"Invalid format for {formatted_date}. Please check the structure of your CSV file.")
        except FileNotFoundError:
            st.warning(f"No attendance data found for {formatted_date}.")
        current_date += timedelta(days=1)

def main():
    st.title("Attendance Viewer")

    start_date = st.date_input("Select start date:", datetime.today() - timedelta(days=7))
    end_date = st.date_input("Select end date:", datetime.today())

    people_list = ["meghana", "sai", "manjula","usha","meenakshi"] 
    selected_person = st.selectbox("Select a person (optional):", [""] + people_list)

    if st.button("Show Attendance"):
        read_attendance_data(selected_person, start_date, end_date)

    if st.button("clear"):
        export_data(selected_person, start_date, end_date)

def export_data(selected_person, start_date, end_date):
    all_data = pd.DataFrame()

    current_date = start_date
    while current_date <= end_date:
        try:
            formatted_date = current_date.strftime("%d-%m-%Y")
            df = pd.read_csv(f"C:\\Users\\91911\\OneDrive\\Desktop\\face_recognition_project-main\\face_recognition_project-main\\Attendance\\AttendanceDate.csv{current_date}.csv")

            if 'NAME' in df.columns:
                if selected_person:
                    df = df[df['NAME'].str.lower() == selected_person.lower()]  # Case-insensitive match

                all_data = pd.concat([all_data, df], ignore_index=True)
            else:
                st.warning(f"Invalid format for {formatted_date}. Please check the structure of your CSV file.")
        except FileNotFoundError:
            pass
        current_date += timedelta(days=1)

    if not all_data.empty:
        all_data.to_csv(f"attendance_export_{start_date}_{end_date}.csv", index=False)
        st.success("Attendance data exported successfully.")

if __name__ == "__main__":
    main()
