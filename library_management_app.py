import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import date
from datetime import datetime
import tkinter.simpledialog as simpledialog


# Connect to the database
conn = sqlite3.connect('library.db')
cur = conn.cursor()



# App Functionalities


def execute_sql_query(cur, query, params=None):
     if params:
        cur.execute(query, params)
     else:
        cur.execute(query)

     results = cur.fetchall()

     return results


#*********************************App's GUI with Tkinter*********************************#
class LibraryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Management App")
        self.create_widgets()
        self.connection = sqlite3.connect('library.db')
        self.cur = self.connection.cursor()


        

    def create_widgets(self):
        # Create labels and entry widgets for search bar
        tk.Label(self.master, text="Search:").grid(row=0, column=0)
        self.search_entry = tk.Entry(self.master)
        self.search_entry.grid(row=0, column=1)
        self.listbox = tk.Listbox(self.master) # define the listbox widget
        tk.Button(self.master, text="Search", command=self.search_books).grid(row=0, column=2)

        # Create listbox for displaying books
        self.books_listbox = tk.Listbox(self.master, height=30, width=90)
        self.books_listbox.grid(row=1, column=0, columnspan=5)

        # Create buttons for adding, borrowing, returning and deleting books
        tk.Button(self.master, text="Add", command=self.add_book).grid(row=2, column=0)
        tk.Button(self.master, text="Return", command=self.return_book).grid(row=2, column=1)
        tk.Button(self.master, text="Borrow", command=self.borrow_book).grid(row=2, column=2)
        tk.Button(self.master, text="Delete", command=self.delete_book).grid(row=2, column=3)
        


    def add_book(self):
        title = simpledialog.askstring("Title", "Enter book title")
        if not title:
            return  # do nothing if title is empty or None
        
        author = simpledialog.askstring("Author", "Enter book author")
        if not author:
            return  # do nothing if author is empty or None
        
        category_id = simpledialog.askstring("Category", "Enter book category ID")
        try:
            category_id = int(category_id)
        except ValueError:
            tk.messagebox.showerror("Error", "Category ID must be an integer.")
            return

        # Insert the new book into the database
        try:
            self.cur.execute('INSERT INTO books (title, author, category_id) VALUES (?, ?, ?)', (title, author, category_id))
            self.connection.commit()
        except sqlite3.IntegrityError:
            tk.messagebox.showerror("Error", "Category ID does not exist.")
            return

        # Update the Listbox with the new book
        self.update_books_listbox()



    def delete_book(self):
        # Get the selected book from the listbox
        selection = self.books_listbox.curselection()
        if not selection:
            tk.messagebox.showinfo("Info", "Please select a book to delete.")
            return
        selected_book = self.books_listbox.get(selection)

        # Ask for user confirmation before deleting the book
        confirm = tk.messagebox.askyesno("Confirm", f"Are you sure you want to delete {selected_book}?")
        if not confirm:
            return

        try:
            # Delete the book from the database
            book_id = selected_book.split(" - ")[0]
            self.cur.execute('DELETE FROM books WHERE id=?', (book_id,))
            self.connection.commit()

            # Update the listbox with the updated book list
            self.cur.execute("SELECT * FROM books")
            books = self.cur.fetchall()
            self.books_listbox.delete(0, tk.END)
            for book in books:
                self.books_listbox.insert(tk.END, f"{book[0]} - {book[1]} by {book[2]} (Category ID: {book[3]})")

            tk.messagebox.showinfo("Success", f"{selected_book} has been successfully deleted.")

        except Exception as e:
            # If an error occurs during the database operation, show an error message
            tk.messagebox.showerror("Error", f"An error occurred while deleting the book: {e}")



    def search_books(self):
        # Retrieve search query from entry widget
        query = self.search_entry.get()

        if not query: # Check if query is empty
            self.books_listbox.delete(0, tk.END) # Clear books_listbox
            return

        try:
            # Prepare SQL query with placeholders for user input
            sql = '''
                SELECT books.id, books.title, books.author, categories.name
                FROM books
                JOIN categories ON books.category_id = categories.id
                WHERE books.title LIKE ? OR books.author LIKE ? OR categories.name LIKE ?
            '''

            # Execute SQL query with user input as parameters
            self.cur.execute(sql, ('%{}%'.format(query), '%{}%'.format(query), '%{}%'.format(query)))
            books = self.cur.fetchall()

            # Update books_listbox with results
            self.books_listbox.delete(0, tk.END)

            if len(books) == 0:
                tk.messagebox.showinfo("Info", "No books found")
            else:
                for book in books:
                    self.books_listbox.insert(tk.END, " {}, Author: {}, Category: {}".format(book[1], book[2], book[3]))

        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", "An error occurred while searching for books:\n{} Run the library database to access it".format(e))




    def borrow_book(self):
         # Get the selected book from the listbox
         selection = self.books_listbox.curselection()
         if not selection:
             messagebox.showwarning("Warning", "Please select a book to borrow.")
             return
         selected_book = self.books_listbox.get(selection)

         # Check if the book is available to be borrowed
         book_id = selected_book.split(" - ")[0]
         self.cur.execute('SELECT * FROM books WHERE id=?', (book_id,))
         book = self.cur.fetchone()

         if book is not None and book[4] != 'available':
             messagebox.showinfo("Info", f"{selected_book} is not available to be borrowed.")
             return

         # Get the user who is borrowing the book
         user_name = simpledialog.askstring("Name", "Enter your name")
         if user_name is None or not user_name.strip():
             return

         # Update the book status and borrow history in the database
         self.cur.execute('UPDATE books SET status=?, borrower=?, borrow_date=? WHERE id=?',
                          ('borrowed', user_name, datetime.now(), book_id))
         self.connection.commit()

         # Update the listbox with the new book status
         self.books_listbox.delete(selection)
         if book is not None:
             new_selection = f"{book[1]} - {book[2]} by {book[3]} (Category ID: {book[5]}, Status: borrowed)"
             self.books_listbox.insert(selection, new_selection)

             # Display success message
             messagebox.showinfo("Success", f"{user_name}, you have successfully borrowed {new_selection}.")
         else:
             new_selection = f"{selected_book} (Status: borrowed)"
             self.books_listbox.insert(selection, new_selection)

             # Display success message
             messagebox.showinfo("Success", f"{user_name}, you have successfully borrowed {new_selection}.")





    def return_book(self):
        # Get the selected book from the listbox
        selection = self.books_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to return.")
            return
        selected_book = self.books_listbox.get(selection)

        # Check if the book has been borrowed
        book_id = selected_book.split(" - ")[0]
        self.cur.execute('SELECT * FROM books WHERE id=?', (book_id,))
        book = self.cur.fetchone()

        if book is None:
            messagebox.showinfo("Info", f"{selected_book} is not in the database.")
            return

        if book[4] == 'available':
            messagebox.showinfo("Info", f"{selected_book} has not been borrowed.")
            return

        # Get the user who is returning the book
        user_name = simpledialog.askstring("Name", "Enter your name")
        if not user_name.strip():
            return

        # Check if the user has borrowed the book
        self.cur.execute('SELECT * FROM borrow_history WHERE book_id=? AND borrower=?', (book_id, user_name))
        borrow_history = self.cur.fetchone()

        if borrow_history is None:
            messagebox.showinfo("Info", f"{user_name}, you can't return {selected_book} as you didn't borrow it.")
            return

        # Update the book status and borrow history in the database
        self.cur.execute('UPDATE books SET status=?, borrower=?, borrow_date=? WHERE id=?',
                         ('available', None, None, book_id))
        self.cur.execute('DELETE FROM borrow_history WHERE book_id=? AND borrower=?', (book_id, user_name))
        self.connection.commit()

        # Update the listbox with the new book status
        self.books_listbox.delete(selection)
        new_selection = f"{book[1]} - {book[2]} by {book[3]} (Category ID: {book[5]}, Status: available)"
        self.books_listbox.insert(selection, new_selection)

        # Display success message
        messagebox.showinfo("Success", f"{user_name}, you have successfully returned {selected_book}.")


    def update_books_listbox(self):
        # Fetch all books from the database
        self.cur.execute("SELECT * FROM books")
        books = self.cur.fetchall()

        # Update the Listbox with the new book
        self.books_listbox.delete(0, tk.END)
        for book in books:
            self.books_listbox.insert(tk.END, f"{book[0]} - {book[1]} by {book[2]} (Category ID: {book[3]})")


    def __del__(self):
    # Close database connection on app exit
        self.connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()



