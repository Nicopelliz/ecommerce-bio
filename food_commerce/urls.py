
from django.contrib import admin
from django.urls import path, include
from .views import register, contatti, home

urlpatterns = [
    #admin
    path('amministrazione/', admin.site.urls),

    #homepage
    path('', home, name='home'),
    path('contatti', contatti, name='contatti'),

    #authentication , registration ecc....
    path('', include('django.contrib.auth.urls')),



    path('registration', register, name='register'),


    # oders apps included
    path('mercato/', include('prodotti.urls')),
    path('carrello/', include('carrello.urls')),
]
