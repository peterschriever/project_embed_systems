var charts = [];
var devices = [];
var deviceCount = -1;
var alertedBefore = false;
var conDevTimer;

//function removeFirstDataPoint(device, chart) {
//    charts[device][chart]['chart'].options.data[0].dataPoints.shift();
//}

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

function initNewDevice(devID) {
    var htmlcode = "";
    {
        htmlcode = htmlcode + "<div id=\"device-" + devID + "\" class=\"rolldown\">";
        htmlcode = htmlcode + "    <div class=\"panel-status-details col-sm-12\">";
        htmlcode = htmlcode + "       <a href=\"#toggle-view\" onclick=\"$('#rollout" + devID + "').toggle();\">";
        htmlcode = htmlcode + "           <h3>Control unit ID: " + devID + "</h3></a>";
        htmlcode = htmlcode + "       <div id=\"rollout" + devID + "\">";
        htmlcode = htmlcode + "           <div id=\"dev-" + devID + "-manualControl\">";
        htmlcode = htmlcode + "               <a href=\"#toggleWindowBlind\" onclick=\"toggleBlind(" + devID + ");\" class=\"btn btn-default\">";
        htmlcode = htmlcode + "                   Roll down <i class=\"fa fa-angle-down\"></i>";
        htmlcode = htmlcode + "               </a>";
        htmlcode = htmlcode + "           </div>";
        htmlcode = htmlcode + "           <div id=\"dev-" + devID + "-status\">";
        htmlcode = htmlcode + "               <div id=\"dev-" + devID + "-status-blind\"><strong> Status: </strong> <i class=\"fa fa-square-o\"></i> Unknown <br /></div>";
        htmlcode = htmlcode + "               <div id=\"dev-" + devID + "-status-temp\"><strong> Current temperature: </strong> ?°C <br /></div>";
        htmlcode = htmlcode + "               <div id=\"dev-" + devID + "-status-light\"><strong> Current light intensity: </strong> ? <br /></div>";
        htmlcode = htmlcode + "           </div>";
        htmlcode = htmlcode + "           <div id=\"dev-" + devID + "-charts\" class=\"panel-status-charts\">";
        htmlcode = htmlcode + "               <!-- CHARTS -->";
        htmlcode = htmlcode + "               <div class=\"col-sm-6\">";
        htmlcode = htmlcode + "                   <div class=\"container\">";
        htmlcode = htmlcode + "                        <div class=\"row m-b-1\">";
        htmlcode = htmlcode + "                           <div class=\"col-xs-6\">";
        htmlcode = htmlcode + "                               <div class=\"card shadow\">";
        htmlcode = htmlcode + "                                   <h4 class=\"card-header\">Temperature</h4>";
        htmlcode = htmlcode + "                                   <div class=\"card-block\">";
        htmlcode = htmlcode + "                                        <div id=\"temp-chart-" + devID + "\"></div>";
        htmlcode = htmlcode + "                                    </div>";
        htmlcode = htmlcode + "                                </div>";
        htmlcode = htmlcode + "                            </div>";
        htmlcode = htmlcode + "                        </div>";
        htmlcode = htmlcode + "                    </div>";
        htmlcode = htmlcode + "                </div>";
        htmlcode = htmlcode + "                <div class=\"col-sm-6\">";
        htmlcode = htmlcode + "                    <div class=\"container\">";
        htmlcode = htmlcode + "                        <div class=\"row m-b-1\">";
        htmlcode = htmlcode + "                            <div class=\"col-xs-6\">";
        htmlcode = htmlcode + "                                <div class=\"card shadow\">";
        htmlcode = htmlcode + "                                    <h4 class=\"card-header\">Light intensity</h4>";
        htmlcode = htmlcode + "                                    <div class=\"card-block\">";
        htmlcode = htmlcode + "                                        <div id=\"light-chart-" + devID + "\"></div>";
        htmlcode = htmlcode + "                                    </div>";
        htmlcode = htmlcode + "                                </div>";
        htmlcode = htmlcode + "                            </div>";
        htmlcode = htmlcode + "                        </div>";
        htmlcode = htmlcode + "                    </div>";
        htmlcode = htmlcode + "                </div>";
        htmlcode = htmlcode + "                <!-- /CHARTS -->";
        htmlcode = htmlcode + "            </div>";
        htmlcode = htmlcode + "        </div>";
        htmlcode = htmlcode + "    </div>";
        htmlcode = htmlcode + "    <br />";
        htmlcode = htmlcode + "    <hr />";
        htmlcode = htmlcode + "</div>";
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
                        // {x: -5, y: 14},
                        // {x: -4, y: 18},
                        // {x: -3, y: 07},
                        // {x: -2, y: -1},
                        // {x: -1, y: 15},
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
                        // {x: -5, y: 14},
                        // {x: -4, y: 18},
                        // {x: -3, y: 07},
                        // {x: -2, y: -1},
                        // {x: -1, y: 15},
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

function getWindowblindStatus() {
    $.post("/api/v1/get-windowblind-state", {'deviceID': null}, function (data) {
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
            console.log('ERROR - getWindowblindStatus(): ' + data.error_msg);
        } else {
            var devID;
            $.each(data.state, function (key, val) {
                devID = $.inArray(key, devices);
                var htmlstring;
                switch (val) {
                    case '00'://rolled down
                        htmlstring = "<strong> Status: </strong> <i class=\"fa fa-square\"></i> Rolled down <br />";
                        break;
                    case '01'://rolled up
                        htmlstring = "<strong> Status: </strong> <i class=\"fa fa-square-o\"></i> Rolled up <br />";
                        break;
                    case '10'://rolling down
                        htmlstring = "<strong> Status: </strong> <i class=\"fa fa-angle-double-down\"></i> Rolling down <br />";
                        break;
                    case '11'://rolling up
                        htmlstring = "<strong> Status: </strong> <i class=\"fa fa-angle-double-up\"></i> rolling up <br />";
                        break;
                }
                $("#dev-" + devID + "-status-blind").html(htmlstring);
            });
        }
    }, "json");
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
                alert(data.error_msg);
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

$(function () {
    //add devices/charts
    getConnectedDevices();
    //poll every 2 seconds
    conDevTimer = window.setInterval(getConnectedDevices, 2000);

    //get device status
    //getWindowblindStatus();
    //poll every 4 seconds
    //window.setInterval(getWindowblindStatus, 4000);

    //get graph data
    getGraphUpdates();

    //poll every 60 seconds
    // window.setInterval(getGraphUpdates(), 60000);
    window.setInterval(getGraphUpdates, 5000);


});
