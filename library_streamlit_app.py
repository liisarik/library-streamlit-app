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
    st.write("Using Streamlit app to manage a fictional University library")
    st.write("Project by Louise Malm and Liisa Rikanson")

    # Sidebar menu to select users:
    selected_user = st.sidebar.selectbox(
        'Select the user:',
        ('Administrator', 'Librarian', 'Student')
    )

    # Display options based on selected user
    if selected_user == 'Administrator':
        option = st.sidebar.selectbox(
            'Select an option:',
            ('View Members', 'Manage Library Cards', 'Catalog of Books', 'Book Copies', 'Loans and Returns')
        )
    elif selected_user == 'Librarian':
        option = st.sidebar.selectbox(
            'Select an option:',
            ('View Members', 'Manage Library Cards', 'Book Copies', 'Loans and Returns')
        )
    elif selected_user == 'Student':
        option = st.sidebar.selectbox(
            'Select an option:',
            ('Book Copies', 'View My Loans', 'Change password')
        )

    # Display data based on selected user
    # If selected user is administrator:
    if selected_user == 'Administrator':

        if option == 'View Members':
            st.header('Library Members')
            members_df = display_data("SELECT * FROM \"DB_project_gr4\".\"libMember\"")
            st.dataframe(members_df)

        elif option == 'Manage Library Cards':
            st.header('Library Cards')
            cards_df = display_data("SELECT * FROM \"DB_project_gr4\".\"libCard\"")
            st.dataframe(cards_df)

            # Function to activate/deactivate card status
            st.subheader('Activate/Deactivate Card Status')

            card_id = st.number_input('Enter Card ID', step=1, value=0, format='%d')
            status = st.radio('Select Status', ('Activate', 'Deactivate'))

            if st.button('Update Status'):
                new_status = True if status == 'Activate' else False
                cursor.execute("UPDATE \"DB_project_gr4\".\"libCard\" SET \"status\" = %s WHERE \"cardID\" = %s",
                               (new_status, card_id))
                conn.commit()
                st.success(f'Card {card_id} status updated successfully')

            # Function to add a new student
            st.subheader('Add New Member')

            # Input fields for student details
            first_name = st.text_input('First Name')
            last_name = st.text_input('Last Name')
            address = st.text_input('Address')
            email = st.text_input('Email')
            phone = st.text_input('Phone')
            is_student = st.checkbox('Is Student')

            if st.button('Add Member'):
                # Insert new student into the database
                cursor.execute(
                    "INSERT INTO \"DB_project_gr4\".\"libMember\" (\"fName\", \"lName\", \"address\", \"email\", \"phone\", \"isStudent\", \"loanedItems\") "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, address, email, phone, is_student, 0)
                )
                conn.commit()
                st.success('Member added successfully')


        elif option == 'Catalog of Books':
            st.header('Catalog of Books')
            books_df = display_data("SELECT * FROM \"DB_project_gr4\".\"book\"")
            st.dataframe(books_df)

            # Function to add a new book
            st.subheader('Add New Book')

            ISBN = st.text_input('ISBN')
            title = st.text_input('Title')
            language = st.text_input('Language')
            num_pages = st.number_input('Number of Pages', min_value=1, step=1)
            pub_year = st.number_input('Publication Year', min_value=0, step=1)
            publisher = st.text_input('Publisher')
            num_copies = st.number_input('Number of Copies', min_value=1, step=1)

            if st.button('Add Book'):
                cursor.execute(
                    "INSERT INTO \"DB_project_gr4\".\"book\" (\"ISBN\", \"title\", \"language\", \"numPage\", \"pubYear\", \"publisher\", \"numCopies\") "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (ISBN, title, language, num_pages, pub_year, publisher, num_copies)
                )
                conn.commit()
                st.success('Book added successfully')

        elif option == 'Book Copies':
            st.header('Book Copies')
            book_copy_df = display_data("SELECT * FROM \"DB_project_gr4\".\"bookCopy\"")
            st.dataframe(book_copy_df)

        elif option == 'Loans and Returns':
            st.header('Loans and Returns')
            bookLoans_df = display_data("SELECT * FROM \"DB_project_gr4\".\"bookLoan\"")
            st.dataframe(bookLoans_df)

    # If selected user is librarian:
    elif selected_user == 'Librarian':

        if option == 'View Members':
            st.header('Library Members')
            members_df = display_data("SELECT * FROM \"DB_project_gr4\".\"libMember\"")
            st.dataframe(members_df)

        elif option == 'Book Copies':
            st.header('Book Copies')
            book_copy_df = display_data("SELECT * FROM \"DB_project_gr4\".\"bookCopy\"")
            st.dataframe(book_copy_df)

        elif option == 'Loans and Returns':
            st.header('Loans and Returns')
            bookLoans_df = display_data("SELECT * FROM \"DB_project_gr4\".\"bookLoan\"")
            st.dataframe(bookLoans_df)

        # Function to update book return status
        st.subheader('Update Book Return Status')

        loan_id = st.number_input('Enter Loan ID', step=1, value=0, format='%d')
        return_status = st.radio('Select Return Status', ('Returned', 'Not Returned'))

        if st.button('Update Return Status'):
            returned = True if return_status == 'Returned' else False
            cursor.execute("UPDATE \"DB_project_gr4\".\"bookLoan\" SET \"returned\" = %s WHERE \"loanID\" = %s",
                           (returned, loan_id))
            conn.commit()
            st.success(f'Book with Loan ID {loan_id} return status updated successfully')

    # If selected user is student:
    elif selected_user == 'Student':

        if option == 'Book Copies':
            st.header('Book Copies')
            book_copy_df = display_data("SELECT * FROM \"DB_project_gr4\".\"bookCopy\"")
            st.dataframe(book_copy_df)


if __name__ == '__main__':
    main()

# Close the cursor and connection
cursor.close()
conn.close()
