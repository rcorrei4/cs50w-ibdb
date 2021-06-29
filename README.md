
# IBDb
This project was inspired by the collaborative editing form of wikipedia, where all users can edit a wiki and thus form quality content. The name was totally inspired by the IMDb (Internet Movie Database).

The idea is simple, all users can create or edit a book but it has a form of protection the administrator can use against page vandalism.

# Distinctiveness and Complexity

I believe that my project satisfies the distinctiveness and complexity requirements because it has more complex functions than Pizza Project and it's distinct from the other projects although it has some similarities on this projects, like posting, searching or editing. It has on total 22 view functions without counting authentication functions.

# Project files

On the books/views.py, the main file, it has 22 functions, without counting authentication functions, that make up the project:

- **index**: show for the user the last added books, latest added books, best rating books and latest reviews.
- **book**: show a page for the user containing all the book info requested. Logged users can rate this book, edit, review and add to bookshelf. The admin can block book editing for preventing page vandalism.
- **show_reviews**: as the name implies, it simply shows to user all the reviews of the requested book.
- **contribute**: send a form for the user to add a new book to the website.
- **edit_book**: send a form for the user to edit the book requested. When a user try to edit a book that is protected, that change is saved in another object and sent for admin to approve or disapprove.
- **get_book**: used for the frontend code so the page doesn't need to be reloaded when a book info is necessary.
- **search**: allow the user searching for a book stored in the database.
- **rate_book**: is simply for the user to rate a book.
- **illustration**: when a GET method is requested it shows a page containing all illustrations of a book for the user, the user can add or delete some illustrations and send a POST method to add or delete these illustrations.
- **review_book**: allow the user to write a review and rate a book.
- **edit_book**: for editing a review.
- **protect**: it blocks or unblock any modification from the user on a book.
- **aprove**: send for the admin all editions made by users when a book was protected. The admin can aprove or reprove these changes.
- **reprove**: delete a change on a book made by a user.
- **show_request**: shows the user a changes that have been submitted for analysis.
- **profile**: send a page containing basic user info, his bookshelf and all editions made by him sent for analysis.
- **book_status**: add or remove a book from bookshelf.
- **book_score**: its simply get a score from a book.

On books/forms.py, it has all forms for creating and editing a book or review and the protection form.
On books/models.py, all models needed for the website.
On fonts folder inside books/static it contains a font file used for the application.

The templates are inside books/templates/books/.

## Frameworks used

- Bootstrap
- SwiperJS

# Run

## Requirements
- Python3 or above

## Pip modules

You can install all pip modules with this command inside the folder:
~~~python3
python3 -m pip install -r requirements.txt or pip3 install -r requirements.txt
~~~

After installing requirements you can type this command to start the application:
~~~python3
python3 manage.py runserver
~~~