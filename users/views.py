from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

def home_view(request):
    print("home_view")
    user_id = None
    user_name = None

    if request.user.is_authenticated:
        user_id = request.user.id
        user_name = request.user.username

    return render(request, 'index.html', {'user_id': user_id, 'user_name': user_name})

def login_view(request):
    print("login_view")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['id'] = user.id
            request.session['name'] = user.username

            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name for your home page
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'index.html')

def logout_view(request):
    print("logout_view")
    logout(request)
    request.session.clear()
    return redirect('home')
