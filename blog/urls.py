from django.urls import path
from blog.views import (
    create_blogpost_view
)

app_name = 'blog'

urlpatterns = [
    path('create/', create_blogpost_view, name='create'),

]
