var charts = [];
var devices = [];
var deviceCount = -1;
var alertedBefore = false;
var conDevTimer;
var automaticUpdatesPaused = false;
var _changeStateNextIter = false;
var _csDevID = false;

var API_URI = '/api/v1/';

function addDataPoint(device, chart, datapoint) {
    if (datapoint === null) {
        datapoint = 25 - Math.random() * 10;
    }
    var chartObject = charts[device][chart]['chart'];
    $.each(chartObject.options.data[0].dataPoints, function (key, val) {
        chartObject.options.data[0].dataPoints[key].x -= 1;
    });
    var length = chartObject.options.data[0].dataPoints.length;
    if (length > 10) {
        chartObject.options.data[0].dataPoints.shift();
    }
    //charts[device][chart]['lastTime'] -= 10

    chartObject.options.data[0].dataPoints.push({x: 0, y: datapoint});
    chartObject.render();
}

function updateDataPoint(device, chart, datapoint, pos) {
    var chartObject = charts[device][chart]['chart'];
    if (pos === null) {
        pos = (chartObject.options.data[0].dataPoints.length) - 1;
    }
    if(datapoint === null){
        datapoint = 15 - Math.random() * 10;
    }
    chartObject.options.data[0].dataPoints[pos].y = datapoint;
    chartObject.render();
}

function toggleBlind(devID) {
  devID = devices[devID];
  currentState = $("#dev-" + devID + "-status-blind").data("state");
  if (currentState) {
    // 1: rolled down
    _changeStateNextIter = "up";
    _csDevID = devID;
  } else {
    // 0: rolled up
    _changeStateNextIter = "down";
    _csDevID = devID;
  }
}

