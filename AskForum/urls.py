"""AskForum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import static
from App import  views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contactus/', views.contactus, name='contactus'),
    path('sessionval/', views.sessionval, name='sessionval'),
    
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    path('askaquestion/', views.askaquestion, name='askaquestion'),
    path('answer/<str:id>/', views.answer, name='answer'),
    path('postanswer/', views.postanswer, name='postanswer'),

    path('recent/', views.recent, name='recent'),
    path('mostAnswered/', views.mostAnswered, name='mostAnswered'),
    path('mostVisited/', views.mostVisited, name='mostVisited'),
    path('mostPopular/', views.mostPopular, name='mostPopular'),

    path('profile/<str:id>', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('userProfile/', views.userProfile, name='userProfile'),
    path('vote/',views.vote,name='vote'),
    path('answervote/', views.answervote, name='answervote'),

    path('session_logout/',views.session_logout, name='session_logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Custom Error URLs
handler404 = 'App.views.error_404_view'
handler500 = 'App.views.error_500_view'