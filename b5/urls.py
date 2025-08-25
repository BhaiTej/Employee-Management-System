from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_emp, name='all_emp'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # Employee CRUD
    path('add/', views.add_emp, name='add_emp'),
    path('update/<int:id>/', views.update_emp, name='update_emp'),
    path('remove/<int:id>/', views.remove_emp, name='remove_emp'),
]
