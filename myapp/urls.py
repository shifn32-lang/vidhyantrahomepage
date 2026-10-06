from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('newsletter/submit/', views.newsletter_submit, name='newsletter_submit'),
    path('login/', views.login_submit, name='login_submit'),
    path('logout/', views.logout_view, name='logout'),
]
