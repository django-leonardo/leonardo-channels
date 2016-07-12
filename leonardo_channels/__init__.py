
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


default_app_config = 'leonardo_channels.Config'


LEONARDO_APPS = ['leonardo_channels', 'channels']

LEONARDO_CHANNEL_ROUTING = [
    ('leonardo_channels.messages.routing.channel_routing',
     {'path': r"^/messages"}),
    ('leonardo_channels.widgets.routing.channel_widget_routing',
        {'path': r"^/widgets"}),
    ('leonardo_channels.widgets.routing.channel_widget_http',),
]

LEONARDO_JS_FILES = [
    'websocket/reconnecting-websocket.js'
]

LEONARDO_CONFIG = {
    'LEONARDO_CHANNELS_STREAMING_UPDATE': (True, _('Stream updates to the clients (Experimental)'))
}


def is_websocket_enabled(request):
    try:
        import leonardo_channels
    except ImportError:
        return False
    else:
        return True

LEONARDO_EXTRA_CONTEXT = {
    "is_websocket_enabled": is_websocket_enabled
}


class Config(AppConfig):
    name = 'leonardo_channels'
    verbose_name = "leonardo-channels"

    def ready(self):

        from django.db.models.signals import post_save, post_delete
        from .widgets.reciever import update_widget_reciever, update_widget_post_delete
        post_save.connect(update_widget_reciever,
                          dispatch_uid="update_widgets")

        post_delete.connect(update_widget_post_delete,
                            dispatch_uid="update_widget_post_delete")

try:
    from django.channels import Channel, Group  # NOQA isort:skip
    from django.channels.asgi import channel_layers  # NOQA isort:skip
    from django.channels.routing import route, include  # NOQA isort:skip
except ImportError:
    from channels import Channel, Group
    from channels.asgi import channel_layers  # NOQA isort:skip
    from channels.routing import route, include  # NOQA isort:skip

from leonardo_channels.router import router  # noqa
