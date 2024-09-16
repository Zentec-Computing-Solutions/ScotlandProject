let settings = {
    'flip_video': false,
    // Add more settings here as needed
};

document.getElementById('flip-button').addEventListener('click', function() {
    settings.flip_video = !settings.flip_video;  // Toggle the flip_video setting
    fetch('/update_settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)  // Send the settings as JSON data in the POST request
    });
});

// Add more event listeners here for other buttons, sliders, checkboxes, etc.