function initNewDevice(devID) {
    var htmlCode = "";
    {
        htmlCode += "<div id=\"device-" + devID + "\" class=\"rolldown\">";
        htmlCode += "    <div class=\"panel-status-details col-sm-12\">";
        htmlCode += "       <a href=\"#toggle-view\" onclick=\"$('#rollout" + devID + "').toggle();\">";
        htmlCode += "           <h3>Control unit ID: " + devID + "</h3></a>";
        htmlCode += "       <div id=\"rollout" + devID + "\">";
        htmlCode += "           <div id=\"dev-" + devID + "-manualControl\">";
        htmlCode += "               <button id=\"toggleWindowBlind\" disabled=\"disabled\" onclick=\"toggleBlind(" + devID + ");\" class=\"btn btn-default\">";
        htmlCode += "                   Toggle blind status";
        htmlCode += "               </button>";
        htmlCode += "           </div>";
        htmlCode += "           <div id=\"dev-" + devID + "-status\">";
        htmlCode += "               <div id=\"dev-" + devID + "-status-blind\"><strong> Status: </strong> <i class=\"fa fa-square-o\"></i> Loading data.. <br /></div>";
        // htmlCode += "               <div id=\"dev-" + devID + "-status-temp\"><strong> Current temperature: </strong> ?°C <br /></div>";
        // htmlCode += "               <div id=\"dev-" + devID + "-status-light\"><strong> Current light intensity: </strong> ? <br /></div>";
        htmlCode += "           </div>";
        htmlCode += "           <div id=\"dev-" + devID + "-charts\" class=\"panel-status-charts\">";
        htmlCode += "               <!-- CHARTS -->";
        htmlCode += "               <div class=\"col-sm-6\">";
        htmlCode += "                   <div class=\"container\">";
        htmlCode += "                        <div class=\"row m-b-1\">";
        htmlCode += "                           <div class=\"col-xs-6\">";
        htmlCode += "                               <div class=\"card shadow\">";
        htmlCode += "                                   <h4 class=\"card-header\">Temperature</h4>";
        htmlCode += "                                   <div class=\"card-block\">";
        htmlCode += "                                        <div id=\"temp-chart-" + devID + "\"></div>";
        htmlCode += "                                    </div>";
        htmlCode += "                                </div>";
        htmlCode += "                            </div>";
        htmlCode += "                        </div>";
        htmlCode += "                    </div>";
        htmlCode += "                </div>";
        htmlCode += "                <div class=\"col-sm-6\">";
        htmlCode += "                    <div class=\"container\">";
        htmlCode += "                        <div class=\"row m-b-1\">";
        htmlCode += "                            <div class=\"col-xs-6\">";
        htmlCode += "                                <div class=\"card shadow\">";
        htmlCode += "                                    <h4 class=\"card-header\">Light intensity</h4>";
        htmlCode += "                                    <div class=\"card-block\">";
        htmlCode += "                                        <div id=\"light-chart-" + devID + "\"></div>";
        htmlCode += "                                    </div>";
        htmlCode += "                                </div>";
        htmlCode += "                            </div>";
        htmlCode += "                        </div>";
        htmlCode += "                    </div>";
        htmlCode += "                </div>";
        htmlCode += "                <!-- /CHARTS -->";
        htmlCode += "            </div>";
        htmlCode += "        </div>";
        htmlCode += "    </div>";
        htmlCode += "    <br />";
        htmlCode += "    <hr />";
        htmlCode += "</div>";
    }
    $("#devices").append(htmlCode);
    temp = [];
    temp.push({'chart': new CanvasJS.Chart("temp-chart-" + devID, {
            animationEnabled: true,
            backgroundColor: "transparent",
            theme: "theme1",
            axisX: {
                labelFontSize: 14,
                title: "Time"
            },
            axisY: {
                labelFontSize: 14,
                title: "Temperature(°C) "
            },
            toolTip: {
                borderThickness: 0,
                cornerRadius: 0
            },
            data: [
                {
                    type: "spline", //change type to bar, line, area, pie, etc
                    dataPoints: [
                        {x: 0, y: 0}
                    ]
                }
            ]
        }), 'lastTime': 0});
    temp.push({'chart': new CanvasJS.Chart("light-chart-" + devID, {
            animationEnabled: true,
            backgroundColor: "transparent",
            theme: "theme1",
            axisX: {
                labelFontSize: 14,
                title: "Time"

            },
            axisY: {
                labelFontSize: 14,
                title: "Light intensity "
            },
            toolTip: {
                borderThickness: 0,
                cornerRadius: 0
            },
            data: [
                {
                    type: "spline", //change type to bar, line, area, pie, etc
                    dataPoints: [
                        {x: 0, y: 0}
                    ]
                }
            ]
        }), 'lastTime': 0});

    charts.push(temp);

    charts[devID][0]['chart'].render();
    charts[devID][1]['chart'].render();
}

function updateConnectedDevices(data) {
  //update the count at top of the page
  htmlCode = "";
  htmlCode += "<strong>Connected automatic window blind control units: " + data.count + "</strong><br/>"
  htmlCode += "<button id=\"toggleAutoUpdates\" onclick=\"toggleAutoUpdates();\" class=\"btn btn-default\">";
  htmlCode += "  Disable automatic updates <i class=\"fa fa-pause\"></i>";
  htmlCode += "</button>";

  $('#control-unit-count').html(htmlCode);
  if (deviceCount === -1) {
      //do nothing
  } else if (deviceCount < data.count) {
      alert('a device has been connected');
  } else if (deviceCount > data.count) {
      alert('a device has been disconnected');
  }
  deviceCount = data.count;

  tempList = [];
  $.each(data.info, function (key, val) {
      tempList.push(val[1]);
      if ($.inArray(val[1], devices) !== -1) {
          //exists
      } else {
          devices.push(val[1]);
          initNewDevice(devices.length - 1);
      }
  });
  $.each(devices, function (key, val) {
      if ($.inArray(val, tempList) === -1) {
          devices = $.grep(devices, function (value) {
              return value !== val;
          });
          charts.pop();
          $("#device-" + devices.length).remove();
      }
  });
  console.log("connected devices updated")
  console.log(devices)
}

