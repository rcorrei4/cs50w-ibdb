from django import forms
from books.models import Book

CHOICES = [('1', '☆'),
		   ('2', '☆'),
		   ('3', '☆'),
		   ('4', '☆'),
		   ('5', '☆'),]

class ReviewForm(forms.Form):
	rating = forms.ChoiceField(choices=CHOICES)
	title = forms.CharField(max_length=175)
	text = forms.CharField(max_length=500)

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['title', 'author', 'book_cover', 'isbn', 'synopsis', 'genres', 
				  'published', 'original_title', 'characters','keywords']