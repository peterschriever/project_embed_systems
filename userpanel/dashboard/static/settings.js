var devices = [];
var deviceCount = -1;
var alertedBefore = false;
var conDevTimer;
var currentDevice = -1;

function initNewDevice(devID) {
    var htmlcode = "";
    {
        htmlcode = htmlcode + "<option id=\"dev-0-optionSelect\" value=\"" + devID + "\">Control Unit ID: " + devID + "</option>";
    }
    $("#selControlUnit").append(htmlcode);
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
            //$('#control-unit-count').html("<strong>Connected automatic window blind control units: " + data.count + "</strong><br/>");
            if (deviceCount === -1) {
                //do nothing
            } else if (deviceCount < data.count) {
                alert('a device has been connected');
            } else if (deviceCount > data.count) {
                alert('a device has been disconnected');
            } else {
                return;
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
                    currentDevice = -1;
                    $("#dev-" + devices.length + "-optionSelect").remove();
                    $("#noDeviceSelected-option").prop('selected', true);
                    $("#distMax").val("");
                    $("#distMin").val("");
                    $("#light").val("");
                    $("#temp").val("");
                }
            });
        }
    }, "json");
}

function loadSettings(sel) {
    var deviceID = sel.value;
    currentDevice = deviceID;
    if (deviceID == -1) {
        $("#distMax").val("");
        $("#distMin").val("");
        $("#light").val("");
        $("#temp").val("");
    } else {
        $.post("api/v1/get-device-settings", {'deviceID': devices[deviceID]}, function (data) {
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
                console.log('ERROR - loadSettings(): ' + data.error_msg);
            } else {
                $("#distMax").val(data.distMax);
                $("#distMin").val(data.distMin);
                $("#light").val(data.light);
                $("#temp").val(data.temp);
            }
        }, "json");
    }
}

function postSettings() {
    if (currentDevice < 0) {
        alert("select a device to save to first");
        return;
    }
    var postData = {'deviceID': devices[currentDevice], 'temp': $("#temp").val(), 'light': $("#light").val(), 'distMin': $("#distMin").val(), 'distMax': $("#distMax").val()};
    $.post("api/v1/set-device-settings", postData, function (data) {
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
            console.log('ERROR - postSettings(): ' + data.error_msg);
        } else {
            alert(data.msg);
        }
    }, "json");
}

$(function () {
//add devices/charts
    getConnectedDevices();
    //poll every 2 seconds
    conDevTimer = window.setInterval(getConnectedDevices, 2000);
    $("#settings-form").submit(function (event) {
// Stop form from submitting normally
        event.preventDefault();
        postSettings();
    });
});


