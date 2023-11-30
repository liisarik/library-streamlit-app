import streamlit as st
import pandas as pd
import psycopg2

# Connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname='testdb',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)

# Creating a cursor object
cursor = conn.cursor()

# Function to fetch data from PostgreSQL and display in Streamlit
def display_data(query):
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[column[0] for column in cursor.description])
    return df

# Streamlit app layout
def main():
    st.title('Library Management System')
    st.write("Using Streamlit app to manage a small fictional school library")
    st.write("Project by very smart students - Louise Malm and Liisa Rikanson")

    # Sidebar menu to select users:
    st.sidebar.selectbox(
        'Select the user:',
        ('Administrator', 'Librarian', 'Student')
    )

    # Sidebar menu to select options:
    option = st.sidebar.selectbox(
        'Select an option:',
        ('View Members', 'Manage Library Cards', 'Catalog of Books', 'Book Copies', 'Loans and Returns')
    )


    # Display data based on selected option
    if option == 'View Members':
        st.header('Library Members')
        members_df = display_data("SELECT * FROM \"DB_project_gr4\".\"libMember\"")
        st.dataframe(members_df)

        # Just testing stuff:
        st.write(pd.DataFrame({
            'first column': [1, 2, 3, 4],
            'second column': [10, 20, 30, 40]
        }))

        df = pd.DataFrame({
            'first column': [1, 2, 3, 4],
            'second column': [10, 20, 30, 40]
        })

        st.button('Save changes')

    elif option == 'Manage Library Cards':
        st.header('Library Cards')
        cards_df = display_data("SELECT * FROM \"DB_project_gr4\".\"libCard\"")
        st.dataframe(cards_df)

# ... need to add sections for other functionalities (Books, Copies, Loans, ...)


if __name__ == '__main__':
    main()

# Close the cursor and connection
cursor.close()
conn.close()
