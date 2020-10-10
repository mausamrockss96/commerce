from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("alterwish/<int:id>", views.alterwish, name="alterwish"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("close/<int:id>", views.close, name="close"),
    path("categories", views.categories, name="categories")
]
