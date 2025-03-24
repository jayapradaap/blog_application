from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blog.models import Category, Post

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
        
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password',max_length=20,required=True)
    confirm_password = forms.CharField(label='Confirm Password',max_length=20,required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Password doesn't match!")

class PostForm(forms.ModelForm):
    title = forms.CharField(label="Title",max_length=250,required=True)
    content = forms.CharField(label="Content",required=True)

    #This particular field is from a separate model called category 
    #Also This field has different choices
    #Inorder to define that we have to use the the module called "ModelChoiceField"
    #Also the field is from the model "Category" we have to use the object called "queryset="
    #This "queryset=" will fetch all the data related to that particular model
    #Before declaring the model name we have to import that model from the models.py
    category = forms.ModelChoiceField(label="Category",required=True,queryset=Category.objects.all())
    image_url = forms.ImageField(label="Image",required=False)
    
    class Meta():
        #Below variables has to be in lowercase
        model = Post
        fields = ['title', 'content', 'category', 'image_url']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        category = cleaned_data.get('category')

        if title and len(title) < 5:
            raise forms.ValidationError("The length of the title must be greater than 5 characters!")
        
        if content and len(content) < 10:
            raise forms.ValidationError("The length of the content must be greater than 10 characters!")
        
    def save(self, commit = ...):
        post = super().save(commit)

        cleaned_data = super().clean() #Fetches the image url if uploaded 

        if cleaned_data.get('image_url'): #If true stores the retrieved url into post.image_url 
            post.image_url = cleaned_data.get('image_url')
        else:
            #Stores the default image url
            img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/450px-No_image_available.svg.png"
            post.image_url = img_url

        if commit:
            post.save()
        return post
