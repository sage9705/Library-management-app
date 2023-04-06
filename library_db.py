import sqlite3

#**************************Database to store Library Details****************************#
def create_tables(cur):
# Books table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'available',
            borrower TEXT,
            borrow_date TEXT,
            availability INTEGER DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )

    ''')

# Categories table

    cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

# Users table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

# Borrowings table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS borrowings (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            book_title TEXT NOT NULL,
            borrower TEXT NOT NULL,
            borrowed_date DATE NOT NULL,
            returned_date DATE,
            borrow_history INTEGER DEFAULT 0,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')


    print("Tables created successfully")


def insert_categories(cur):
    categories = [
        'Fiction', 'Non-fiction', 'Mystery', 'Biography',
        'Science Fiction', 'History', 'Thriller', 'Horror',
        'Classic Literature', 'Writing Style Guides',
        'Mystery and Crime Fiction', 'Science and Technology',
        'Biographies and Memoirs'
    ]
    for category in categories:
        cur.execute('INSERT INTO categories (name) VALUES (?)', (category,))

def insert_books(cur):
    books = [
        ('The Great Gatsby', 'F. Scott Fitzgerald', 1),
        ('To Kill a Mockingbird', 'Harper Lee', 1),
        ('The Elements of Style', 'William Strunk Jr. and E.B. White', 2),
        ('The Girl with the Dragon Tattoo', 'Stieg Larsson', 3),
        ('The Adventures of Sherlock Holmes', 'Arthur Conan Doyle', 4),
        ('Steve Jobs', 'Walter Isaacson', 5),
        ('1984', 'George Orwell', 3),
        ('Brave New World', 'Aldous Huxley', 3),
        ('A Brief History of Time', 'Stephen Hawking', 4),
        ('Murder on the Orient Express', 'Agatha Christie', 3),
        ('The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams', 4),
        ('The Da Vinci Code', 'Dan Brown', 1)
    ]
    for book in books:
        cur.execute('INSERT INTO books (title, author, category_id) VALUES (?, ?, ?)', book)

    
conn = sqlite3.connect('library.db') # Establish a connection to the database file named library.db
cur = conn.cursor()                  # Create a cursor object cur that can be used to execute SQL commands on the database.

# Function calls to the defined functions
create_tables(cur)
insert_categories(cur)
insert_books(cur)
 

conn.commit()
