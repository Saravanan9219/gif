from django.conf.urls import url
from api import views as api_views

app_name = 'api'

urlpatterns = [
    url(r'', api_views.get_gif)
]
