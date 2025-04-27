from django.apps import AppConfig
import threading
class DinarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dinar'
    
    def ready(self):
        from .log_producer import start_log_producer
        threading.Thread(target=start_log_producer, daemon=True).start()
