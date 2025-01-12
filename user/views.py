from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout , login, authenticate

# Create your views here.
@login_required
def index(request):
   return  render (request,'index.html')
    
    


def login_view(request):
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Find the user with the given email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        # Authenticate the user
        if user is not None and user.check_password(password):
            # If user exists and password is correct, log them in
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('/')  # Redirect to index or home page
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid email or password.")
            return redirect('login')  # Redirect to login page if credentials are incorrect

    return render(request, 'login.html')

def register(request):
     
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        print(username+" "+email+" "+password2+" "+password)

        # Validate passwords match
        if password != password2:
            messages.error(request, "Passwords do not match.")
          
            return redirect('register')
       

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
           
            return redirect('register')
        

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            
            return redirect('register')
        

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
       
    

        # Authenticate and log in the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('/')  # Redirect to the index page

    
    return render(request, 'register.html')


def logout_view(request):
     logout(request)
     return redirect('login')
