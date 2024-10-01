function power(value) {
    if (confirm(`Your Pi is about to ${value}. Are you sure?`)) {
        fetch(`/power?value=${value}`);
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

function updateBrightness(value) {
    fetch(`/set_brightness?value=${value}`);
}
function updateContrast(value) {
    fetch(`/set_contrast?value=${value}`);
}

function updateSaturation(value) {
    fetch(`/set_saturation?value=${value}`);
}

function updateSharpness(value) {
    fetch(`/set_sharpness?value=${value}`);
}

function setupSliderInputPair(sliderId, inputId, updateFunction) {
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
            updateFunction(slider.value);
        }, 50);
    }

    input.oninput = handleInputChange;
    slider.oninput = function () {
        input.value = this.value;
        handleInputChange();
    };
}

setupSliderInputPair("brightnessSlider", "brightnessInput", updateBrightness);
setupSliderInputPair("contrastSlider", "contrastInput", updateContrast);
setupSliderInputPair("saturationSlider", "saturationInput", updateSaturation);
setupSliderInputPair("sharpnessSlider", "sharpnessInput", updateSharpness);
