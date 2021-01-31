
from django.contrib import admin
from django.urls import path, include
from .views import register, contatti, home, edit_profile, login
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #admin
    path('amministrazione/', admin.site.urls),

    #homepage
    path('', home, name='home'),
    path('contatti', contatti, name='contatti'),

    #authentication , registration ecc....
    path('', include('django.contrib.auth.urls')),
    path('registration', register, name='register'),
    path('edit-profile', edit_profile, name='edit_profile'),

    #prova con social apps
    path('', include('social_django.urls', namespace='social')),
    path("login/", login, name="login"),
    path('logout/', LogoutView.as_view, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    # oder apps included
    path('mercato/', include('prodotti.urls')),
    path('carrello/', include('carrello.urls')),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


