from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date

class Book(models.Model):
	title = models.CharField(max_length=128)
	author = models.CharField(max_length=64)
	book_cover = models.ImageField(upload_to="books")
	isbn = models.JSONField(max_length=64, default=dict)
	synopsis = models.TextField(max_length=600)
	genres = models.JSONField(max_length=64, default=dict)
	published = models.DateField(default=date(2000, 2, 2))
	original_title = models.CharField(max_length=128)
	characters = models.JSONField(max_length=528, default=dict)
	keywords = models.JSONField(max_length=528, default=dict)

	def __str__(self):
		return str(self.title)

class Illustration(models.Model):
	image = models.ImageField()
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.book)

class Rating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	score = models.IntegerField(default=0, 
		validators = [
				MaxValueValidator(5),
				MinValueValidator(0)
			]
		)

	def __str__(self):
		return str(f"{self.user} - {self.book}: Rating {self.score}")

class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	title = models.CharField(max_length=175)
	text = models.CharField(max_length=500)
	date = models.DateField(auto_now=True)
	score = models.IntegerField(default=0, 
		validators = [
				MaxValueValidator(5),
				MinValueValidator(0)
			]
		)