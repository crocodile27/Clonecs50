from django.urls import path
#This file can be seen as a module informally called "URLconf (URL configuration)"
#This means that it connects web urls from links on the templates with the views file.
from . import views

#urlpatterns is a sequence of django.urls.path() instances.
#The parameters for path are (route, view, kwargs=None, name=None)

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newPage", views.newPage, name="newPage"),
    path("save", views.save, name="save"),
    path("randomPage",views.randomPage, name='randomPage'),
    path("editPage",views.editPage, name='editPage'),
    path("saveEdit",views.saveEdit, name='saveEdit')
]

#Name is for reverse(), reverse matches number of arguments so same name with different arguments is ok
# but you should try and not overlap names.