var devices = [];
var deviceCount = -1;
var alertedBefore = false;
var conDevTimer;
var currentDevice = -1;
var automaticUpdatesPaused = false;
var _selectedDevID = 0;

var API_URI = '/api/v1/';

function initNewDevice(devID) {
    var htmlcode = "";
    {
        htmlcode = htmlcode + "<option id=\"dev-optionSelect\" value=\"" + devID + "\">Control Unit ID: " + devID + "</option>";
    }
    $("#selControlUnit").append(htmlcode);
}

function updateConnectedDevices(data) {
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
        // NOTE remove thing is a bit strange?
        $("#dev-" + devices.length + "-optionSelect").remove();
        $("#noDeviceSelected-option").prop('selected', true);
        $("#distMax").val("");
        $("#distMin").val("");
        $("#light").val("");
        $("#temp").val("");
    }
  });
}

function loadSettings(sel) {
    var deviceID = sel.value;
    currentDevice = devices[deviceID];
    console.log(currentDevice);
    if (deviceID == -1) {
        $("#distMax").val("");
        $("#distMin").val("");
        $("#light").val("");
        $("#temp").val("");
        $('#settings-loading').hide();
        $('#introText').fadeIn();
    } else {
      // set Loading
      $('#settings-loading').fadeIn();
      $('#introText').hide();

      queryAPI("get-device-settings", {"deviceID": currentDevice});
      _selectedDevID = currentDevice;
    }
}

function updateSettings(data) {
  $('.rolloutSettings').show();
  $('.temperatureBoundaries').show();
  $('.submitBtnContainer').show();
  $('#settings-loading').fadeOut();
  $("#distMax").val(data.distMax);
  $("#distMin").val(data.distMin);
  $("#light").val(data.light);
  $("#temp").val(data.temp);
}

function postSettings() {
    if (currentDevice < 0) {
        alert("select a device to save to first");
        return;
    }
    var postData = {
      'deviceID': _selectedDevID,
     'maxTemperature': $("#temp").val(),
     'maxLightIntensity': $("#light").val(),
     'minRolloutAmount': $("#distMin").val(),
     'maxRolloutAmount': $("#distMax").val()
    };
    console.log(postData);
    queryAPI('set-device-settings', postData)
    // $.post("api/v1/set-device-settings", postData, function (data) {
    //     if (data.error) {
    //         if (data.errorcode === '111111') {
    //             //not (yet) supported function
    //             if (!alertedBefore) {
    //                 alert(data.error_msg);
    //                 alertedBefore = true;
    //             }
    //         } else {
    //             alert(data.error_msg);
    //         }
    //         console.log('ERROR - postSettings(): ' + data.error_msg);
    //     } else {
    //         alert(data.msg);
    //     }
    // }, "json");
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
      case "get-device-settings":
        updateSettings(respData.data);
        break;
      case "set-device-settings":
        alert("Device settings changed!");
        break;
      default:
        console.log(respData);
    }

  });
}

$(function () {
  getUpdate = function() {
    if(!automaticUpdatesPaused) {
      queryAPI("get-connected-devices");
    }
  }
  getUpdate();
  // setInterval(getUpdate, 5000);

// //add devices/charts
//     getConnectedDevices();
//     //poll every 2 seconds
//     conDevTimer = window.setInterval(getConnectedDevices, 2000);
    $("#settings-form").submit(function (event) {
      // Stop form from submitting normally
        event.preventDefault();
        postSettings();
    });
});
