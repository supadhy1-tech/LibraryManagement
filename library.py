import sqlite3
import datetime

# Connect to SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create Books Table
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                  book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  author TEXT NOT NULL,
                  year INTEGER,
                  copies INTEGER DEFAULT 1)''')

# Create Issued Books Table
cursor.execute('''CREATE TABLE IF NOT EXISTS issued_books (
                  issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  book_id INTEGER,
                  issued_to TEXT NOT NULL,
                  issue_date TEXT NOT NULL,
                  FOREIGN KEY (book_id) REFERENCES books (book_id))''')

conn.commit()


def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    year = input("Enter the publication year: ")
    copies = int(input("Enter number of copies: "))

    cursor.execute("INSERT INTO books (title, author, year, copies) VALUES (?, ?, ?, ?)",
                   (title, author, year, copies))
    conn.commit()
    print("Book added successfully!")


def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        print("ID | Title | Author | Year | Copies")
        for book in books:
            print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]}")
    else:
        print("No books available.")


def issue_book():
    book_id = int(input("Enter the book ID to issue: "))
    issued_to = input("Enter the name of the person: ")

    # Check if the book is available
    cursor.execute("SELECT copies FROM books WHERE book_id = ?", (book_id,))
    result = cursor.fetchone()
    if result and result[0] > 0:
        issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO issued_books (book_id, issued_to, issue_date) VALUES (?, ?, ?)",
                       (book_id, issued_to, issue_date))
        cursor.execute("UPDATE books SET copies = copies - 1 WHERE book_id = ?", (book_id,))
        conn.commit()
        print("Book issued successfully!")
    else:
        print("Sorry, no copies available.")


def delete_book():
    book_id = int(input("Enter the book ID to delete: "))

    cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully!")
    else:
        print("Book not found.")


def search_books():
    search_query = input("Enter book title or author to search: ")

    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                   ('%' + search_query + '%', '%' + search_query + '%'))
    results = cursor.fetchall()
    if results:
        print("ID | Title | Author | Year | Copies")
        for book in results:
            print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]}")
    else:
        print("No matching books found.")


def return_book():
    issue_id = int(input("Enter the issue ID to return the book: "))

    # Check if the issued book exists
    cursor.execute("SELECT book_id FROM issued_books WHERE issue_id = ?", (issue_id,))
    result = cursor.fetchone()
    if result:
        book_id = result[0]
        cursor.execute("DELETE FROM issued_books WHERE issue_id = ?", (issue_id,))
        cursor.execute("UPDATE books SET copies = copies + 1 WHERE book_id = ?", (book_id,))
        conn.commit()
        print("Book returned successfully!")
    else:
        print("Invalid issue ID.")


def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add New Book")
        print("2. View All Books")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Delete Book")
        print("6. Search Books")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            issue_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            search_books()
        elif choice == '7':
            print("Exiting the system. Goodbye!")
            conn.close()
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main_menu()
