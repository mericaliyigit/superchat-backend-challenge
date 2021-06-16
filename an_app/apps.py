from django.apps import AppConfig
from an_app.superchat_apps.superchat_service import SuperchatPlugin

class AnAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'an_app'


class SuperChatConfig(AppConfig):
    name = 'superchat'
    plugin = SuperchatPlugin()