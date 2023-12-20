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
    print(df)
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

        # Function to add a new student
        st.subheader('Add New Student')

        # Input fields for student details
        first_name = st.text_input('First Name')
        last_name = st.text_input('Last Name')
            # ... other fields

        if st.button('Add Student'):
        # Insert new student into the database
             #cursor.execute(
                # "INSERT INTO \"DB_project_gr4\".\"libMember\" (\"fName\", \"lName\", ...) VALUES (%s, %s, ...)",
                #(first_name, last_name, ...))
            #conn.commit()
            st.success('Student added successfully')

# ... need to add sections for other functionalities (Books, Copies, Loans, ...)


    # Function to activate/deactivate card status
    st.subheader('Activate/Deactivate Card Status')

    card_id = st.number_input('Enter Card ID')
    status = st.radio('Select Status', ('Activate', 'Deactivate'))

    if st.button('Update Status'):
        new_status = True if status == 'Activate' else False
        cursor.execute("UPDATE \"DB_project_gr4\".\"libCard\" SET \"status\" = %s WHERE \"cardID\" = %s", (new_status, card_id))
        conn.commit()
        st.success(f'Card {card_id} status updated successfully')

    elif option == 'Catalog of Books':
        st.header('Catalog of Books')
        books_df = display_data("SELECT * FROM \"DB_project_gr4\".\"book\"")
        st.dataframe(books_df)

        # Function to add a new book
        st.subheader('Add New Book')

        title = st.text_input('Title')
        author = st.text_input('Author')
        # ... other fields

        if st.button('Add Book'):
            cursor.execute("INSERT INTO \"DB_project_gr4\".\"book\" (\"title\", \"author\", ...) VALUES (%s, %s, ...)",
                           (title, author, ...))
            conn.commit()
            st.success('Book added successfully')


if __name__ == '__main__':
    main()

# Close the cursor and connection
cursor.close()
conn.close()
