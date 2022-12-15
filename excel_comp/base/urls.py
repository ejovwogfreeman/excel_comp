from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('documentation/', views.documentation_page, name="documentation_page"),
    path('compare_csv/', views.compare_csv_page, name="compare_csv_page"),
    path('view_csv/', views.view_csv_page, name="view_csv_page"),
    path('view_csv/<int:pk>/', views.view_csv_detail_page, name="view_csv_detail_page"),
    path('delete_csv/<int:pk>/', views.delete_csv_page, name="delete_csv_page"),
    path('profile/', views.profile_page, name="profile_page"),
    path('update_profile/', views.update_profile_page, name="update_profile_page"),
    path('register/', views.register_page, name="register_page"),
    path('login/', views.login_page, name="login_page"),
    path('logout/', views.logout_page, name="logout_page"),
    path('upload_csv/', views.upload_csv_page, name="upload_csv_page"),
]
