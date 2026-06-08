from django.apps import AppConfig


class ArchiveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'archive'
    verbose_name = '非遗数字档案管理'

    def ready(self):
        from . import signals
