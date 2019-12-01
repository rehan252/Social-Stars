from django.urls import path
from social import views

app_name = 'social'

urlpatterns = [
    path('', views.SocialHome.as_view(), name='home'),
    path('connect/<operation>/<int:pk>', views.connect, name='connect'),
    path('update/<int:post_id>/', views.update_post, name='update'),
    path('delete/<int:post_id>/', views.delete_post, name='delete'),
    path('post/<int:post_id>/preference/<int:user_pref>/', views.post_preference, name='post_preference'),
]
