from django.conf.urls import url
from django.http import HttpRequest
from ajax_api import json_views

urlpatterns = [
    # @TODO: actually create api, this is just an example
    # /api/v1/get-temperature-data
     #url(r'^get-temperature-data$', json_views.getTemperatureData(request)),
     url(r'^test$', json_views.templateFunction),
     url(r'^get-connected-devices$', json_views.getConnectedDevices)
]

