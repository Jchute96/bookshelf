from django.apps import AppConfig


class DemoConfig(AppConfig):
    name = 'demo'
    
    def ready(self):
        # Import signals so they get registerd when Django starts
        import demo.signals
