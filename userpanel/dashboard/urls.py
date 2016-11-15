from django.conf.urls import url
from dashboard import views

urlpatterns = [
    # /
    url(r'^$', views.index, name="dash-index"),
    # /settings/
    url(r'^settings$', views.settings, name="dash-settings")
]
