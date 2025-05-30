from ftplib import MAXLINE
from django import forms 
from .models import Cliente
from .models import ImagenGaleria
from .models.AdminCitas import CitaRapida
from django.core.validators import MinValueValidator
from datetime import date

class ImagenGaleriaForm(forms.ModelForm):
    class Meta:
        model = ImagenGaleria
        fields = ['imagen', 'titulo', 'orden']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['orden'].widget.attrs.update({
            'min': '1',
            'max': '9',
            'class': 'border rounded px-2 py-1 w-full'
        })
        self.fields['imagen'].widget.attrs.update({
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
        })
        self.fields['titulo'].widget.attrs.update({
            'class': 'border rounded px-2 py-1 w-full',
            'placeholder': 'Título opcional'
        })
        
class DatosCliente(forms.Form):
    class Meta:
        model = Cliente
        fields = [
            'primer_nombre', 
            'primer_apellido', 
            'tipo_documento', 
            'correo_electronico', 
            'telefono'
            'numero_documento'
        ]
        widgets = {
            'primer_nombre': forms.TextInput(attrs={
                'placeholder': 'Ingresa tu nombre',
                'pattern': '[A-Za-záéíóúÁÉÍÓÚñÑ ]+',
                'title': 'Solo letras y espacios'
            }),
            'primer_apellido': forms.TextInput(attrs={
                'placeholder': 'Ingresa tu apellido',
                'pattern': '[A-Za-záéíóúÁÉÍÓÚñÑ ]{2,50}',
                'title': 'Solo letras (entre 2 y 50 caracteres)'
            }),
            'tipo_documento': forms.Select(attrs={
                'required': 'required'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'placeholder': 'Ingresa tu correo electrónico',
                'required': 'required'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ingresa tu número de teléfono',
                'pattern': '[0-9]{10}',
                'title': '10 dígitos numéricos',
                'required': 'required'
            }),
            'numero_documento': forms.TextInput(attrs={
                'placeholder': 'Ingresa tu número de documento',
                'pattern': '[0-9]{6,12}|[A-Za-z]{1,2}[0-9]{4,8}',
                'title': 'Formato: 6-12 dígitos o letras + números para extranjería'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(DatosCliente, self).__init__(*args, **kwargs)
        # Asegurarnos de que los campos requeridos coincidan con el frontend
        if 'primer_nombre' in self.fields: 
            self.fields['primer_nombre'].required = True
        if 'primer_apellido' in self.fields:
            self.fields['primer_apellido'].required = True
        if 'tipo_documento' in self.fields:
            self.fields['tipo_documento'].required = True
        if 'correo_electronico' in self.fields:    
            self.fields['correo_electronico'].required = True
        if 'telefono' in self.fields: 
            self.fields['telefono'].required = True
        if 'numero_docuemnto' in self.fields:
            self.fields['numero_docuemnto'].required = True     
            
class DatosMascota(forms.Form):
    mascota = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa el nombre de tu mascota',
            'pattern': '[A-Za-záéíóúÁÉÍÓÚñÑ ]{2,30}',
            'title': 'Solo letras (entre 2 y 30 caracteres)',
            'required': 'required',
            'id': 'mascota'
        })
    )
    
    clase_mascota = forms.ChoiceField(
        widget=forms.Select(attrs={
            'required': 'required',
            'id': 'clase-mascota'
        }),
        choices=[('', 'Selecciona la especie de tu mascota'), ('Perro', 'Perro'), ('Gato', 'Gato')]
    )
    
    edad_numero = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Número',
            'min': '0',
            'max': '30',
            'required': 'required',
            'style': 'width: 60%; display: inline-block;',
            'id': 'edad-numero'
        })
    )
    
    edad_unidad = forms.ChoiceField(
        widget=forms.Select(attrs={
            'style': 'width: 35%; display: inline-block; margin-left: 5%;',
            'id': 'edad-unidad'
        }),
        choices=[('meses', 'Meses'), ('años', 'Años')],
        initial='meses'
    )
    
    raza_mascota = forms.ChoiceField(
        widget=forms.Select(attrs={
            'required': 'required',
            'id': 'raza-mascota'
        }),
        choices=[]
    )
    
    otra_raza = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Especifique la raza',
            'id': 'otra-raza',
            'style': 'display: none;'
        })
    )

    def __init__(self, *args, **kwargs):
        super(DatosMascota, self).__init__(*args, **kwargs)
        self.fields['raza_mascota'].choices = self.get_raza_choices()
        
    def get_raza_choices(self):
        return [
            ('', 'Seleccione la raza'),
            ('Criollo', 'Criollo'),
            ('Labrador Retriever', 'Labrador Retriever'),
            ('Bulldog Francés', 'Bulldog Francés'),
            ('Poodle', 'Poodle'),
            ('Golden Retriever', 'Golden Retriever'),
            ('Pug', 'Pug'),
            ('Bulldog Inglés', 'Bulldog Inglés'),
            ('Beagle', 'Beagle'),
            ('Rottweiler', 'Rottweiler'),
            ('Pastor Alemán', 'Pastor Alemán'),
            ('Persa', 'Persa'),
            ('Siamés', 'Siamés'),
            ('Bengalí', 'Bengalí'),
            ('Maine Coon', 'Maine Coon'),
            ('Ragdoll', 'Ragdoll'),
            ('Esfinge', 'Esfinge'),
            ('Angora', 'Angora'),
            ('otro', 'Otro (especificar)')
        ]

    def clean(self):
        cleaned_data = super().clean()
        
        # Validación para raza "otro"
        if cleaned_data.get('raza_mascota') == 'otro' and not cleaned_data.get('otra_raza'):
            self.add_error('otra_raza', 'Por favor especifique la raza')
        
        return cleaned_data
    
