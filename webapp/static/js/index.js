const socket = io();
const dropdownIndexArray = [0, 15, 30, 45, 60, 120, 180, 240, 300, 360, 720];
const sampleConfirmTimers = {};
const sampleDefaultLabels = {};

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
    const elementId = "sample-button" + buttonNumber;
    const buttonEl = document.getElementById(elementId);

    if (!buttonEl) {
        return;
    }

    const defaultLabel =
        sampleDefaultLabels[elementId] || buttonEl.textContent.trim();
    sampleDefaultLabels[elementId] = defaultLabel;

    const pending = buttonEl.dataset.confirming === "true";

    if (pending) {
        clearTimeout(sampleConfirmTimers[elementId]);
        buttonEl.dataset.confirming = "false";
        buttonEl.textContent = defaultLabel;
        delete sampleConfirmTimers[elementId];
        enableAllSampleButtons();
        completeSampleAction(buttonNumber);
        return;
    }

    buttonEl.dataset.confirming = "true";
    buttonEl.textContent = "Confirm?";
    disableOtherSampleButtons(elementId);
    sampleConfirmTimers[elementId] = setTimeout(() => {
        buttonEl.dataset.confirming = "false";
        buttonEl.textContent = defaultLabel;
        enableAllSampleButtons();
        delete sampleConfirmTimers[elementId];
    }, 3000);
}

function completeSampleAction(buttonNumber) {
    socket.emit("sample_button_confirmed", { button: buttonNumber });
}

socket.on("led", function (data) {
    const led = document.getElementById("led");
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
        }, 50);
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
        });
    });
}

// Setup event listeners
window.addEventListener("DOMContentLoaded", function () {
    getInitalData();
});
