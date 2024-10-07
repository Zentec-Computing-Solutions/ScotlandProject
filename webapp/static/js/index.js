const socket = io();

function power(value) {
    if (confirm(`Your Pi is about to ${value}. Are you sure?`)) {
        socket.emit("power", { value: value });
    }
}

function led(checkbox) {
    const value = checkbox.value;
    const checked = checkbox.checked;
    const data = { value: value, checked: checked };
    socket.emit("led", data);
}

socket.on("led", function (data) {
    const led = document.getElementById("led");
    led.checked = data.checked;
});

function cameraEnabled(checkbox) {
    const checked = checkbox.checked;
    const video_feed = document.getElementById("video_feed");
    if (checked) {
        video_feed.src = "/video_feed";
    } else {
        video_feed.src = "static/img/disabled_camera.png";
    }
}
function reload() {
    if (
        confirm(
            "Your page is about to reload, resetting the settings to default. Are you sure?"
        )
    ) {
        location.reload();
    }
}
function updateSetting(settingName, settingValue) {
    socket.emit("update_setting", { name: settingName, value: settingValue });
}

function getInitalData() {
    fetch("/inital_data").then((response) => {
        response.json().then((data) => {
            console.log(data);
            const led = document.getElementById("led");
            led.checked = data.led_on;
        });
    });
}

function setupSliderInputPair(settingName, sliderId, inputId) {
    const slider = document.getElementById(sliderId);
    const input = document.getElementById(inputId);
    let debounceTimer;
    function resetValues() {
        slider.value = slider.defaultValue;
        input.value = input.defaultValue;
    }

    function handleInputChange() {
        if (input.value === "") {
            resetValues();
        } else {
            slider.value = input.value;
        }
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            updateSetting(settingName, slider.value);
        }, 50);
    }

    input.oninput = handleInputChange;
    slider.oninput = function () {
        input.value = this.value;
        handleInputChange();
    };
}

setupSliderInputPair("brightness", "brightnessSlider", "brightnessInput");
setupSliderInputPair("contrast", "contrastSlider", "contrastInput");
setupSliderInputPair("saturation", "saturationSlider", "saturationInput");
setupSliderInputPair("sharpness", "sharpnessSlider", "sharpnessInput");

window.onload = function () {
    getInitalData();
};
