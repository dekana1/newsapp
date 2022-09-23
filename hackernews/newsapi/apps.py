from django.apps import AppConfig


class NewsapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapi'

    def ready(self):
        
        print("Launching Scheduler...")
        
        from .hnews_scheduler import HN_updater
        
        HN_updater.run_update()
