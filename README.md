**This is my capstone project that I made for CS50's Web Programming with Python and Javascript 2020 course**

# IBDb
IBDb is a collaborative library editing, you can create a page for a book and anyone can help improving the page, it was inspired by the collaborative editing form of wikipedia, where all users can edit a wiki and thus form quality content. The name was totally inspired by the IMDb (Internet Movie Database).

# Distinctiveness and Complexity

I believe that my project satisfies the distinctiveness and complexity requirements because it has several complex functions and models that were a challenge for me and it has more functions than Pizza Project, it's distinct from the other projects although it has some similarities on this projects, like posting, searching or editing.

Another point I want to mention is the frontend code, it was much more difficult, I did my best to make the site modern and responsive. So I think it all fits into a good final project.

# Project files

- `capstone`

	- `books` - Main application directory.

		- `__migrations` - All migrations of the project.

		- `static` - CSS, Images, Fonts and JS files.
			- `css` - All CSS files used in the project.
			- `images` - All images used in the project.
			- `js` - Contains all JS files used in the project, the main purpouse is executing functions without reloading the page.
				- `aprove.js` - Aprove any request_post in the website.
				- `book_status.js` - Add a book to read, reading or want to read in user profile.
				- `ibdb_rating.js` - Get all scores for the book requested.
				- `illustration.js` - Create/Edit/Delete book illustrations in /book/book_id/illustrations
				- `index.js` - Configuration file for SwipeJS slides.
				- `menu.js` - Used to create a responsive menu bar.
				- `rate.js` - Insert a user score on a book.
		- `templates/books` - HTML files used in the website.
			- `aprove.html` - A page to show all request editions on the website.
			- `book.html` - Show a page for a book on the website.
			- `book_reviews` - Show all reviews of a book.
			- `contribute.html` - A page that provides several inputs to create a book page.
			- `edit_book.html` and `edit_review.html` - As the name says, it provides for the user editing of books and reviews
			- `illustration.html` - Show all illustrations of a book.
			- `index.html` - Home page of the website
			- `layout.html` - Used as a layout for all HTML files, contains the navbar and some frontend setup files.
			- `login.html` - A login page for the user.
			- `profile` - Show some user info.
			- `register.html` - A registration page for the user.
			- `review.html` - Provide inputs for reviewing a book.
			- `search.html` - Shows all search results that compare to the user's search.
			- `show_request.html` - Shows an edit made by a user that is in analysis.
		- `admin.py` - Used to register all project models for django-admin.
		- `forms.py`  - Contains some forms used in templates to get data, like a new book page.
		- `models.py` - Contains all models used in the project.
		- `urls.py` - Contains all url paths for the project like new book or edit book.
		- `views.py` - Contains all view functions of the project.
	- `ibdb` - Project configuration folder
	- `manage.py` - Main file used, for example, starting the project.
	- `requirements.txt` - All dependencies used in the project.

## Frontend Frameworks used

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
