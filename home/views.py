from django.shortcuts import render, redirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib import messages
from .models import Profile, Blog, Comment
from .forms import ProfileForm, BlogForm, UserForm, CommentForm
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q

def home(request):
    blogs = Blog.objects.all().order_by('-fecha_publicacion')
    return render(request, 'home.html', {'blogs': blogs})

def blogs(request):
    blogs = Blog.objects.all().order_by('-fecha_publicacion')
    return render(request, "blog.html", {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=blog).order_by('-dateTime')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.blog = blog
            new_comment.save()
            return redirect('blog_detail', slug=slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog_detail.html', context)

def blog_comments(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=blog)

    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get('content', '')
        if content:
            comment = Comment(user=request.user, content=content, blog=blog)
            comment.save()
            messages.success(request, "Comentario añadido con éxito.")
            return redirect('blog_comments', slug=slug)
        else:
            messages.error(request, "El comentario no puede estar vacío.")

    return render(request, "blog_comments.html", {'blog': blog, 'comments': comments})

@login_required
def edit_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug, autor=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', slug=blog.slug)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'edit_blog_post.html', {'form': form, 'blog': blog})

@login_required
def delete_blog_post(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog eliminado con éxito.")
        return redirect('home')
    
    return render(request, 'delete_blog_post.html', {'blog': blog})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = Blog.objects.filter(título__contains=searched)
        return render(request, "search.html", {'searched':searched, 'blogs':blogs})
    else:
        return render(request, "search.html", {})
    
def search_view(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = Blog.objects.filter(
            Q(title__contains=searched) | Q(content__contains=searched)
        )
        return render(request, 'search_results.html', {'searched': searched, 'blogs': blogs})
    else:
        return render(request, 'search_results.html', {})    

@login_required
@csrf_protect
def add_blogs(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.autor = request.user
            blog.save()
            messages.success(request, "Blog añadido con éxito.")
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'add_blogs.html', {'form': form})

def filtrar_por_categoria(request, categoria):
    blogs = Blog.objects.filter(categoria=categoria).order_by('-fecha_publicacion')
    return render(request, 'home.html', {'blogs': blogs, 'categoria': categoria})

def search_blogs(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = Blog.objects.filter(
            Q(titulo__icontains=searched) | 
            Q(contenido__icontains=searched)
        )
        return render(request, 'search_results.html', {'searched': searched, 'blogs': blogs})
    else:
        return render(request, 'search_results.html', {})

class UpdatePostView(UpdateView):
    model = Blog
    template_name = 'edit_blog_post.html'
    fields = ['título', 'slug', 'contenido', 'image']


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Blog.objects.filter(autor=user)
    return render(request, "user_profile.html", {'posts': posts, 'profile_user': user})

def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None
    return render(request, 'profile.html', {'user': request.user}) #Antes{'profile': profile})

@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil actualizado con éxito.")
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    
    return render(request, "edit_profile.html", {'user_form': user_form, 'profile_form': profile_form})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        print("Usuario:", username)
        print("Contraseñas coinciden:", password1 == password2)

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password1)
        user.save()
        messages.success(request, "Usuario registrado con éxito.")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect("/")  # Redirige a la página principal
            else:
                messages.error(request, "Credenciales inválidas. Inténtalo de nuevo.")
        else:
            messages.error(request, "Por favor, proporciona un nombre de usuario y contraseña.")
        return redirect('login')

    return render(request, "login.html")

def logout(request):
    auth_logout(request)  # Cierra la sesión del usuario
    messages.success(request, "Cerró sesión exitosamente.")
    return redirect('login') # Cierra la sesión del usuario
    