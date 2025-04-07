import datetime
import json

class Book:
    def __init__(self, author, title, pubyear, isbn):
        self.author = author
        self.title = title
        self.pubyear = pubyear
        self.isbn = isbn
        self.borrowed_by = None
        self.borrowed_date = None

    def get_userinput(self):
        self.title = input("ENTER THE TITLE OF THE BOOK: ")
        self.author = input("ENTER THE AUTHOR NAME: ")
        while True:
            try:
                isbn = input("ENTER YOUR ISBN NUMBER (13 digits max): ")
                if len(isbn) <= 13:
                    self.isbn = isbn
                    break
                else:
                    print("ISBN NUMBER SHOULD BE WITHIN 13 DIGITS")
            except ValueError:
                print("ENTER A VALID ISBN NUMBER!!")
        
        while True:
            try:
                pubyear = int(input("ENTER THE PUBLISHED YEAR OF THE BOOK: "))
                if 1800 <= pubyear <= datetime.datetime.now().year:
                    self.pubyear = pubyear
                    break
                else:
                    print("YEAR SHOULD BE WITHIN LIMITS (1800 to current year)")
            except ValueError:
                print("ENTER A VALID YEAR!!")

    def insert_book(self):
        return {
            "title": self.title,
            "author": self.author,
            "pubyear": self.pubyear,
            "isbn": self.isbn,
            "borrowed_by": self.borrowed_by,
            "borrowed_date": self.borrowed_date
        }

class Library:
    def __init__(self):
        self.books = []
        try:
            with open("library_data.json", 'r') as file:
                self.books = json.load(file)
                print("File loaded successfully")
        except FileNotFoundError:
            print("library_data.json file is not found.")

    def add_book(self):
        n = int(input("Enter the number of books you want to add: "))
        for _ in range(n):
            b = Book("", "", 0, 0)
            b.get_userinput()
            self.books.append(b.insert_book())
        print("BOOK INSERTED SUCCESSFULLY")
        self.save_data()

    def search_book(self):
        search_term = input("Enter title, author, or ISBN to search: ")
        results = [book for book in self.books if search_term.lower() in book['title'].lower() or search_term.lower() in book['author'].lower() or search_term.lower() in book['isbn'].lower()]
        if results:
            for idx, book in enumerate(results, start=1):
                print(f"Search Result {idx}:")
                print(f"  Title: {book['title']}")
                print(f"  Author: {book['author']}")
                print(f"  Published Year: {book['pubyear']}")
                print(f"  ISBN: {book['isbn']}")
                print(f"  Status: {'Borrowed' if book['borrowed_by'] else 'Available'}")
                if book['borrowed_by']:
                    print(f"  Borrowed By: {book['borrowed_by']}")
                    print(f"  Borrowed Date: {book['borrowed_date']}")
                print("-" * 30)
        else:
            print("No matching books found.")

    def borrow_book(self):
        isbn = input("Enter the ISBN of the book to borrow: ")
        for book in self.books:
            if book['isbn'] == isbn:
                if book['borrowed_by']:
                    print("This book is already borrowed.")
                else:
                    borrower = input("Enter your name: ")
                    book['borrowed_by'] = borrower
                    book['borrowed_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"Book '{book['title']}' borrowed successfully by {borrower}.")
                self.save_data()
                return
        print("Book not found.")

    def return_book(self):
        isbn = input("Enter the ISBN of the book to return: ")
        for book in self.books:
            if book['isbn'] == isbn:
                if book['borrowed_by']:
                    print(f"Book '{book['title']}' returned successfully.")
                    book['borrowed_by'] = None
                    book['borrowed_date'] = None
                else:
                    print("This book was not borrowed.")
                self.save_data()
                return
        print("Book not found.")

    def view_books(self):
        if not self.books:
            print("No books available in the library.")
        else:
            for idx, book in enumerate(self.books, start=1):
                print(f"Book {idx}:")
                print(f"  Title: {book['title']}")
                print(f"  Author: {book['author']}")
                print(f"  Published Year: {book['pubyear']}")
                print(f"  ISBN: {book['isbn']}")
                print(f"  Status: {'Borrowed' if book['borrowed_by'] else 'Available'}")
                if book['borrowed_by']:
                    print(f"  Borrowed By: {book['borrowed_by']}")
                    print(f"  Borrowed Date: {book['borrowed_date']}")
                print("-" * 30)

    def save_data(self):
        with open("library_data.json", 'w') as file:
            json.dump(self.books, file, indent=4)
            print("File content saved successfully")

    def menu(self):
        while True:
            print("________LIBRARY MANAGEMENT SYSTEM_________")
            print("1. Add book")
            print("2. Search book")
            print("3. Borrow book")
            print("4. Return book")
            print("5. View books")
            print("6. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                self.add_book()
            elif choice == 2:
                self.search_book()
            elif choice == 3:
                self.borrow_book()
            elif choice == 4:
                self.return_book()
            elif choice == 5:
                self.view_books()
            elif choice == 6:
                break
            else:
                print("Invalid choice. Please try again.")
library = Library()
library.menu()
