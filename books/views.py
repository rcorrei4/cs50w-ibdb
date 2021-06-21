import json
import requests
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q, Avg
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


from .models import Book, BookRequest,Rating, Review, Illustration, IllustrationPostRequest, IllustrationDeleteRequest, User
from .forms import ReviewForm, BookForm, EditBookForm, EditBookRequestForm, ProtectionForm

def index(request):
	Books = Book.objects.all().order_by('id')
	last_added_books = Book.objects.all().order_by('-id')[:10]
	best_book_ratings = Book.objects.all().order_by('-score_avg')
	reviews = Review.objects.all().order_by('-id')[:5]

	return render(request, "books/index.html", {
		"Books": Books,
		"last_added_books": last_added_books,
		"best_book_ratings": best_book_ratings,
		"reviews": reviews
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
	book = get_object_or_404(Book, id=book_id)

	# Get book illustrations and reviews objects
	illustrations = Illustration.objects.filter(book=book)
	reviews = Review.objects.filter(book=book)

	read = False
	reading = False
	want_to_read = False

	if User.objects.filter(username=request.user.username, read=book).exists():
		read = True

	if User.objects.filter(username=request.user.username, reading=book).exists():
		reading = True

	if User.objects.filter(username=request.user.username, want_to_read=book).exists():
		want_to_read= True

	context = {
		"Book": book,
		"Illustrations": illustrations,
		"Reviews": reviews,
		"ProtectionForm": ProtectionForm(),
		"read": read,
		"reading": reading,
		"want_to_read": want_to_read
	}

	# Show user rating if exists
	if request.user.is_authenticated and Rating.objects.filter(user=request.user, book=book).exists():
		rating = Rating.objects.get(user=request.user, book=book)
		context["rating_score"] = rating.score
		return render(request, "books/book.html", context)
	else:
		return render(request, "books/book.html", context)

@login_required
def contribute(request):
	if request.method == "POST":
		form = BookForm(request.POST, request.FILES)
		if form.is_valid():
			book = form.save()
			user = User.objects.get(username=request.user.username)
			user.contributions += 1
			user.save()

			return HttpResponseRedirect(reverse("book", args=[book.id]))
		else:
			return render(request, "books/contribute.html", {
				"form": form
				})
	else:
		initial_data = {
			"isbn": {"isbn10": "Insert ISBN10 here", "isbn13": "Insert ISBN13 here"},
			"genres": {"genres": ["insert", "genres", "here"]},
			"characters": {"characters": ["Insert", "characters", "here"]},
			"keywords": {"keywords": ["Insert", "keywords", "here"]},
		}
		return render(request, "books/contribute.html", {
			"form": BookForm(initial=initial_data)
			})

@login_required
def edit_book(request, book_id):
	book = get_object_or_404(Book, id=book_id)
	if request.method == "POST":
		if book.protection:
			new_book = BookRequest()
			form = EditBookRequestForm(request.POST, instance=book)
			if form.is_valid():
				new_book.title = form.cleaned_data["title"]
				new_book.author = form.cleaned_data["author"]
				new_book.isbn = form.cleaned_data["isbn"]
				new_book.synopsis = form.cleaned_data["synopsis"]
				new_book.genres = form.cleaned_data["genres"]
				new_book.published = form.cleaned_data["published"]
				new_book.original_title = form.cleaned_data["original_title"]
				new_book.characters = form.cleaned_data["characters"]
				new_book.keywords = form.cleaned_data["keywords"]
				new_book.change = "Book"
				new_book.user = User.objects.get(username=request.user.username)
				new_book.book_cover = "NULL"
				new_book.save()

				return HttpResponseRedirect(reverse("book", args=[book.id]))

		else:
			form = EditBookForm(request.POST, instance=book)
			if form.is_valid():
				edit_book = form.save()
				user = User.objects.get(username=request.user.username)
				user.contributions += 1
				user.save()

				return HttpResponseRedirect(reverse("book", args=[book.id]))
			else:
				return render(request, "books/edit_book.html", {
					"form": form
					})
	else:
		if book.protection:
			return render(request, "books/edit_book.html", {
				"form": EditBookRequestForm(instance=book),
				"book_id": book.id
				})
		return render(request, "books/edit_book.html", {
			"form": EditBookForm(instance=book),
			"book_id": book.id
			})

def get_book(request, book_id):
	book = get_object_or_404(Book, id=book_id)
	return JsonResponse({"book": {"title": book.title, "author": book.author,
						 "synopsis": book.synopsis, "cover": book.book_cover.url,
						 "genre": book.genres["genres"][0] }})

def search(request):
	entry_search = request.GET['q']
	books = Book.objects.filter(Q(title__icontains=entry_search) | Q(author__icontains=entry_search) | Q(isbn__icontains=entry_search) | Q(genres__icontains=entry_search) | Q(original_title__icontains=entry_search) | Q(characters__icontains=entry_search) | Q(keywords__icontains=entry_search))

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

			book.get_score
			return JsonResponse({'success':'true', 'score': rating_score}, safe=False)

		if request.method == "DELETE":
			data = json.loads(request.body)
			#Get book object
			book_id = data.get('book_id')
			book = get_object_or_404(Book, id=book_id)
			try:
				rating = Rating.objects.get(user=request.user, book=book)
				rating.delete()
				book.get_score
				return JsonResponse({'success':'deleted'})
			except ObjectDoesNotExist:
				return JsonResponse({'error':'rating dont exist!'})
	else:
		return JsonResponse({'error':'login_required'})

@login_required
def illustration(request, book_id):
	book = get_object_or_404(Book, id=book_id)
	if request.method == "POST":
		user = get_object_or_404(User, username=request.user.username)
		if book.protection:
			for i in request.FILES.values():
				illustration = IllustrationPostRequest(user=user, book=book, image=i)
				illustration.save()

		else:
			for i in request.FILES.values():
				illustration = Illustration(book=book, image=i)
				illustration.save()
				user.contributions += 1

		return HttpResponseRedirect(reverse("book", args=[book_id]))

	if request.method == "DELETE":
		data = json.loads(request.body)
		user = get_object_or_404(User, username=request.user.username)
		if book.protection:
			for i in data:
				illustration = get_object_or_404(Illustration, id=i)
				illustration_delete = IllustrationDeleteRequest(user=user, illustration=illustration)
				illustration_delete.save()
		else:
			for i in data:
				illustration = get_object_or_404(Illustration, id=i)
				illustration.delete()
				user.contributions += 1

		return JsonResponse({'success':'deleted'})

	else:
		illustrations = Illustration.objects.filter(book=book)
		return render(request, "books/illustration.html", {
			"book_id": book.id,
			"book_title": book.title,
			"illustrations": illustrations
			})

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
				return render(request, "books/edit_review.html", {
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

@login_required
def protect(request, book_id):
	if request.user.is_superuser:
		book = get_object_or_404(Book, id=book_id)

		if book.protection:
			book.protection = False
		else:
			book.protection = True

		book.save()
	else:
		pass
		
	return HttpResponseRedirect(reverse("book", args=[book_id]))

@login_required
def aprove(request):
	if request.method == "POST":
		user = get_object_or_404(User, username=request.user.username)
		data = json.loads(request.body)
		book_post_id = data.get("id")
		
		book_request_model = get_object_or_404(BookRequest, id=book_post_id)
		book = Book.objects.get(title=book_request_model.title)
		book.title = book_request_model.title
		book.author = book_request_model.author
		book.isbn = book_request_model.isbn
		book.synopsis = book_request_model.synopsis
		book.genres = book_request_model.genres
		book.published = book_request_model.published
		book.original_title = book_request_model.original_title
		book.characters = book_request_model.characters
		book.keywords = book_request_model.keywords
		book.save()
		user.contributions += 1

		book_request_model.delete()

		return JsonResponse({'success':'aproved'})

	else:
		book_post_request = BookRequest.objects.all()
		illustration_post_request = IllustrationPostRequest.objects.all()
		illustration_delete_request = IllustrationDeleteRequest.objects.all()
		
		return render(request, "books/aprove.html", {
			"book_post": book_post_request,
			"illustration_post": illustration_post_request,
			"illustration_delete": illustration_delete_request
			})

@login_required
def aprove_illustration(request):
	if request.method == "POST":
		user = get_object_or_404(User, username=request.user.username)
		data = json.loads(request.body)
		illustration_post_request_id = data.get("id")

		illustration_post_request = IllustrationPostRequest.objects.get(id=illustration_post_request_id)
		illustration = Illustration(image=illustration_post_request.image, book=illustration_post_request.book)
		illustration.save()
		user.contributions += 1
		illustration_post_request.delete()

		return JsonResponse({'success':'aproved'})

	if request.method == "DELETE":
		user = get_object_or_404(User, username=request.user.username)
		data = json.loads(request.body)
		illustration_delete_request_id = data.get("id")

		illustration_delete_request = IllustrationDeleteRequest.objects.get(id=illustration_delete_request_id)
		illustration_delete_request.illustration.delete()
		illustration_delete_request.delete()
		user.contributions += 1

		return JsonResponse({'success':'aproved'})

	else:
		return HttpResponseRedirect(reverse("aprove"))

@login_required
def reprove(request):
	if request.user.is_superuser:
		data = json.loads(request.body)
		model = data.get("model")
		model_id = data.get("id")
		
		if model == "book":
			book = get_object_or_404(BookRequest, id=model_id)
			book.delete()

		if model == "illustration":
			illustration = get_object_or_404(IllustrationPostRequest, id=model_id)
			illustration.delete()

		if model == "remove_illustration":
			illustration = get_object_or_404(IllustrationDeleteRequest, id=model_id)
			illustration.delete()

		return JsonResponse({'success':'aproved'})
	else:
		return HttpResponseRedirect(reverse("index"))


@login_required
def show_request(request, request_id):
	book = get_object_or_404(BookRequest, id=request_id)
	
	return render(request, "books/show_request.html", {
		"Book": book
		})

@login_required
def profile(request, user_id):
	user = User.objects.get(username=request.user.username)
	book_post_request = BookRequest.objects.filter(user=user)
	illustration_post_request = IllustrationPostRequest.objects.filter(user=user)
	illustration_delete_request = IllustrationDeleteRequest.objects.filter(user=user)

	return render(request, "books/profile.html", {
		"user_id": user_id,
		"reviews": Review.objects.filter(user=request.user).count(),
		"ratings": Rating.objects.filter(user=request.user).count(),
		"read": user.read.count(),
		"reading": user.reading.count(),
		"want": user.reading.count(),
		"book_post": book_post_request,
		"illustration_post": illustration_post_request,
		"illustration_delete": illustration_delete_request
		})

def user_books(request, user_id, book_list):
	user = User.objects.get(id=user_id)

	if book_list == "read" or book_list == "reading" or book_list == "want_to_read":
		books = getattr(user, book_list).all()

		return render(request, "books/search.html", {
			"books": books
			})

	else:
		return HttpResponseRedirect(reverse("index"))

def book_status(request, book_id):
	if request.method == "POST":
		data = json.loads(request.body)
		option = data.get("option")

		book = get_object_or_404(Book, id=book_id)
		user = User.objects.get(username=request.user.username)

		if User.objects.filter(username=user.username, read=book).exists():
			user.read.remove(book)

		if User.objects.filter(username=user.username, reading=book).exists():
			user.reading.remove(book)

		if User.objects.filter(username=user.username, want_to_read=book).exists():
			user.want_to_read.remove(book)

		if option == "want_read":
			user.want_to_read.add(book)

		if option == "reading":
			user.reading.add(book)

		if option == "read":
			user.read.add(book)

		user.save()
		return JsonResponse({'success': option})
	else:
		return HttpResponseRedirect(reverse("index"))

def get_book_score(request, book_id):
	book = get_object_or_404(Book, id=book_id)

	return JsonResponse(book.score)