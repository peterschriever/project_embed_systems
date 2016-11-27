var charts = [];
var devices = [];
var deviceCount = -1;
var alertedBefore = false;
var conDevTimer;

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
  devID = typeof devID == 'undefined' ? null : devID;
  setTimeout(function() {
    currentState = getUnitCurrentState(devID);
    console.log(currentState);
    state = (currentState == 0 ? 1 : 0 );

    $.post("/api/v1/set-windowblind-state", {'deviceID': devID, 'state':state}, function (data) {
      if (data.error) {
        if (data.errorcode === '111111') {
          //not (yet) supported function
          if (!alertedBefore) {
            alert(data.error_msg);
            alertedBefore = true;
          }
        } else {
          alert(data.error_msg);
        }
        console.log('ERROR - getUnitCurrentState(): ' + data.error_msg);
      } else {
        var devID;
        console.log(data.data);
        // TODO: change HTML
        // $.each(data.state, function (key, val) {
        //     devID = $.inArray(key, devices);
        //     var htmlstring;
        //     switch (val) {
        //         case '00'://rolled down
        //             htmlstring = "<strong> Status: </strong> <i class=\"fa fa-square\"></i> Rolled down <br />";
        //             break;
        //         case '01'://rolled up
        //             htmlstring = "<strong> Status: </strong> <i class=\"fa fa-square-o\"></i> Rolled up <br />";
        //             break;
        //         case '10'://rolling down
        //             htmlstring = "<strong> Status: </strong> <i class=\"fa fa-angle-double-down\"></i> Rolling down <br />";
        //             break;
        //         case '11'://rolling up
        //             htmlstring = "<strong> Status: </strong> <i class=\"fa fa-angle-double-up\"></i> rolling up <br />";
        //             break;
        //     }
        //     $("#dev-" + devID + "-status-blind").html(htmlstring);
        // });
      }
    }, "json");
  }, 1000);
}

