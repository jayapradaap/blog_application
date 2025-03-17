from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ContactForm(forms.Form):
    name = forms.CharField(label="Name",max_length=100, required=True)
    email = forms.EmailField(label="Email",required=True)
    message = forms.CharField(label = "Message",required=True)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Username",max_length=100, required=True)
    email = forms.CharField(label="Email",required=True)
    password = forms.CharField(label="Password",required = True)
    password_confirm = forms.CharField(label="Confirm Password",required = True)

    class Meta:
        model = User
        fields = ['username','email','password']

    def clean(self):
        cleaned_data = super().clean()
        Password = cleaned_data.get('password')
        Password_Confirm = cleaned_data.get('password_confirm')

        if Password and Password_Confirm and Password != Password_Confirm:
            raise forms.ValidationError("Password doesn't match")
        
class Login(forms.Form):
    username = forms.CharField(label="Username",max_length=100, required=True)
    password = forms.CharField(label="Password",required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password :
            user = authenticate(username = username,password = password)

            if user is None : 
                raise forms.ValidationError("Invalid Username or Password !")

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email',max_length=254,required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        #This will check whether the user exists in the database or not 
        #If not this will raise an validation error
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User not found !")