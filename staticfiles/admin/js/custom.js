document.addEventListener("DOMContentLoaded", function () {
    const toggleSwitch = document.getElementById("darkModeToggle");
    const modeText = document.getElementById("modeText");

    // Check local storage for the user's preference
    const isDarkMode = localStorage.getItem("darkMode") === "enabled";
    if (isDarkMode) {
        enableDarkMode();
        toggleSwitch.checked = true;
    }

    // Event listener for toggle switch
    toggleSwitch.addEventListener("change", function () {
        if (this.checked) {
            enableDarkMode();
        } else {
            disableDarkMode();
        }
    });

    // Enable dark mode
    function enableDarkMode() {
        document.body.classList.add("dark-mode");
        modeText.textContent = "Light Mode";
        localStorage.setItem("darkMode", "enabled");
    }

    // Disable dark mode
    function disableDarkMode() {
        document.body.classList.remove("dark-mode");
        modeText.textContent = "Dark Mode";
        localStorage.setItem("darkMode", null);
    }
});