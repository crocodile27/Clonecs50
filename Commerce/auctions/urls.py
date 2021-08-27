from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("submit_listing", views.submit_listing, name="submit_listing"),
    path("<int:active_listings_id>", views.display_listing, name="display_listing"),
    path("<int:listing_id>/close_auction",views.close_auction, name="close_auction"),
    path("<int:listing_id>/add_comment",views.add_comment, name="add_comment"),
    path("<int:listing_id>/new_bid",views.new_bid, name="new_bid"),
    path("<int:listing_id>/add_watchlist",views.add_watchlist, name="add_watchlist"),
    path("<int:listing_id>/remove_watchlist",views.remove_watchlist, name="remove_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category")
]