class CitaForm(forms.Form):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'required': 'required',
            'id': 'fecha',
            'class': 'date-input'
        }),
        validators=[MinValueValidator(date.today, message="La fecha no puede ser en el pasado")]
    )
    
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'required': 'required',
            'id': 'hora'
        })
    )
    
    main_service = forms.ChoiceField(
        choices=[
            ('', 'Seleccione principal*'),
            ('consulta', 'Consulta'),
            ('esterilizacion', 'Esterilización'),
            ('guarderia', 'Guardería'),
            ('vacunacion', 'Vacunación'),
            ('profilaxis', 'Profilaxis'),
            ('cirugias', 'Cirugías')
        ],
        widget=forms.Select(attrs={
            'id': 'main-service',
            'class': 'service-select',
            'required': 'required'
        })
    )
    
    extra_service = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Servicio extra (opcional)'),
            ('consulta', 'Consulta'),
            ('esterilizacion', 'Esterilización'),
            ('guarderia', 'Guardería'),
            ('vacunacion', 'Vacunación'),
            ('profilaxis', 'Profilaxis'),
            ('cirugias', 'Cirugías'),
            ('ninguno', 'Ninguno')
        ],
        widget=forms.Select(attrs={
            'id': 'extra-service',
            'class': 'service-select'
        })
    )
    
    extra = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'id': 'extra'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        main_service = cleaned_data.get('main_service')
        extra_service = cleaned_data.get('extra_service')
        
        if extra_service == 'ninguno':
            cleaned_data['extra_service'] = ''
        
        # Combinar servicios para el campo extra
        servicios = [main_service]
        if extra_service and extra_service != 'ninguno':
            servicios.append(extra_service)
        
        cleaned_data['extra'] = ", ".join(servicios)
        
        return cleaned_data

class CitaRapidaForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        edad_valor = self.data.get('edad_mascota_valor')
        edad_tipo = self.data.get('edad_mascota_tipo')
        if not edad_valor or not edad_tipo:
            raise forms.ValidationError("Debe ingresar la edad y el tipo (años o meses).")
        if edad_tipo == 'años' and (int(edad_valor) < 0 or int(edad_valor) > 20):
            raise forms.ValidationError("La edad en años debe estar entre 0 y 20.")
        if edad_tipo == 'meses' and (int(edad_valor) < 0 or int(edad_valor) > 11):
            raise forms.ValidationError("La edad en meses debe estar entre 0 y 11.")
        # ...otras validaciones...
        return cleaned_data

    class Meta:
        model = CitaRapida
        fields = [
            'numero_documento',
            'nombre_cliente',
            'nombre_mascota',
            'edad_mascota',        
            'raza_mascota',        
            'fecha',
            'hora',
            'servicio',
            'estado',
            'observaciones'
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'border p-2 rounded-md'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'border p-2 rounded-md'}),
            'estado': forms.Select(attrs={'class': 'border p-2 rounded-md'}),
            'observaciones': forms.TextInput(attrs={'class': 'border p-2 rounded-md'}),
        }