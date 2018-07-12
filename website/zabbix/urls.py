from django.conf.urls import url
from .views import verify

urlpatterns = [
    url(r'check/(?P<url>[a-zA-Z0-9_.-/:?=#]*)', verify),
]