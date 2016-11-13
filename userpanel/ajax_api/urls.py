from ajax_api import json_views
from django.conf.urls import url
from django.http import HttpRequest

urlpatterns = [
    # /api/v1/get-temperature-data
    url(r'^test$', json_views.templateFunction),
    url(r'^get-connected-devices$', json_views.getConnectedDevices),
    url(r'^get-device-settings$', json_views.getDeviceSettings),
    url(r'^set-device-settings$', json_views.setDeviceSettings),
    url(r'^get-graph-update$', json_views.getGraphUpdate),
    url(r'^get-windowblind-state$', json_views.getWindowblindState),
    url(r'^set-windowblind-state$', json_views.setWindowblindState)
]

