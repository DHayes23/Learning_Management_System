from django.shortcuts import render, redirect

def index(request):
    user_role = None
    if request.user.is_authenticated:
        user_role = request.user.profile.role

    context = {
        'user_role': user_role,
    }

    return render(request, 'home/index.html', context)

def home_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('account_login')