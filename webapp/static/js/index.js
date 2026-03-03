const socket = io();

function disableOtherSampleButtons(activeId) {
    document.querySelectorAll(".sample-button").forEach((btn) => {
        if (btn.id !== activeId) {
            btn.disabled = true;
        }
    });
}

function enableAllSampleButtons() {
    document.querySelectorAll(".sample-button").forEach((btn) => {
        btn.disabled = false;
    });
}

let rotation = 0;
function rotateVideo() {
    rotation += 90;
    if (rotation === 90 || rotation === 270) {
        document.getElementById("video-container-id").style.marginTop = "290px";
        document.getElementById("video-container-id").style.marginLeft =
            "-275px";
    } else {
        document.getElementById("video-container-id").style.marginTop = "10px";
        document.getElementById("video-container-id").style.marginLeft = "1px";
    }
    if (rotation === 360) {
        rotation = 0;
    }
    console.log(rotation);
    document.getElementById("video-container-id").style.transform =
        `rotate(${rotation}deg)`;
}

function power(value) {
    mdui.confirm({
        headline: "Confirm Action",
        description: `Your host device is about to ${value}. Are you sure?`,
        confirmText: "Yes",
        cancelText: "No",
        onConfirm: () => {
            socket.emit("power", { value: value });
        },
        onCancel: () => {},
    });
}

function restartWebserver() {
    mdui.confirm({
        headline: "Restart Webserver",
        description:
            "Your webserver is about to restart. You will not have any control for a few minutes and may need to reload the page. Are you sure?",
        confirmText: "Yes",
        cancelText: "No",
        onConfirm: () => {
            socket.emit("restart_webserver");
        },
        onCancel: () => {},
    });
}

function confirmSampleButton(buttonNumber) {
    let buttonEnable = document.getElementById(
        "sample-button" + buttonNumber + "-enable",
    );
    let button = document.getElementById("sample-button" + buttonNumber);
    button.disabled = true;
    buttonEnable.disabled = false;
    //buttonEnable.icon = "lock";
    socket.emit("sample_button_confirmed", { button: buttonNumber });
}

function toggleSampleButton(buttonNumber) {
    let buttonEnable = document.getElementById(
        "sample-button" + buttonNumber + "-enable",
    );
    buttonEnable.disabled = true;
    //buttonEnable.icon = "lock-open";
    let button = document.getElementById("sample-button" + buttonNumber);
    button.disabled = !button.disabled;
    setTimeout(() => {
        button.disabled = true;
        buttonEnable.disabled = false;
        //buttonEnable.icon = "lock";
    }, 3000);
}

socket.on("led", function (data) {
    const led = document.getElementById("ledSwitch");
    led.checked = data.checked;
});

// SETTINGS
function updateSetting(settingName, settingValue) {
    socket.emit("update_setting", { name: settingName, value: settingValue });
}

function setupSlider(settingName, sliderId) {
    const slider = document.getElementById(sliderId);
    let debounceTimer;

    slider.addEventListener("input", function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            updateSetting(settingName, parseFloat(slider.value));
        }, 100);
    });

    slider.addEventListener("change", function () {
        console.log(slider.value);
        updateSetting(settingName, parseFloat(slider.value));
    });

    slider.labelFormatter = (value) => value.toFixed(1);
}

setupSlider("brightness", "brightnessSlider");
setupSlider("contrast", "contrastSlider");
setupSlider("saturation", "saturationSlider");
setupSlider("sharpness", "sharpnessSlider");
setupSlider("ledBrightness", "ledBrightnessSlider");

// BUTTONS

function cameraEnabled(checked) {
    const video_feed = document.getElementById("video_feed");
    if (checked) {
        video_feed.src = "/video_feed";
    } else {
        video_feed.src = "static/img/disabled_camera.png";
    }
}

function reload() {
    mdui.confirm({
        headline: "Reload Page",
        description:
            "Your page is about to reload, resetting the settings to default. Are you sure?",
        confirmText: "Yes",
        cancelText: "No",
        onConfirm: () => {
            location.reload();
        },
    });
}

// INITIAL DATA
function getInitalData() {
    fetch("/inital_data").then((response) => {
        response.json().then((data) => {
            console.log(data);
            document.getElementById("ledSwitch").checked = data.led_on;
            document.getElementById("ledBrightnessSlider").disabled =
                !data.led_on;
        });
    });
}

function ledToggle(checkbox) {
    const checked = checkbox.checked;
    const data = { checked: checked };
    console.log(data);
    socket.emit("led", data);
    if (checked) {
        const ledBrightnessSlider = document.getElementById(
            "ledBrightnessSlider",
        );
        ledBrightnessSlider.disabled = false;
        ledBrightnessSlider.value = 5;
    } else {
        const ledBrightnessSlider = document.getElementById(
            "ledBrightnessSlider",
        );
        ledBrightnessSlider.disabled = true;
    }
}

function checkVideoFeed() {
    const video_feed = document.getElementById("video_feed");
    if (video_feed.src && video_feed.src !== "") {
        video_feed.onload = () => {
            // Video is loading successfully
        };
        video_feed.onerror = () => {
            console.error("Video feed failed to load");
            location.reload();
        };
    } else {
        console.warn("Video feed src is empty");
        location.reload();
    }
}

setInterval(checkVideoFeed, 1000);

// Setup event listeners
window.addEventListener("DOMContentLoaded", function () {
    getInitalData();
});
