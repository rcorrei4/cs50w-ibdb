from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date

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
	score = models.JSONField(max_length=128, default=dict)
	score_avg = models.FloatField(max_length=32, null=True, blank=True)

	def __str__(self):
		return str(self.title)

	@property
	def get_score(self):
		score = dict()
		score_avg = Rating.objects.filter(book=self).aggregate(Avg('score'))
		score["total"] = Rating.objects.filter(book=self).count()

		for i in range(1, 6):
			score["score_"+str(i)] = Rating.objects.filter(score=i).count()

		self.score = score
		self.score_avg = score_avg['score__avg']
		self.save()

class User(AbstractUser):
	contributions = models.IntegerField(default=0)
	read = models.ManyToManyField(Book, related_name="books_already_read")
	reading = models.ManyToManyField(Book, related_name="books_currently_reading")
	want_to_read = models.ManyToManyField(Book, related_name="books_to_read")

class BookRequest(AbstractBook):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField(auto_now=True)
	change = models.CharField(max_length=24)

	def __str__(self):
		return str(self.title +" - "+ self.change)

class Illustration(models.Model):
	image = models.ImageField(upload_to="books")
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.book)

class IllustrationPostRequest(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="books")
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

	def save(self, *args, **kwargs):
		self.book.get_score
		super().save(*args, **kwargs)

class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	title = models.CharField(max_length=175)
	text = models.CharField(max_length=1024)
	date = models.DateField(auto_now=True)
	score = models.IntegerField(default=0, 
		validators = [
				MaxValueValidator(5),
				MinValueValidator(0)
			]
		)