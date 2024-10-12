from django.apps import AppConfig

#from django.db.models.signals import post_migrate
class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        from django.contrib.auth.models import User

