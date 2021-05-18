from django.contrib import admin
from .models import Book, BookRequest, Rating, Review, Illustration, User

admin.site.register(Book)
admin.site.register(BookRequest)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Illustration)
admin.site.register(User)