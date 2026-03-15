from django.apps import AppConfig


class RecommendationsConfig(AppConfig):
    name = 'recommendations'
    
    # When django starts up ready() is called
    def ready(self):
        # Import signals so they get registerd when Django starts
        import recommendations.signals
