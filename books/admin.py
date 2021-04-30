from django.contrib import admin
from .models import Book, Rating, Review, Illustration, User

admin.site.register(Book)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Illustration)
admin.site.register(User)