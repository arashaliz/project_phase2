from django import forms

from .models import District, Clinic, User


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['location']


class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'address', 'district']


class PatientRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    district = forms.ModelChoiceField(queryset=District.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'district']


class ClinicManagerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    district = forms.ModelChoiceField(queryset=District.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'district', 'clinic']

