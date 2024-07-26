from django.urls import path
from django.contrib.auth.views import LogoutView
from apps import views
from .views import contact, materiales, search_email, register, login, rate_website, search_ratings


urlpatterns = [
    path('', views.home),
    path('index.html', views.home, name='home'), #
    path('about.html', views.about, name='about'), 
    path('contact/', contact, name='contact'), #
    path('pricing.html', views.pricing, name='pricing'),
    path('rate/', views.rate_website, name='rate'), #
    path('search_ratings/', views.search_ratings, name='search_ratings'),
    path('faq.html', views.faq, name='faq'), 
    path('login/', views.login, name='login'), #
    path('logout/', LogoutView.as_view(template_name='apps/index.html'), name="logout"), #
    path('materiales/', materiales, name='materiales'), #
    path('search-email/', search_email, name='search_email'), #
    path('register/', views.register, name='register'), #
]