const socket = io();
const dropdownIndexArray = [0, 15, 30, 45, 60, 120, 180, 240, 300, 360, 720];

let rotation = 0;
function rotateVideo() {
    rotation += 90;
    document.getElementById(
        "video-container-id"
    ).style.transform = `rotate(${rotation}deg)`;
}

function power(value) {
    if (confirm(`Your Pi is about to ${value}. Are you sure?`)) {
        socket.emit("power", { value: value });
    }
}

function wiperTimer(time) {
    console.log(time);
    socket.emit("wiper", { time: time });
}

socket.on("led", function (data) {
    const led = document.getElementById("led");
    led.checked = data.checked;
});

socket.on("wiper", function (data) {
    const wiperSelect = document.getElementById("wiper-select");
    timerInterval = parseInt(data.time);
    if (timerInterval === null) {
        wiperSelect.selectedIndex = 0;
    } else {
        let timerIntervalIndex = dropdownIndexArray.indexOf(timerInterval);
        console.log(timerIntervalIndex);
        wiperSelect.selectedIndex = timerIntervalIndex;
    }
});

// SETTINGS
function updateSetting(settingName, settingValue) {
    socket.emit("update_setting", { name: settingName, value: settingValue });
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

// BUTTONS
function testWiper() {
    socket.emit("wiper", { time: -1 });
}

function led(checkbox) {
    const value = checkbox.value;
    const checked = checkbox.checked;
    const data = { value: value, checked: checked };
    socket.emit("led", data);
}
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

// INITAL DATA
function getInitalData() {
    fetch("/inital_data").then((response) => {
        response.json().then((data) => {
            console.log(data);
            const led = document.getElementById("led");
            const wiperSelect = document.getElementById("wiper-select");
            led.checked = data.led_on;
            if (data.timer_interval === null) {
                wiperSelect.selectedIndex = 0;
            } else {
                let timerIntervalIndex = dropdownIndexArray.indexOf(
                    data.timer_interval
                );
                wiperSelect.selectedIndex = timerIntervalIndex;
            }
        });
    });
}

window.onload = function () {
    getInitalData();
};
