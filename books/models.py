from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date

class User(AbstractUser):
	contributions = models.IntegerField(default=0)

class AbstractBook(models.Model):
	title = models.CharField(max_length=128, default="")
	author = models.CharField(max_length=64, default="")
	isbn = models.JSONField(max_length=64, default=dict)
	synopsis = models.TextField(max_length=600, default="")
	genres = models.JSONField(max_length=64, default=dict)
	published = models.DateField(default=date(2000, 2, 2))
	original_title = models.CharField(max_length=128, default="")
	characters = models.JSONField(max_length=528, default=dict)
	keywords = models.JSONField(max_length=528, default=dict)

	class Meta:
		abstract = True

class Book(AbstractBook):
	book_cover = models.ImageField(upload_to="books")
	protection = models.BooleanField(max_length=128, default=False)

	def __str__(self):
		return str(self.title)

class BookRequest(AbstractBook):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField(auto_now=True)
	change = models.CharField(max_length=24)

	def __str__(self):
		return str(self.title +" - "+ self.change)

class Illustration(models.Model):
	image = models.ImageField()
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.book)

class IllustrationPostRequest(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.CharField(max_length=256)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.book)

class IllustrationDeleteRequest(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	illustration = models.ForeignKey(Illustration, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.illustration.book)

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