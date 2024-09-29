function updateBrightness(value) {
    fetch(`/set_brightness?value=${value}`);
}

function power(value) {
    fetch(`/power?value=${value}`);
}

var slider = document.getElementById("brightnessSlider");
let debounceTimer;
slider.oninput = function () {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        updateBrightness(this.value);
    }, 50); // 200ms delay
};
