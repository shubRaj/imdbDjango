from django.urls import re_path
from . import views
app_name="app_imdbclone"
urlpatterns = [
    re_path("^(?P<id>\w+)?/?$",views.Home.as_view(),name="imdbclone_home"),
]
