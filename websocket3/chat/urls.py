from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
# from .views import CustomLoginView

urlpatterns = [
	path("", views.index, name="index"),
	path("room/<str:room_name>/", views.room, name="room"),
	path("redirect-room/<str:room_name>/", views.redirect_to_room, name="redirect-room"),
	path("auth/login", LoginView.as_view(template_name="chat/LoginPage.html"), name="login-user"),
	# path('auth/login', CustomLoginView.as_view(template_name="chat/LoginPage.html"), name="login-user"),
	path("auth/logout", LogoutView.as_view(), name="logout-user"),
	path("get_user_list/", views.get_user_list, name="get_user_list")
]
