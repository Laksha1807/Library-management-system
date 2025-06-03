import sqlite3
import datetime

DB_NAME = 'library.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        year INTEGER,
                        copies INTEGER NOT NULL DEFAULT 1
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS Patrons (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS BorrowRecords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        book_id INTEGER NOT NULL,
                        patron_id INTEGER NOT NULL,
                        borrow_date TEXT NOT NULL,
                        return_date TEXT,
                        FOREIGN KEY(book_id) REFERENCES Books(id),
                        FOREIGN KEY(patron_id) REFERENCES Patrons(id)
                    )''')
        conn.commit()

def add_book():
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    year = input("Enter publication year (optional): ").strip()
    copies = input("Enter number of copies: ").strip()

    if not title or not author or not copies.isdigit():
        print("Invalid input. Title, author and copies (as number) are required.")
        return

    year_int = int(year) if year.isdigit() else None
    copies_int = int(copies)

    with connect_db() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO Books (title, author, year, copies) VALUES (?, ?, ?, ?)",
                  (title, author, year_int, copies_int))
        conn.commit()
        print(f"Book '{title}' added successfully.")

def list_books():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT id, title, author, year, copies FROM Books")
        books = c.fetchall()
        if books:
            print("\nBooks in Library:")
            print("-" * 60)
            for b in books:
                year_str = str(b[3]) if b[3] else "N/A"
                print(f"ID: {b[0]}, Title: {b[1]}, Author: {b[2]}, Year: {year_str}, Copies: {b[4]}")
        else:
            print("No books found.")

def search_books():
    keyword = input("Enter book title or author keyword to search: ").strip()
    if not keyword:
        print("Empty search keyword.")
        return
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT id, title, author, year, copies FROM Books WHERE title LIKE ? OR author LIKE ?",
                  (f'%{keyword}%', f'%{keyword}%'))
        books = c.fetchall()
        if books:
            print(f"\nSearch Results for '{keyword}':")
            print("-" * 60)
            for b in books:
                year_str = str(b[3]) if b[3] else "N/A"
                print(f"ID: {b[0]}, Title: {b[1]}, Author: {b[2]}, Year: {year_str}, Copies: {b[4]}")
        else:
            print("No matching books found.")

def update_book():
    list_books()
    book_id = input("Enter the ID of the book to update: ").strip()
    if not book_id.isdigit():
        print("Invalid book ID.")
        return
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Books WHERE id = ?", (book_id,))
        book = c.fetchone()
        if not book:
            print("Book ID not found.")
            return
        print("Enter new values (leave blank to keep current):")
        new_title = input(f"Title [{book[1]}]: ").strip()
        new_author = input(f"Author [{book[2]}]: ").strip()
        new_year = input(f"Year [{book[3]}]: ").strip()
        new_copies = input(f"Copies [{book[4]}]: ").strip()

        title = new_title if new_title else book[1]
        author = new_author if new_author else book[2]
        year = int(new_year) if new_year.isdigit() else book[3]
        copies = int(new_copies) if new_copies.isdigit() else book[4]

        c.execute("UPDATE Books SET title = ?, author = ?, year = ?, copies = ? WHERE id = ?",
                  (title, author, year, copies, book_id))
        conn.commit()
        print("Book updated successfully.")

def delete_book():
    list_books()
    book_id = input("Enter the ID of the book to delete: ").strip()
    if not book_id.isdigit():
        print("Invalid book ID.")
        return
    with connect_db() as conn:
        c = conn.cursor()
        # Check if book exists
        c.execute("SELECT title FROM Books WHERE id = ?", (book_id,))
        book = c.fetchone()
        if not book:
            print("Book ID not found.")
            return
        confirm = input(f"Confirm deletion of book '{book[0]}'? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Deletion cancelled.")
            return
        c.execute("DELETE FROM Books WHERE id = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully.")

def add_patron():
    name = input("Enter patron name: ").strip()
    email = input("Enter patron email: ").strip()
    if not name or not email:
        print("Name and email are required.")
        return
    with connect_db() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Patrons (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            print(f"Patron '{name}' added successfully.")
        except sqlite3.IntegrityError:
            print("Error: Email must be unique. Patron with this email already exists.")

def list_patrons():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, email FROM Patrons")
        patrons = c.fetchall()
        if patrons:
            print("\nPatrons:")
            print("-" * 60)
            for p in patrons:
                print(f"ID: {p[0]}, Name: {p[1]}, Email: {p[2]}")
        else:
            print("No patrons found.")

def search_patrons():
    keyword = input("Enter patron name or email keyword to search: ").strip()
    if not keyword:
        print("Empty search keyword.")
        return
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, email FROM Patrons WHERE name LIKE ? OR email LIKE ?",
                  (f'%{keyword}%', f'%{keyword}%'))
        patrons = c.fetchall()
        if patrons:
            print(f"\nSearch Results for '{keyword}':")
            print("-" * 60)
            for p in patrons:
                print(f"ID: {p[0]}, Name: {p[1]}, Email: {p[2]}")
        else:
            print("No matching patrons found.")

def update_patron():
    list_patrons()
    patron_id = input("Enter the ID of the patron to update: ").strip()
    if not patron_id.isdigit():
        print("Invalid patron ID.")
        return
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Patrons WHERE id = ?", (patron_id,))
        patron = c.fetchone()
        if not patron:
            print("Patron ID not found.")
            return
        print("Enter new values (leave blank to keep current):")
        new_name = input(f"Name [{patron[1]}]: ").strip()
        new_email = input(f"Email [{patron[2]}]: ").strip()

        name = new_name if new_name else patron[1]
        email = new_email if new_email else patron[2]

        try:
            c.execute("UPDATE Patrons SET name = ?, email = ? WHERE id = ?", (name, email, patron_id))
            conn.commit()
            print("Patron updated successfully.")
        except sqlite3.IntegrityError:
            print("Error: Email must be unique. This email already exists.")

def delete_patron():
    list_patrons()
    patron_id = input("Enter the ID of the patron to delete: ").strip()
    if not patron_id.isdigit():
        print("Invalid patron ID.")
        return
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM Patrons WHERE id = ?", (patron_id,))
        patron = c.fetchone()
        if not patron:
            print("Patron ID not found.")
            return
        confirm = input(f"Confirm deletion of patron '{patron[0]}'? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Deletion cancelled.")
            return
        c.execute("DELETE FROM Patrons WHERE id = ?", (patron_id,))
        conn.commit()
        print("Patron deleted successfully.")

def borrow_book():
    list_patrons()
    patron_id = input("Enter patron ID who is borrowing: ").strip()
    if not patron_id.isdigit():
        print("Invalid patron ID.")
        return
    list_books()
    book_id = input("Enter book ID to borrow: ").strip()
    if not book_id.isdigit():
        print("Invalid book ID.")
        return

    with connect_db() as conn:
        c = conn.cursor()
        # Check patron exists
        c.execute("SELECT name FROM Patrons WHERE id = ?", (patron_id,))
        patron = c.fetchone()
        if not patron:
            print("Patron not found.")
            return
        # Check book exists and availability
        c.execute("SELECT title, copies FROM Books WHERE id = ?", (book_id,))
        book = c.fetchone()
        if not book:
            print("Book not found.")
            return
        title, copies = book

        # Check currently borrowed copies of this book (not returned yet)
        c.execute("SELECT COUNT(*) FROM BorrowRecords WHERE book_id = ? AND return_date IS NULL", (book_id,))
        borrowed_count = c.fetchone()[0]

        if borrowed_count >= copies:
            print(f"Sorry, all copies of '{title}' are currently borrowed.")
            return

        # Insert borrow record
        borrow_date = datetime.datetime.now().isoformat()
        c.execute("INSERT INTO BorrowRecords (book_id, patron_id, borrow_date) VALUES (?, ?, ?)",
                  (book_id, patron_id, borrow_date))
        
        # Decrement the number of copies in the Books table
        c.execute("UPDATE Books SET copies = copies - 1 WHERE id = ?", (book_id,))
        
        conn.commit()
        print(f"Book '{title}' borrowed successfully by {patron[0]}.")

def return_book():
    list_patrons()
    patron_id = input("Enter patron ID who is returning: ").strip()
    if not patron_id.isdigit():
        print("Invalid patron ID.")
        return
    with connect_db() as conn:
        c = conn.cursor()
        # List borrowed books by this patron (not returned)
        c.execute('''
            SELECT br.id, b.id, b.title, br.borrow_date FROM BorrowRecords br
            JOIN Books b ON br.book_id = b.id
            WHERE br.patron_id = ? AND br.return_date IS NULL
        ''', (patron_id,))
        borrowed = c.fetchall()
        if not borrowed:
            print("No borrowed books found for this patron.")
            return
        print("\nBorrowed Books:")
        print("-" * 60)
        for br in borrowed:
            borrow_date = br[3][:19].replace("T", " ")
            print(f"Record ID: {br[0]}, Book ID: {br[1]}, Title: {br[2]}, Borrowed on: {borrow_date}")
        record_id = input("Enter the Record ID of the book to return: ").strip()
        if not record_id.isdigit() or int(record_id) not in [r[0] for r in borrowed]:
            print("Invalid Record ID.")
            return

        # Update return date
        return_date = datetime.datetime.now().isoformat()
        c.execute("UPDATE BorrowRecords SET return_date = ? WHERE id = ?", (return_date, record_id))

        # Increment the number of copies in Books table
        # Find the book_id for this borrow record
        book_id = None
        for r in borrowed:
            if r[0] == int(record_id):
                book_id = r[1]
                break
        
        if book_id:
            c.execute("UPDATE Books SET copies = copies + 1 WHERE id = ?", (book_id,))

        conn.commit()
        print("Book returned successfully.")

def view_borrowed_books():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT br.id, b.title, p.name, br.borrow_date, br.return_date FROM BorrowRecords br
            JOIN Books b ON br.book_id = b.id
            JOIN Patrons p ON br.patron_id = p.id
            ORDER BY br.return_date IS NOT NULL, br.borrow_date DESC
        ''')
        records = c.fetchall()
        if records:
            print("\nBorrow Records:")
            print("-" * 80)
            for r in records:
                borrow_date = r[3][:19].replace("T", " ")
                return_date = r[4][:19].replace("T", " ") if r[4] else "Not Returned"
                print(f"Record ID: {r[0]}, Book: {r[1]}, Patron: {r[2]}, Borrowed: {borrow_date}, Returned: {return_date}")
        else:
            print("No borrow records found.")

def main_menu():
    print("""
Library Management System
=========================
1. Add Book
2. List Books
3. Search Books
4. Update Book
5. Delete Book

6. Add Patron
7. List Patrons
8. Search Patrons
9. Update Patron
10. Delete Patron

11. Borrow Book
12. Return Book
13. View Borrow Records

0. Exit
""")

def main():
    init_db()
    while True:
        main_menu()
        choice = input("Select an option: ").strip()
        if choice == '1':
            add_book()
        elif choice == '2':
            list_books()
        elif choice == '3':
            search_books()
        elif choice == '4':
            update_book()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            add_patron()
        elif choice == '7':
            list_patrons()
        elif choice == '8':
            search_patrons()
        elif choice == '9':
            update_patron()
        elif choice == '10':
            delete_patron()
        elif choice == '11':
            borrow_book()
        elif choice == '12':
            return_book()
        elif choice == '13':
            view_borrowed_books()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()


