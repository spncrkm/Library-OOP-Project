from book import Book
from user import User
from author import Author
from genre import Genre
from datetime import datetime, timedelta



class Library:

    def __init__(self):
        self.users = {} # Dictionary to store users with library_id as keys
        self.books = {}  # Dictionary to store books by ISBN as keys
        self.authors = {}  
        self.genres = {}
        self.overdue_books = []


    def add_user(self, name, dob, email):
        new_user = User(name, dob, email)  # User object and generate a library ID
        library_id = new_user.generate_lib_id()  # Generate library ID for the new user
        self.users[library_id] = new_user  # Add user to the library dictionary
        return new_user.library_id  # Return the generated library ID to the new user
        
    
    def check_out_book(self, library_id, isbn):
        user = self.users.get(library_id)
        if not user:
            print("User not found.")
        
        book = self.books.get(isbn)
        if not book:
            print("Book not found.")
        
        if book.check_out():
            user.borrow_book(book, datetime.now())
            print("Book checked out successfully.")
        else:
            print("Book is not available.")

        
    def return_book(self, library_id, isbn):
        user = self.users.get(library_id) # get the user object based on library ID
        if not user:
            print("User not found.")
            return
        for borrowed_book in user.borrowed_books:
            if borrowed_book["book"].get_isbn() == isbn:
                user.borrowed_books.remove(borrowed_book)
                borrowed_book["book"].return_book()
                print("Book returned successfully.")
                return
        print("Book not found in user's borrowed list.")


    def check_overdue_books(self):
        current_date = datetime.now()
        for user_id, user in self.users.items():
            for borrowed_book in user.borrowed_books:
                date_borrowed = borrowed_book["date_borrowed"]
                due_date = date_borrowed + timedelta(days=30)

                if current_date > due_date:
                    self.overdue_books.append({"user_id": user_id, "book": borrowed_book["book"], "due_date": due_date})
            print(due_date)
        return self.overdue_books
    

    def add_book(self, title, author_name, isbn, category=None):
        # Find or create the author
        if author_name in self.authors:
            author = self.authors[author_name]
        else:
            biography = input(f"Enter biography for author {author_name}: ")
            author = Author(author_name, biography)
            self.authors[author_name] = author
        # Create and add the book
        book = Book(title, author_name, isbn, category)
        self.books[isbn] = book
        author.add_book(book)

    def get_books_by_author(self, author_name):
        if author_name in self.authors:
            author = self.authors[author_name]
            return author.get_books()
        else:
            return []
        
    def add_genre(self, name, description, category=None):
        if name in self.genres:
            print(f"Genre {name} already exists.")
            return
        genre = Genre(name, description, category)
        self.genres[name] = genre
        print(f"Genre {name} added successfully.")
        

    def get_genre_details(self, name):
        if name in self.genres:
            genre = self.genres[name]
            return genre.get_details()
        else:
            print(f"Genre {name} not found.")
            return None 
        
    def display_all_genres(self):
        for genre in self.genres.values():
            print(f"Name: {genre.get_name()}, Description: {genre.get_description()}, Category: {genre.get_category()}")
