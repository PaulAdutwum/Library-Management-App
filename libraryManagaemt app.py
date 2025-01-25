from datetime import datetime, timedelta
import getpass  

books = {}
borrowed_books = {}
users = {"admin": "password123"}  

def authenticate_user():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    return users.get(username) == password

def calculate_due_date():
    return datetime.now() + timedelta(days=14)

def calculate_overdue_fee(return_date, due_date):
    days_overdue = (return_date - due_date).days
    return max(0, days_overdue * 1.5)  


def add_book():
    if not authenticate_user():
        print("Authentication failed! Access denied.")
        return

    book_title = input("Enter book title: ")
    book_author = input("Enter book author: ")
    publication_year = input("Enter publication year: ")
    genre = input("Enter book genre (e.g., Fiction, Non-Fiction): ")
    copies_to_add = int(input("Enter the number of copies to add: "))

    if book_title in books:
        books[book_title]["copies"] += copies_to_add
        print(f"{copies_to_add} copies added successfully for '{book_title}'. Total copies: {books[book_title]['copies']}")
    else:
        book = {
            "author": book_author,
            "publication_year": publication_year,
            "genre": genre,
            "copies": copies_to_add
        }
        books[book_title] = book
        print(f"Book '{book_title}' added successfully!")


def remove_book():
    if not authenticate_user():
        print("Authentication failed! Access denied.")
        return

    title = input("Enter title of the book to remove: ")
    if title in books:
        if books[title]["copies"] > 1:
            books[title]["copies"] -= 1
            print(f"One copy of book '{title}' removed successfully!")
        else:
            del books[title]
            print(f"Book '{title}' removed successfully!")
    else:
        print("Book not found.")


def search_book():
    search_info = input("Enter title, author, or genre to search: ").lower()
    found_books = []
    for title, book in books.items():
        if (search_info == title.lower() or 
            search_info == book["author"].lower() or 
            search_info == book["genre"].lower()):
            found_books.append((title, book))

    if found_books:
        print("Found Books:")
        for title, book in found_books:
            print(f"Title: {title}, Author: {book['author']}, Year: {book['publication_year']}, Genre: {book['genre']}, Copies: {book['copies']}")
    else:
        print("No books found.")


def display_books():
    if books:
        print("All Books:")
        for idx, (title, book) in enumerate(sorted(books.items()), 1):
            print(f"{idx}. Title: {title}, Author: {book['author']}, Year: {book['publication_year']}, Genre: {book['genre']}, Copies: {book['copies']}")
    else:
        print("No books available.")


def borrow_book():
    title = input("Enter title of the book to borrow: ")
    if title in books and books[title]["copies"] > 0:
        due_date = calculate_due_date()
        books[title]["copies"] -= 1
        borrowed_books[title] = {
            "due_date": due_date,
            "borrow_date": datetime.now()
        }
        print(f"Book '{title}' borrowed successfully! Due date: {due_date.strftime('%Y-%m-%d')}")
    else:
        print("Book not available or not found.")


def return_book():
    title = input("Enter title of the book to return: ")
    if title in borrowed_books:
        due_date = borrowed_books[title]["due_date"]
        return_date = datetime.now()
        overdue_fee = calculate_overdue_fee(return_date, due_date)
        
        if overdue_fee > 0:
            print(f"Book returned late. Overdue fee: ${overdue_fee:.2f}")
        else:
            print("Book returned on time. No overdue fee.")
        
        books[title]["copies"] += 1
        del borrowed_books[title]
    else:
        print("Book not found in borrowed records.")


def library_analytics():
    print("Library Analytics:")
    print(f"Total books in library: {len(books)}")
    print(f"Total borrowed books: {len(borrowed_books)}")
   


while True:
    print("\nWELCOME TO PAUL'S LIBRARY SERVICES, CHOOSE FROM THE MENU BELOW:")
    print("=================================================================")
    print("1. Add a new book")
    print("2. Remove a book")
    print("3. Search for a book by title/author/genre")
    print("4. Display all books")
    print("5. Borrow a book")
    print("6. Return a book")
    print("7. View library analytics")
    print("8. Exit the program")
    choice = input("Enter your choice (1-8): ")

    if choice == "1":
        add_book()
    elif choice == "2":
        remove_book()
    elif choice == "3":
        search_book()
    elif choice == "4":
        display_books()
    elif choice == "5":
        borrow_book()
    elif choice == "6":
        return_book()
    elif choice == "7":
        library_analytics()
    elif choice == "8":
        print("Exiting program! Thank you for using our Library Service. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 8.")
