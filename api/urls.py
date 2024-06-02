from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    
    path('user-home/', views.userHome, name='user-home'),
    path('user-home/<str:id>', views.userHomeWithId, name='user-home'),
    path('user-apply-prop/<str:propId>/<str:userId>/', views.applyProperty, name='user-home'),
    path('user-applications/', views.userApplications, name='user-home'),
    path('user-applications/<str:id>', views.userApplicationsWithId, name='user-home'),
    path('application-withdraw/<str:id>', views.withdrawApplication, name='user-home'),
    path('user-rentals/', views.userRentals, name='user-home'),
    path('user-rentals/<str:id>', views.userRentalsWithId, name='user-home'),
    path('vacate-rental/<str:id>', views.vacateProperty, name='user-home'),
    
    path('owner-home/', views.ownerHome, name='owner-home'),
    path('owner-home/<str:id>', views.ownerHomeWIthId, name='owner-home'),
    path('owner-applications/', views.ownerApplications, name='owner-home'),
    path('owner-applications/<str:id>', views.ownerApplicationsWithId, name='owner-home'),
    path('new-property/', views.newProperty, name='new-property'),
    path('update-property/<str:id>/', views.updateProperty, name='update-property'),
    path('approve-application/<str:id>/', views.approveApplication, name='update-property'),
    path('reject-application/<str:id>/', views.rejectApplication, name='update-property'),
    
    path('admin-home', views.adminHome, name='admin-home'),
    path('admin-applications', views.adminApplications, name='admin-home'),
    path('allUsers', views.allUsers, name='admin-home'),
    
    
    
]