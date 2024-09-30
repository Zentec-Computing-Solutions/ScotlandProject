function updateBrightness(value) {
    fetch(`/set_brightness?value=${value}`);
}

function power(value) {
    fetch(`/power?value=${value}`);
}

function updateContrast(value) {
    fetch(`/set_contrast?value=${value}`);
}

var slider = document.getElementById("brightnessSlider");
let brightnessDebounceTimer;
slider.oninput = function () {
    clearTimeout(brightnessDebounceTimer);
    brightnessDebounceTimer = setTimeout(() => {
        updateBrightness(this.value);
    }, 50); // 200ms delay
};

var slider = document.getElementById("contrastSlider");
let contrastDebounceTimer;
slider.oninput = function () {
    clearTimeout(contrastDebounceTimer);
    contrastDebounceTimer = setTimeout(() => {
        updateContrast(this.value);
    }, 50); // 200ms delay
};
