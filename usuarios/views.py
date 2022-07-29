from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm

# Create your views here.


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:home')
        else:
            messages.error(
                request, 'Usuário ou senha não conferem. Tente novamente!')
            return redirect('usuarios:entrar')
    return render(request, 'auth/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("Obrigado pela sua vista!"))
    return redirect('usuarios:entrar')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Cadastro efetuado com sucesso!'))
            return redirect('home:home')

    else:
        form = RegisterUserForm()

    return render(request, 'auth/registrar.html', {'form': form})
