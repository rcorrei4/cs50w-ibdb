import json
import requests
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import Book, Rating, Review, Illustration
from .forms import ReviewForm

def index(request):
	Books = Book.objects.all().order_by('id')
	return render(request, "books/index.html", {
		"Books": Books
		})

def login_view(request):
	if request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "books/login.html", {
			"message": "Invalid username and/or password."
			})
	else:
		return render(request, "books/login.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))

def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "books/register.html", {
			"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()

		except IntegrityError:
			return render(request, "books/register.html", {
			"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "books/register.html")

def book(request, book_id):
	# Get book, illustrations and reviews objects
	book = get_object_or_404(Book, id=book_id)
	illustrations = Illustration.objects.filter(book=book)
	reviews = Review.objects.filter(book=book)

	context = {
		"Book": book,
		"Illustrations": illustrations,
		"Reviews": reviews
	}
	# Show user rating if exists
	if request.user.is_authenticated and Rating.objects.filter(user=request.user, book=book).exists():
		rating = Rating.objects.get(user=request.user, book=book)
		context["rating_score"] = rating.score
		return render(request, "books/book.html", context)
	else:
		return render(request, "books/book.html", context)

def get_book(request, book_id):
	book = get_object_or_404(Book, id=book_id)
	return JsonResponse({"book": {"title": f"{book.title}", "author": f"{book.author}",
							 "synopsis": f"{book.synopsis}", "cover": f"{book.book_cover.url}"}})

def search_book(request):
	# Get user input and request a search on google books api
	search = request.GET.get('q')
	response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={search}&key=AIzaSyB9dSBK_IUe9xWylsNyYuVRoNROM3T6sRQ")
	result = response.json()
	books = dict()
	for count, item in enumerate(result['items']):
		books[f'book{count}'] = dict()
		title = item['volumeInfo']['title']
		author = item['volumeInfo'].get('authors')
		book_id = item['id']
		if not item['volumeInfo'].get('imageLinks') == None:
			image = item['volumeInfo'].get('imageLinks').get('thumbnail')

			books[f'book{count}'] = {"id": book_id, "title": title, "image": image, "author": author}
	# AIzaSyB9dSBK_IUe9xWylsNyYuVRoNROM3T6sRQ

	return render(request, "books/search.html", {
		"books": books
		})

def rate_book(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			data = json.loads(request.body)
			rating_score = data.get('rating')

			#Get book object
			book_id = data.get('book_id')
			book = get_object_or_404(Book, id=book_id)

			# Get rating object and insert score, create if dont exist
			try:
				rating = Rating.objects.get(user=request.user, book=book)
				rating.score = rating_score
				rating.save()
			except ObjectDoesNotExist:
				rating = Rating(book=book, user=request.user, score=rating_score)
				rating.save()

			return JsonResponse({'success':'true', 'score': rating_score}, safe=False)

		if request.method == "DELETE":
			data = json.loads(request.body)
			#Get book object
			book_id = data.get('book_id')
			book = get_object_or_404(Book, id=book_id)
			try:
				rating = Rating.objects.get(user=request.user, book=book)
				rating.delete()
				return JsonResponse({'success':'deleted'})
			except ObjectDoesNotExist:
				return JsonResponse({'error':'rating dont exist!'})
	else:
		return JsonResponse({'error':'login_required'})

@login_required
def review_book(request, book_id):
	book = get_object_or_404(Book, id=book_id)
	context = {
		"book": book
	}
	# Prevent review duplication
	if Review.objects.filter(user=request.user, book=book).exists():
		return HttpResponseRedirect(reverse("edit_review", args=[book_id]))

	if request.method == "POST":
		# Prevent review duplication
		if Review.objects.filter(user=request.user, book=book).exists():
			return JsonResponse({'error':'review already exists!'})

		form = ReviewForm(request.POST)
		if form.is_valid():
			rating = form.cleaned_data['rating']
			title = form.cleaned_data["title"]
			text = form.cleaned_data["text"]
			
			review = Review(user=request.user, book=book, title=title, text=text, score=rating)
			review.save()

			return HttpResponseRedirect(reverse("book", args=[book_id]))
		else:
			context["message"] = "Invalid input"
			return render(request, "books/review.html", context)
	else:
		return render(request, "books/review.html", context)

@login_required
def edit_review(request, book_id):
	book = get_object_or_404(Book, id=book_id)
	if request.method == "POST":
		try:
			review = Review.objects.get(user=request.user, book=book)
			form = ReviewForm(request.POST)
			if form.is_valid():
				rating = form.cleaned_data['rating']
				title = form.cleaned_data["title"]
				text = form.cleaned_data["text"]
				review.score = rating
				review.title = title
				review.text = text
				review.save()
				return HttpResponseRedirect(reverse("book", args=[book_id]))
			else:
				return render(request, "books/review.html", {
				"book": book,
				"message": "Invalid input"
				})
		except ObjectDoesNotExist:
			return HttpResponseRedirect(reverse("book", args=[book_id]))
	else:
		try:
			review = Review.objects.get(user=request.user, book=book)
		except ObjectDoesNotExist:
			return HttpResponseRedirect(reverse("book", args=[book_id]))

		return render(request, "books/edit_review.html", {
			"book": book,
			"review": review
			})