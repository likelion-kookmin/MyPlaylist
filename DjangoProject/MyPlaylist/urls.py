"""MyPlaylist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import snsApp.views
import serviceApp.views
import playlistApp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', serviceApp.views.home, name='home'),
    path('feeds', serviceApp.views.feeds, name='feeds'),
    path('popular', serviceApp.views.popular, name='popular'),
    path('myprofile', snsApp.views.myprofile, name='myprofile'),
    path('login', serviceApp.views.login, name='login'),
    path('logout', serviceApp.views.logout, name='logout'),
    path('register', serviceApp.views.register, name='register'),
    path('integrate/add', serviceApp.views.add_integrate, name='integrate'),
    
    path('<str:username>', snsApp.views.profile, name='user-profile'),
    path('myprofile/myprofile', serviceApp.views.home, name='sssmyprofile'),

    # path('', serviceApp.views.root, name='root'),
    # path('<str:query>', serviceApp.views.root, name='root'),
    # path('accounts/' )
    # path('user/<str:username>', snsApp.views.profile, name='user-profile'),
]


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
