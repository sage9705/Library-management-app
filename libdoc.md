# Library-management-app
#Library Database Documentation
This script creates and populates a SQLite database named 'library.db' that can be used to manage the books and borrowers of a library.

#Dependencies
The script requires the following dependencies:

Python 3.x
SQLite3 module
Functionality
The script creates and populates four tables in the 'library.db' database:
books: stores information about books such as title, author, category, status, borrower, and availability.
categories: stores information about the categories of books available in the library.
users: stores information about the users of the library.
borrowings: stores information about the books borrowed by the users of the library, such as the book id, user id, book title, borrower, borrowed date, and returned date.
The following functions are used to create and populate the tables:

create_tables(cur): creates the four tables in the database if they do not already exist.
insert_categories(cur): inserts predefined categories into the categories table.
insert_books(cur): inserts predefined books into the books table.
The predefined categories and books can be customized according to the library's requirements.

Usage
The 'library.db' database is used with the library management application 'library_management_app.py'. The library management application script 
connects to the database in executing its functionalities.

This program is for educational purposes only. 
