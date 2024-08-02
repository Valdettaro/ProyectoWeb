from django.db.models import Avg
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Contact, Materiales, Profile, Rating
from .forms import ContactForm, MaterialesForm, SearchMaterialForm, SearchEmailForm, RegisterForm, LoginForm, RatingForm, SearchRatingForm, ProfileForm, UserEditForm, CustomPasswordChangeForm

def home(request):
    return render(request, "apps/index.html")

def about(request):
    return render(request, "apps/about.html")

def pricing(request):
    return render(request, "apps/pricing.html")

def faq(request):
    return render(request, "apps/faq.html")

def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña inválidos')
    return render(request, 'apps/login.html', {'form': form})

def home(request):
    return render(request, 'apps/index.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                message=form.cleaned_data['message']
            )
            return redirect('home') 
    else:
        form = ContactForm()
    
    return render(request, 'apps/contact.html', {'form': form})

def materiales(request):
    if request.method == 'POST':
        form = MaterialesForm(request.POST)
        if form.is_valid():
            
            Materiales.objects.create(
                material=form.cleaned_data['material'],
                color=form.cleaned_data['color'],
            )
            return redirect('materiales')
    else:
        form = MaterialesForm()
    
    search_form = SearchMaterialForm(request.GET or None)
    materiales = []
    if search_form.is_valid():
        color = search_form.cleaned_data['color']
        materiales = Materiales.objects.filter(color__icontains=color)
    
    return render(request, 'apps/materiales.html', {'form': form, 'search_form': search_form, 'materiales': materiales})

def search_email(request):
    form = SearchEmailForm(request.GET or None)
    users = []
    search_made = False #elimina el resultado de busqueda al inicio

    if form.is_valid():
        email = form.cleaned_data.get('email')
        users = User.objects.filter(email=email).values('id', 'username', 'first_name', 'last_name', 'email')
        search_made = True 

    return render(request, 'apps/search_email.html', {'form': form, 'users': users, 'search_made': search_made})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Tu cuenta ha sido creada exitosamente.')
            return redirect('home')
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        form = RegisterForm()

    return render(request, 'apps/register.html', {'form': form})

def rate_website(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gracias por tu calificación')
            return redirect('rate')
    else:
        form = RatingForm()

    return render(request, 'apps/rate.html', {'form': form})

def search_ratings(request):
    form = SearchRatingForm(request.GET or None)
    ratings = []
    search_made = False
    average_rating = None

    if form.is_valid():
        stars = form.cleaned_data.get('stars')
        ratings = Rating.objects.filter(rating=stars)
        search_made = True
        
        average_rating = Rating.objects.aggregate(average_rating=Avg('rating'))['average_rating'] #revisar si esta calculando bien el promedio

    return render(request, 'apps/search_ratings.html', {
        'form': form,
        'ratings': ratings,
        'search_made': search_made,
        'average_rating': average_rating
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if 'update_user' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Tu información de usuario se ha actualizado con éxito!')
            else:
                messages.error(request, 'Error al actualizar la información del usuario.')

        if 'update_profile' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Tu foto de perfil se ha actualizado con éxito!')
            else:
                messages.error(request, 'Error al actualizar la foto de perfil.')

        if 'update_password' in request.POST:
            if password_form.is_valid():
                user = request.user
                old_password = password_form.cleaned_data['old_password']
                new_password1 = password_form.cleaned_data['new_password1']
                new_password2 = password_form.cleaned_data['new_password2']

                if old_password and new_password1 and new_password2:
                    if not user.check_password(old_password):
                        messages.error(request, 'Tu contraseña actual es incorrecta.')
                    elif new_password1 != new_password2:
                        messages.error(request, 'Las contraseñas no coinciden.')
                    else:
                        user.set_password(new_password1)
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(request, 'Tu contraseña se ha actualizado correctamente!')
                else:
                    messages.error(request, 'Por favor, completa todos los campos de contraseña.')
            else:
                messages.error(request, 'Error al cambiar la contraseña.')

        return redirect('edit_profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'apps/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })