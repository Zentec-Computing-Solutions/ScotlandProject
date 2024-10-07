const socket = io();

function power(value) {
    if (confirm(`Your Pi is about to ${value}. Are you sure?`)) {
        socket.emit("power", value);
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
/**
 * Sends a socket.io event to the server to update the specified setting to the given value.
 * @param {string} settingName - The name of the setting to update.
 * @param {number|string} settingValue - The new value of the setting.
 */
function updateSetting(settingName, settingValue) {
  socket.emit('update_setting', { name: settingName, value: settingValue });
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
