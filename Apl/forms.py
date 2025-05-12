from ftplib import MAXLINE
from django import forms 

class craeteNewTask(forms.Form):
    nombre = forms.CharField(label="nombre de la persona", max_length=250)
    apellido = forms.CharField(label="segundo nombre ", max_length=250)

from .models import ImagenGaleria

class ImagenGaleriaForm(forms.ModelForm):
    class Meta:
        model = ImagenGaleria
        fields = ['imagen', 'titulo', 'orden', 'activa']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Título descriptivo (opcional)'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0'
            }),
        }