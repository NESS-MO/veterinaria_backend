from django.urls import path
from Apl.views import * 

urlpatterns = [
    path('Quit/', index),
    path('Letra/', Palabra),
    path('hello/<int:id>', hello),
    path('Adminis/',Adminis)
]
