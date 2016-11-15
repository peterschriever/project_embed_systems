/* global charts */
var charts = [];


//function removeFirstDataPoint(device, chart) {
//    charts[device][chart]['chart'].options.data[0].dataPoints.shift();
//}

function addDataPoint(device, chart) {
    var chartObject = charts[device][chart]['chart']
    var length = (chartObject.options.data[0].dataPoints.length) * 10;
    if (length > 10) {
        chartObject.options.data[0].dataPoints.shift();
    }
    charts[device][chart]['lastTime'] -= 10

    chartObject.options.data[0].dataPoints.push({x: charts[device][chart]['lastTime'], y: 25 - Math.random() * 10});
    chartObject.render();
    return;
}

function updateDataPoint(device, chart) {
    var chartObject = charts[device][chart]['chart']
    var length = (chartObject.options.data[0].dataPoints.length);
    chartObject.options.data[0].dataPoints[length - 1].y = 15 - Math.random() * 10;
    chartObject.render();
    return;
}

function getConnectedDevices() {
    $.post( "/api/v1/get-connected-devices", {} ,function(data){
        alert(data.count+' devices connected')
    },"json");
}

$(function () {
    //add devices/charts
    getConnectedDevices();
    //poll every 2 seconds
    window.setInterval(getConnectedDevices, 2000);
    // CanvasJS column chart 

    var c1 = [];
    c1.push({'chart': new CanvasJS.Chart("temp-chart-1", {
            animationEnabled: true,
            backgroundColor: "transparent",
            theme: "theme1",
            axisX: {
                labelFontSize: 14,
                title: "Minutes"

            },
            axisY: {
                labelFontSize: 14,
                title: "Temperature(Â°C) "
            },
            toolTip: {
                borderThickness: 0,
                cornerRadius: 0
            },
            data: [
                {
                    type: "spline", //change type to bar, line, area, pie, etc
                    dataPoints: [
                        {x: 50, y: 14},
                        {x: 40, y: 18},
                        {x: 30, y: 07},
                        {x: 20, y: -1},
                        {x: 10, y: 15},
                        {x: 00, y: 13},
                        {x: -10, y: 4}
                    ]
                }
            ]
        }), 'lastTime': -10});
    c1.push({'chart': new CanvasJS.Chart("light-chart-1", {
            animationEnabled: true,
            backgroundColor: "transparent",
            theme: "theme1",
            axisX: {
                labelFontSize: 14,
                title: "Minutes"

            },
            axisY: {
                labelFontSize: 14,
                title: "Temperature(Â°C) "
            },
            toolTip: {
                borderThickness: 0,
                cornerRadius: 0
            },
            data: [
                {
                    type: "spline", //change type to bar, line, area, pie, etc
                    dataPoints: [
                        {x: 50, y: 14},
                        {x: 40, y: 18},
                        {x: 30, y: 07},
                        {x: 20, y: -1},
                        {x: 10, y: 15},
                        {x: 00, y: 13},
                        {x: -10, y: 4}
                    ]
                }
            ]
        }), 'lastTime': -10});

    charts.push(c1);
    c1 = [];

    charts[0][0]['chart'].render();
    charts[0][1]['chart'].render();

});

