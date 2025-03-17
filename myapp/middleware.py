from django.urls import reverse
from django.shortcuts import redirect
class Redirectauthenticatedmiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):

        #To check whether the user is authenticated or not
        if request.user.is_authenticated :
            path_to_redirect = [reverse('blog:login'),reverse('blog:register')]

            #If authenticated the user shouldn't be present in the paths defined above
            if request.path in path_to_redirect:
                return redirect('blog:index')
        
        #If not authenticated this will pass the request to the respective view functions 
        response = self.get_response(request)

        #And in return we will get the response that we should pass back to where the request came from
        return response
    
class RestrictUnauthenticatedUserMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = [reverse('blog:dashboard')]

        #This will check for the Unauthenticated user and restrict them from accessing the restricted paths
        if not request.user.is_authenticated and request.path in restricted_paths:
            return redirect(reverse('blog:login'))
        
        #If the user is authenticated then it will directly send the request to the respective view functions
        response = self.get_response(request)
        #This will return the response for that request 
        return response