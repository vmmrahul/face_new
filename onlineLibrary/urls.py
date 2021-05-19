"""onlineLibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin', login, name='loginPage'),
    path('dashboard', dashboard, name='dashboard'),
    path('signout', signout, name='signout'),
    path('changePassword', changePassword, name='changePassword'),
    path('changePassword', changePassword, name='changePassword'),

    # add member
    path('addMeber', addMeber, name='addMeber'),
    path('viewMembers', viewMembers, name='viewMembers'),

    #     addLibrary
    path('addLibrary', addLibrary, name='addLibrary'),
    path('ViewLibrary', ViewLibrary, name='ViewLibrary'),
    path('deleteLibrary/<int:id>', deleteLibrary, name='deleteLibrary'),
    path('editLibrary/<int:id>', editLibrary, name='editLibrary'),
    #     end of addLibrary

    #    User Side Work Start
    #    Login Page
    path('', userLogin, name='userLogin'),
    path('home', home, name='home'),
    path('Usersignout', Usersignout, name='Usersignout'),
    path('addSection', addSection, name='addSection'),
    path('viewSection', viewSection, name='viewSection'),
    path('deleteSection', deleteSection, name='deleteSection'),
    #     add books
    path('addbook', addbook, name='addbook'),
    path('viewBook', viewBook, name='viewBook'),
    path('deleteBook', deleteBook, name='deleteBook'),

    #     Ebook
    path('addEbook',addEbook, name='addEbook'),
    path('viewEBook',viewEBook, name='viewEBook'),
    path('deleteEbook',deleteEbook, name='deleteEbook'),
]
