from django.apps import AppConfig


class ProfileUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile_users'

    def ready(self):
        import profile_users.signals
