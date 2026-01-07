const socket = io();
const dropdownIndexArray = [0, 15, 30, 45, 60, 120, 180, 240, 300, 360, 720];

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
    document.getElementById(
        "video-container-id"
    ).style.transform = `rotate(${rotation}deg)`;
}

function power(value) {
    mdui.confirm({
        headline: "Confirm Action",
        description: `Your Pi is about to ${value}. Are you sure?`,
        confirmText: "Yes",
        cancelText: "No",
        onConfirm: () => {
            socket.emit("power", { value: value });
        }
    });
}

function wiperTimer(time) {
    console.log(time);
    socket.emit("wiper", { time: time });
}

function restartWebserver() {
    mdui.confirm({
        headline: "Restart Webserver",
        description: "Your webserver is about to restart. You will not have any control for a few minutes and may need to reload the page. Are you sure?",
        confirmText: "Yes",
        cancelText: "No",
        onConfirm: () => {
            socket.emit("restart_webserver");
        }
    });
}

socket.on("led", function (data) {
    const led = document.getElementById("led");
    led.checked = data.checked;
});

socket.on("wiper", function (data) {
    const wiperSelect = document.getElementById("wiper-select");
    timerInterval = parseInt(data.time);
    if (timerInterval === null) {
        wiperSelect.value = "0";
    } else {
        wiperSelect.value = timerInterval.toString();
    }
});

// SETTINGS
function updateSetting(settingName, settingValue) {
    socket.emit("update_setting", { name: settingName, value: settingValue });
}

function setupSlider(settingName, sliderId) {
    const slider = document.getElementById(sliderId);
    let debounceTimer;

    slider.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            updateSetting(settingName, parseFloat(slider.value));
        }, 50);
    });

    slider.addEventListener('change', function() {
        updateSetting(settingName, parseFloat(slider.value));
    });
}

setupSlider("brightness", "brightnessSlider");
setupSlider("contrast", "contrastSlider");
setupSlider("saturation", "saturationSlider");
setupSlider("sharpness", "sharpnessSlider");

// BUTTONS
function testWiper() {
    socket.emit("wiper", { time: -1 });
}

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
        description: "Your page is about to reload, resetting the settings to default. Are you sure?",
        confirmText: "Yes",
        cancelText: "No",
        onConfirm: () => {
            location.reload();
        }
    });
}

// INITIAL DATA
function getInitalData() {
    fetch("/inital_data").then((response) => {
        response.json().then((data) => {
            console.log(data);
            const wiperSelect = document.getElementById("wiper-select");
            if (data.timer_interval === null) {
                wiperSelect.value = "0";
            } else {
                wiperSelect.value = data.timer_interval.toString();
            }
        });
    });
}

// Setup event listeners
window.addEventListener('DOMContentLoaded', function () {
    getInitalData();
    
    // Button click handlers
    document.getElementById("test-wiper-btn").addEventListener("click", testWiper);
    document.getElementById("rotate-btn").addEventListener("click", rotateVideo);
    document.getElementById("reload-btn").addEventListener("click", reload);
    document.getElementById("restart-webserver-btn").addEventListener("click", restartWebserver);
    document.getElementById("restart-pi-btn").addEventListener("click", () => power('restart'));
    document.getElementById("shutdown-pi-btn").addEventListener("click", () => power('shutdown'));
    
    // Camera switch handler
    const cameraSwitch = document.getElementById("camera_enabled");
    cameraSwitch.addEventListener("change", (e) => {
        cameraEnabled(e.target.checked);
    });
    
    // Wiper select handler
    const wiperSelect = document.getElementById("wiper-select");
    wiperSelect.addEventListener("change", (e) => {
        wiperTimer(e.target.value);
    });
});
