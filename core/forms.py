# core/forms.py
from django import forms
from core.models import User
from core.utils.validators import validate_rut

class CustomerRegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(attrs={'class': 'form-control'}))
    rut = forms.CharField(label="RUT", validators=[validate_rut], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 12345678-5'}))
    email = forms.EmailField(label="Correo Electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'rut', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Usamos el email como nombre de usuario único
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user