function initNewDevice(devID) {
    var htmlcode = "";
    {
        htmlcode += "<div id=\"device-" + devID + "\" class=\"rolldown\">";
        htmlcode += "    <div class=\"panel-status-details col-sm-12\">";
        htmlcode += "       <a href=\"#toggle-view\" onclick=\"$('#rollout" + devID + "').toggle();\">";
        htmlcode += "           <h3>Control unit ID: " + devID + "</h3></a>";
        htmlcode += "       <div id=\"rollout" + devID + "\">";
        htmlcode += "           <div id=\"dev-" + devID + "-manualControl\">";
        htmlcode += "               <a href=\"#toggleWindowBlind\" onclick=\"toggleBlind(" + devID + ");\" class=\"btn btn-default\">";
        htmlcode += "                   Roll down <i class=\"fa fa-angle-down\"></i>";
        htmlcode += "               </a>";
        htmlcode += "           </div>";
        htmlcode += "           <div id=\"dev-" + devID + "-status\">";
        htmlcode += "               <div id=\"dev-" + devID + "-status-blind\"><strong> Status: </strong> <i class=\"fa fa-square-o\"></i> Loading data.. <br /></div>";
        // htmlcode += "               <div id=\"dev-" + devID + "-status-temp\"><strong> Current temperature: </strong> ?°C <br /></div>";
        // htmlcode += "               <div id=\"dev-" + devID + "-status-light\"><strong> Current light intensity: </strong> ? <br /></div>";
        htmlcode += "           </div>";
        htmlcode += "           <div id=\"dev-" + devID + "-charts\" class=\"panel-status-charts\">";
        htmlcode += "               <!-- CHARTS -->";
        htmlcode += "               <div class=\"col-sm-6\">";
        htmlcode += "                   <div class=\"container\">";
        htmlcode += "                        <div class=\"row m-b-1\">";
        htmlcode += "                           <div class=\"col-xs-6\">";
        htmlcode += "                               <div class=\"card shadow\">";
        htmlcode += "                                   <h4 class=\"card-header\">Temperature</h4>";
        htmlcode += "                                   <div class=\"card-block\">";
        htmlcode += "                                        <div id=\"temp-chart-" + devID + "\"></div>";
        htmlcode += "                                    </div>";
        htmlcode += "                                </div>";
        htmlcode += "                            </div>";
        htmlcode += "                        </div>";
        htmlcode += "                    </div>";
        htmlcode += "                </div>";
        htmlcode += "                <div class=\"col-sm-6\">";
        htmlcode += "                    <div class=\"container\">";
        htmlcode += "                        <div class=\"row m-b-1\">";
        htmlcode += "                            <div class=\"col-xs-6\">";
        htmlcode += "                                <div class=\"card shadow\">";
        htmlcode += "                                    <h4 class=\"card-header\">Light intensity</h4>";
        htmlcode += "                                    <div class=\"card-block\">";
        htmlcode += "                                        <div id=\"light-chart-" + devID + "\"></div>";
        htmlcode += "                                    </div>";
        htmlcode += "                                </div>";
        htmlcode += "                            </div>";
        htmlcode += "                        </div>";
        htmlcode += "                    </div>";
        htmlcode += "                </div>";
        htmlcode += "                <!-- /CHARTS -->";
        htmlcode += "            </div>";
        htmlcode += "        </div>";
        htmlcode += "    </div>";
        htmlcode += "    <br />";
        htmlcode += "    <hr />";
        htmlcode += "</div>";
    }
    $("#devices").append(htmlcode);
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

function getConnectedDevices() {
    $.post("/api/v1/get-connected-devices", {}, function (data) {
        if (data.error) {
            if (data.errorcode === '111111') {
                //not (yet) supported function
                if (!alertedBefore) {
                    alert(data.error_msg);
                    alertedBefore = true;
                }
            } else {
                alert(data.error_msg);
            }
            console.log('ERROR - getConnectedDevices(): ' + data.error_msg);
        } else {
            //update the count at top of the page
            $('#control-unit-count').html("<strong>Connected automatic window blind control units: " + data.count + "</strong><br/>");
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
        }
    }, "json");
}

function updateWindowBlindStates(statesData) {
  console.log(statesData);
  // $.each(statesData, function (key, val) {
  //     devID = $.inArray(key, devices);
  //     var htmlstring;
  //     switch (val) {
  //         case 0: // rolled down
  //             htmlstring = "<strong> Status: </strong> <i class=\"fa fa-square\"></i> Rolled down <br />";
  //             break;
  //         case 1: // rolled up
  //             htmlstring = "<strong> Status: </strong> <i class=\"fa fa-square-o\"></i> Rolled up <br />";
  //             break;
  //         case 2: // rolling down
  //             htmlstring = "<strong> Status: </strong> <i class=\"fa fa-angle-double-down\"></i> Rolling down <br />";
  //             break;
  //         case 3: // rolling up
  //             htmlstring = "<strong> Status: </strong> <i class=\"fa fa-angle-double-up\"></i> rolling up <br />";
  //             break;
  //     }
  //     $("#dev-" + devID + "-status-blind").html(htmlstring);
  // });
}

function getGraphUpdates() {
    $.post("/api/v1/get-graph-update", {'deviceID': null}, function (data) {
        if (data.error) {
            if (data.errorcode === '111111') {
                //not (yet) supported function
                if (!alertedBefore) {
                    alert(data.error_msg);
                    alertedBefore = true;
                }
            } else {
                // alert(data.error_msg);
            }
            console.log('ERROR - getGraphUpdates(): ' + data.error_msg);
        } else {
            var devID;
            $.each(data.data, function (key, val) {
                devID = $.inArray(key, devices);
                addDataPoint(devID, 0, val[0]);
                addDataPoint(devID, 1, val[1]);
            });
        }
    }, "json");
}

function queryAPI(apiCommand, args) {
  resp = $.post(API_URI + apiCommand, {'args': args}, null, "json");
  resp.done(function(respData) {
    if (respData.error) {
      // show error
      alert(respData.error_msg);
      return;
    }

    switch (respData.command) {
      case "get-windowblind-state":
        updateWindowBlindStates(respData.data);
        break;
      default:
        console.log(respData);
    }

  });
}

// init javascript
$(function () {
    // add devices/charts
    getConnectedDevices();

    queryAPI("get-windowblind-state");

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
