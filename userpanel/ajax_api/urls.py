from ajax_api import json_views
from django.conf.urls import url
from django.http import HttpRequest

urlpatterns = [
    # /api/v1/test
    url(r'^test$', json_views.templateFunction),
    # /api/v1/get-connected-devices
    url(r'^get-connected-devices$', json_views.getConnectedDevices),
    # /api/v1/get-device-settings
    url(r'^get-device-settings$', json_views.getDeviceSettings),
    # /api/v1/set-device-settings
    url(r'^set-device-settings$', json_views.setDeviceSettings),
    # /api/v1/get-graph-update
    url(r'^get-graph-update$', json_views.getGraphUpdate),
    # /api/v1/get-windowblind-state
    url(r'^get-windowblind-state$', json_views.getWindowblindState),
    # /api/v1/set-windowblind-state
    url(r'^set-windowblind-state$', json_views.setWindowblindState),
    # /api/v1/set-windowblind-mode
    url(r'^set-windowblind-mode$', json_views.setWindowBlindMode)
]
