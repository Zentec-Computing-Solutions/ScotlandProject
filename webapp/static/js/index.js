let settings = {
    flip_video: false,
    // Add more settings here as needed
};

document.getElementById("flip-button").addEventListener("click", function () {
    settings.flip_video = !settings.flip_video; // Toggle the flip_video setting
    fetch("/update_settings", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(settings), // Send the settings as JSON data in the POST request
    });
});
document.getElementById("save-image").addEventListener("click", function () {
    fetch("/save_image", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    });
});

// Add more event listeners here for other buttons, sliders, checkboxes, etc.
