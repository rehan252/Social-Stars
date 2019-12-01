from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/<int:pk>/', views.user_profile, name='view_profile_with_pk'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password', views.change_password, name='change-password'),
    path('reset-password/',
         auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html',
                                              success_url=reverse_lazy(
                                                  'accounts:password_reset_done'),
                                              email_template_name='accounts/reset_password_email.html'),
         name='password_reset'),
    path('reset-password/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
                      template_name='accounts/reset_password_confirm.html',
                      success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='accounts/reset_password_complete.html'),
         name='password_reset_complete')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
