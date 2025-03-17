from django.shortcuts import render, redirect
from django.http import HttpResponse as response
from django.urls import reverse 
import logging
from .models import Post, AboutUs
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm, ForgotPasswordForm, Login, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail

# Create your views here.
'''
posts=[ 
        {'id':1,'post_title':'Post 1','content':'Content of post 1'},
        {'id':2,'post_title':'Post 2','content':'Content of post 2'},
        {'id':3,'post_title':'Post 3','content':'Content of post 3'},
        {'id':4,'post_title':'Post 4','content':'Content of post 4'},
    ]
    '''
def index(request):
    blog_title = "Search Posts"

    #Getting the data from the post model
    all_posts = Post.objects.all()

    #paginate
    paginator = Paginator(all_posts,3) #this will create a rule to maintain only three posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,"index.html",{'value':blog_title,'page_obj':page_obj})

def detail(request,slug):

    #Getting static data:
    #post=next((item for item in posts if item['id'] == int(post_id)),None)
    #detail_title="Posts and awards"
   # logger = logging.getLogger("TESTING")
    #logger.debug(f'Post value is {post}')

    #Getting dynamic data:
    try:
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)

    except Post.DoesNotExist:
        raise Http404("Page Doesn't exist!")
    
    return render(request,"detail.html",{'post':post,'related_posts':related_posts})

def old_url_redirect(request):
    return redirect(reverse('blog:new_page_url'))

def new_url(request):
    return response("Redirected to the new URL page")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST) 
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        logger = logging.getLogger("TESTING")
        if form.is_valid():
            logger.debug(f'Post data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            success_message = "Your email has been sent successfully!"
        else:
            logger.debug('Form validation failure.')
        return render(request,"contact.html",{'form':form,'success_message':success_message})
    return render(request,"contact.html")

def about(request):
    about_content = AboutUs.objects.first()

    if about_content is None or not about_content.content :
        about_content = "Default content goes here !"
    else:
        about_content = about_content.content

    return render(request,"about.html",{'about_content':about_content})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #form validation
        if form.is_valid():
           user =  form.save(commit=False)
           user.set_password(form.cleaned_data['password'])
           user.save()
           #sends the success message to the template
           messages.success(request,"Registration Successfull. You can log in !")
           return redirect("blog:login")
        

    return render(request,"register.html",{'form':form})

def login(request):
    form = Login() #this is to carry some empty value back to the templates if the validation fails ,To avoid getting an error
    #Checks the type of request
    if request.method == 'POST':
        form = Login(request.POST) #An object for the login form in the forms page
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username and password:
                user = authenticate(username=username,password = password)
                if username is not None:
                    auth_login(request, user) #login function imported from auth module 
                    print("LOGIN Successfull !")
                    return redirect("blog:dashboard") #redirect to dashboard
    return render(request,"login.html",{'form':form})


def dashboard(request):
    blog_title = "My Posts"
    return render(request,"dashboard.html",{'title':blog_title})

def logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forgot_password(request):
    print("Step 1")
    form = ForgotPasswordForm()
    if request.method =='POST':
       form = ForgotPasswordForm(request.POST)
       
       #This will check whether the form is valid or not
       if form.is_valid():
           email = form.cleaned_data['email']
           user = User.objects.get(email=email)
           token = default_token_generator.make_token(user)
           uid = urlsafe_base64_encode(force_bytes(user.pk))
           current_site = get_current_site(request)
           domain = current_site.domain
           subject = "Reset Password Requested"
           message = render_to_string('reset_password_email.html',{
               'domain' : domain,
               'uid' : uid,
               'token' : token
           })
           send_mail(subject,message,"noreply@examlple.com",[email])
           messages.success(request,"The request mail has been sent")
           
    return render(request,"forgot_password.html",{'form':form})

def reset_password(request):
    pass