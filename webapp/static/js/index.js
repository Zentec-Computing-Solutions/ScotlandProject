function updateBrightness(value) {
    fetch(`/set_brightness?value=${value}`);
}

function power(value) {
    fetch(`/power?value=${value}`);
}

function updateGain(value) {
    fetch(`/set_gain?value=${value}`);
}

var slider = document.getElementById("brightnessSlider");
let brightnessDebounceTimer;
slider.oninput = function () {
    clearTimeout(debounceTimer);
    brightnessDebounceTimer = setTimeout(() => {
        updateBrightness(this.value);
    }, 50); // 200ms delay
};

var slider = document.getElementById("gainSlider");
let gainDebounceTimer;
slider.oninput = function () {
    clearTimeout(debounceTimer);
    gainDebounceTimer = setTimeout(() => {
        updateBrightness(this.value);
    }, 50); // 200ms delay
};
