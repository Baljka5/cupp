from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = 'cupp.common'
    label = 'common'

    # This function is the only new thing in this file
    # it just imports the signal file when the app is ready
    def ready(self):
        import cupp.common.signals
