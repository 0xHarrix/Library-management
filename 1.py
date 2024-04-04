import tkinter as tk
from tkinter import messagebox
import sqlite3
from hashlib import sha256

# Create a SQLite database connection
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create tables for users, books, and permissions if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL UNIQUE,
                    author TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    date_acquired TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS permissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    permission_type TEXT NOT NULL,
                    FOREIGN KEY (book_id) REFERENCES books(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )''')

# Function to hash password
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Function to sign up a new user
def signup(username, email, password):
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
    conn.commit()
    messagebox.showinfo("Success", "User signed up successfully!")

# Function to handle signup button click
def signup_click():
    username = signup_username_entry.get()
    email = signup_email_entry.get()
    password = signup_password_entry.get()

    if username == "" or email == "" or password == "":
        messagebox.showerror("Error", "Please fill in all fields.")
    else:
        signup(username, email, password)

# Function to handle login button click
def login_click():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    if row:
        user_id, stored_password = row
        if stored_password == hash_password(password):
            messagebox.showinfo("Success", "Login successful!")
            open_library_page()
        else:
            messagebox.showerror("Error", "Incorrect password.")
    else:
        messagebox.showerror("Error", "Username not found.")

# Function to open the library page
def open_library_page():
    # Create a new Tkinter window for the library
    library_window = tk.Tk()
    library_window.title("Library")

    # Display books with permissions
    books_label = tk.Label(library_window, text="Books in the Library:")
    books_label.pack()

    # Sample books (you can replace these with your own data)
    sample_books = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "quantity": 5, "date_acquired": "2024-04-05"},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "quantity": 3, "date_acquired": "2024-04-07"},
        {"title": "1984", "author": "George Orwell", "quantity": 7, "date_acquired": "2024-04-10"},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "quantity": 4, "date_acquired": "2024-04-12"},
        {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "quantity": 2, "date_acquired": "2024-04-15"}
    ]

    for book in sample_books:
        title = book["title"]
        author = book["author"]
        quantity = book["quantity"]
        date_acquired = book["date_acquired"]

        book_frame = tk.Frame(library_window)
        book_frame.pack()

        title_label = tk.Label(book_frame, text=f"Title: {title}, Author: {author}, Quantity: {quantity}, Date Acquired: {date_acquired}")
        title_label.pack(side=tk.LEFT)

        borrow_button = tk.Button(book_frame, text="Borrow", command=lambda t=title: borrow_book(t))
        borrow_button.pack(side=tk.LEFT)

        return_button = tk.Button(book_frame, text="Return", command=lambda t=title: return_book(t))
        return_button.pack(side=tk.LEFT)

    # Input button for book and date acquired
    input_button = tk.Button(library_window, text="Input Book & Date Acquired", command=input_book_date)
    input_button.pack()

def input_book_date():
    input_window = tk.Toplevel()
    input_window.title("Input Book & Date Acquired")

    # Entry fields for book title and date acquired
    book_title_label = tk.Label(input_window, text="Book Title:")
    book_title_label.pack()
    book_title_entry = tk.Entry(input_window)
    book_title_entry.pack()

    author_label = tk.Label(input_window, text="Author:")
    author_label.pack()
    author_entry = tk.Entry(input_window)
    author_entry.pack()

    quantity_label = tk.Label(input_window, text="Quantity:")
    quantity_label.pack()
    quantity_entry = tk.Entry(input_window)
    quantity_entry.pack()

    date_label = tk.Label(input_window, text="Date Acquired:")
    date_label.pack()
    date_entry = tk.Entry(input_window)
    date_entry.pack()

    save_button = tk.Button(input_window, text="Save", command=lambda: save_book_info(book_title_entry.get(), author_entry.get(), quantity_entry.get(), date_entry.get()))
    save_button.pack()

def save_book_info(title, author, quantity, date):
    # Validate input
    if title == "" or author == "" or date == "" or int(quantity) <= 0:
        messagebox.showerror("Error", "Please fill in all fields with valid information.")
        return

    cursor.execute("INSERT INTO books (title, author, quantity, date_acquired) VALUES (?, ?, ?, ?)", (title, author, int(quantity), date))
    conn.commit()
    messagebox.showinfo("Success", "Book information saved.")

# Function to handle borrowing a book
def borrow_book(title):
    # Implement your borrowing logic here
    messagebox.showinfo("Borrow Book", f"Borrowed book: {title}")

# Function to handle returning a book
def return_book(title):
    # Implement your returning logic here
    messagebox.showinfo("Return Book", f"Returned book: {title}")

# Create Tkinter window for login and signup
root = tk.Tk()
root.title("Library Management System")

# Signup widgets...
signup_frame = tk.Frame(root)
signup_frame.pack()

signup_username_label = tk.Label(signup_frame, text="Username:")
signup_username_label.pack()
signup_username_entry = tk.Entry(signup_frame)
signup_username_entry.pack()

signup_email_label = tk.Label(signup_frame, text="Email:")
signup_email_label.pack()
signup_email_entry = tk.Entry(signup_frame)
signup_email_entry.pack()

signup_password_label = tk.Label(signup_frame, text="Password:")
signup_password_label.pack()
signup_password_entry = tk.Entry(signup_frame, show="*")
signup_password_entry.pack()

signup_button = tk.Button(signup_frame, text="Sign Up", command=signup_click)
signup_button.pack()

# Login widgets...
login_frame = tk.Frame(root)
login_frame.pack()

login_username_label = tk.Label(login_frame, text="Username:")
login_username_label.pack()
login_username_entry = tk.Entry(login_frame)
login_username_entry.pack()

login_password_label = tk.Label(login_frame, text="Password:")
login_password_label.pack()
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.pack()

login_button = tk.Button(login_frame, text="Login", command=login_click)
login_button.pack()

root.mainloop()

# Close database connection
conn.close()
