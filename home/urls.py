from django.urls import path
from . import views
from .views import UpdatePostView
from .views import login_view
from django.contrib.auth import views as auth_views
from .views import filtrar_por_categoria
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/edit/', views.edit_blog, name='edit_blog'),
    path('blog/<slug:slug>/delete/', views.delete_blog_post, name='delete_blog_post'),  # Nueva línea
    path('blog/<slug:slug>/comments/', views.blog_comments, name='blog_comments'),
    path('add_blogs/', views.add_blogs, name='add_blog'),
    path('categoria/<str:categoria>/', views.filtrar_por_categoria, name='categoria'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('search/', views.search_view, name='search'),
    path('filtrar/<str:categoria>/', views.filtrar_por_categoria, name='filtrar_por_categoria'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)