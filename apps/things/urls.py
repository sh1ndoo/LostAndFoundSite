from django.contrib import admin
from django.urls import include, path
from .views import *

app_name = "things"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create/", CreateThingView.as_view(), name="create"),
    path("search/", SearchThingView.as_view(), name="search"),
    path("<int:pk>/", DetailThingView.as_view(), name="detail"),
    path("edit/<int:pk>/", EditThingView.as_view(), name="edit"),
    path("delete/<int:pk>/", DeleteThingView.as_view(), name="delete"),
]