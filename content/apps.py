from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'

    # we have to register the signals in the apps.py file
    def ready(self):
        # to trigger the signals we have to register the receivers
        # when django load this app it will onvoked

        import content.signals



