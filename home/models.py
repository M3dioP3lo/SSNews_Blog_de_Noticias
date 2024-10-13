from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, Thumbnail

class Blog(models.Model):
    CATEGORIES = [
        ('politica', 'Política'),
        ('deportes', 'Deportes'),
        ('internacionales', 'Internacionales'),
        ('ciencia', 'Ciencia'),
    ]

    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=20, choices=CATEGORIES, default='politica')
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    image = models.ImageField(upload_to="blog_images", blank=True, null=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[Thumbnail(300, 300)],
                                     format='JPEG',
                                     options={'quality': 60})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        
        # Procesar la imagen
        if self.image:
            img = Image.open(self.image)
            output = BytesIO()

            # Redimensionar
            img.thumbnail((800, 800))  # Ajusta estos valores según tus necesidades

            # Guardar
            img.save(output, format='JPEG', quality=85)
            output.seek(0)
            self.image = InMemoryUploadedFile(output, 'ImageField', 
                                              f"{self.slug}.jpg", 'image/jpeg',
                                              output.tell(), None)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.titulo


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics', default='profile_pics/default_profile_pic.png')
    bio = models.TextField(blank=True, null=True)
    phone_no = models.IntegerField(blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    linkedin = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)


class BlogPost(models.Model):
    título = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=130, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.autor} Blog Título: {self.título}'
    
    def get_absolute_url(self):
        return reverse('blogs')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:50]}"

    
