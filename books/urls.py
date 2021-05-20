from . import views
from django.urls import path

urlpatterns = [ 
	path('', views.index, name="index"),
	path('login', views.login_view, name="login"),
	path('register', views.register, name="register"),
	path('logout', views.logout_view, name="logout"),
	path('contribute', views.contribute, name="contribute"),
	path('book/<str:book_id>', views.get_book, name="get_book"),
	path('book/edit/<str:book_id>/', views.edit_book, name="edit_book"),
	path('book/search/', views.search_book, name="search_book"),
	path('book/show/<str:book_id>', views.book, name="book"),
	path('book/rate/', views.rate_book, name="rate"),
	path('book/<str:book_id>/illustration', views.illustration, name="illustration"),
	path('book/review/<str:book_id>', views.review_book, name="review_book"),
	path('book/review/edit/<str:book_id>', views.edit_review, name="edit_review"),
	path('book/protect/<str:book_id>', views.protect, name="protect"),
	path('book/aprove/', views.aprove, name="aprove"),
	path('profile/<str:user_id>', views.profile, name="profile")
]