function updateWindowBlindStates(statesData) {
  $.each(statesData, function (key, val) {
      devID = $.inArray(key, devices);
      var htmlstring;
      switch (val['getCurrentState']) {
          case 0: // rolled down
              htmlstring = "<strong> Status: </strong> <i class=\"fa fa-square\"></i> Rolled up <br />";
              break;
          case 1: // rolled up
              htmlstring = "<strong> Status: </strong> <i class=\"fa fa-square-o\"></i> Rolled down <br />";
              break;
          case 2: // rolling down
              htmlstring = "<strong> Status: </strong> <i class=\"fa fa-angle-double-down\"></i> Rolling down <br />";
              break;
          case 3: // rolling up
              htmlstring = "<strong> Status: </strong> <i class=\"fa fa-angle-double-up\"></i> rolling up <br />";
              break;
      }
      $("#dev-" + devID + "-status-blind").html(htmlstring);
      $("#dev-" + devID + "-status-blind").data("state", val['getCurrentState']);
  });
}

function updateGraphs(data) {
    var devID;
    $.each(data, function (key, val) {
        devID = $.inArray(key, devices);
        addDataPoint(devID, 0, val['getTemperature']);
        addDataPoint(devID, 1, val['getLightLevel']);
    });
}

function toggleAutoUpdates() {
  automaticUpdatesPaused = automaticUpdatesPaused ? false : true;

  var toggleBlindsBtn = document.getElementById("toggleWindowBlind");
  toggleBlindsBtn.disabled = toggleBlindsBtn.disabled ? false : true;

  var toggleAutoUpdBtn = document.getElementById("toggleAutoUpdates");
  enabledHtml = "Disable automatic updates <i class=\"fa fa-pause\"></i>";
  disabledHtml = "Enable automatic updates <i class=\"fa fa-play\"></i>";

  toggleAutoUpdBtn.innerHTML = toggleBlindsBtn.disabled ? enabledHtml : disabledHtml;
}

function queryAPI(apiCommand, args) {
  resp = $.post(API_URI + apiCommand, JSON.stringify({'args': args}), null, "json");
  resp.done(function(respData) {
    console.log(respData)
    if (respData.error) {
      // show error
      alert(respData.error_msg);
      return;
    }

    switch (respData.command) {
      case "get-windowblind-state":
        updateWindowBlindStates(respData.data);
        break;
      case "get-connected-devices":
        updateConnectedDevices(respData.data);
        break;
      case "get-graph-update":
        updateGraphs(respData.data);
        break;
      default:
        console.log(respData);
    }

  });
}

// init javascript
$(function () {
  getUpdate = function() {
    if(!automaticUpdatesPaused) {
      queryAPI("get-connected-devices");
      window.setTimeout(function() {queryAPI("get-windowblind-state")}, 100); //43
      window.setTimeout(function() {queryAPI("get-graph-update")}, 4000); //25
      if (_changeStateNextIter) {
        window.setTimeout(function() {queryAPI("set-windowblind-state", {"setState": _changeStateNextIter, "deviceID": _csDevID})}, 6000);
        _changeStateNextIter = false;
      }
    } else {
      if (_changeStateNextIter) {
        console.log({"setState": _changeStateNextIter, "deviceID": _csDevID});
        queryAPI("set-windowblind-state", {"setState": _changeStateNextIter, "deviceID": _csDevID});
        _changeStateNextIter = false;
      }
    }
  }
  getUpdate();
  setInterval(getUpdate, 16000);


  // poll for new devices every 2 seconds
  // conDevTimer = window.setInterval(getConnectedDevices, 2000);

  // get graph data
  // getGraphUpdates();

  // poll every 60 (5) seconds
  // window.setInterval(getGraphUpdates(), 60000);
  // window.setInterval(getGraphUpdates, 5000);

  // poll the control units current states every 4s
  // window.setInterval(getUnitCurrentState, 4000);

});
