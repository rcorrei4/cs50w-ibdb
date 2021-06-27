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
	path('search/', views.search, name="search"),
	path('book/show/<str:book_id>', views.book, name="book"),
	path('book/rate/', views.rate_book, name="rate"),
	path('book/<str:book_id>/illustration', views.illustration, name="illustration"),
	path('book/review/<str:book_id>', views.review_book, name="review_book"),
	path('book/review/edit/<str:book_id>', views.edit_review, name="edit_review"),
	path('book/protect/<str:book_id>', views.protect, name="protect"),
	path('book/aprove/', views.aprove, name="aprove"),
	path('book/reprove/', views.reprove, name="reprove"),
	path('book/aprove_illustration/', views.aprove_illustration, name="aprove_illustration"),
	path('profile/<str:user_id>', views.profile, name="profile"),
	path('profile/<str:user_id>/<str:book_list>', views.user_books, name="user_books"),
	path('show_request/<str:request_id>', views.show_request, name="show_request"),
	path('book/status/<str:book_id>', views.book_status, name="status"),
	path('book/<str:book_id>/score', views.get_book_score, name="get_book_score"),
	path(r'book/show/reviews/<str:book_id>/', views.show_reviews, name="book_reviews")
]