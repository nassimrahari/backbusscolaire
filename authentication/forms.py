
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model=get_user_model()
        fields=('profile_photo',)

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
        
class ContactUsForm(forms.Form):
    name = forms.CharField(required=False, label="Nom")
    email = forms.EmailField(label="Adresse e-mail")
    message = forms.CharField(
    widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Votre message ici...'}),
     max_length=1000, label="Message")