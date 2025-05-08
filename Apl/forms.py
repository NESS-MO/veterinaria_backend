from ftplib import MAXLINE
from django import forms 

class craeteNewTask(forms.Form):
    nombre = forms.CharField(label="nombre de la persona", max_length=250)
    apellido = forms.CharField(label="segundo nombre ", max_length=250)