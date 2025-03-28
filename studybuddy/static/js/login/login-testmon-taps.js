document.addEventListener("DOMContentLoaded", function () {
  const tabButtons = document.querySelectorAll(".tab-button");
  const tabContents = document.querySelectorAll(".tab-content");

  function switchTab(targetTabId) {
    if (!targetTabId) return;

    // Hide all tab contents
    tabContents.forEach((content) => {
      content.style.display = "none";
      content.classList.remove("active");
    });

    // Remove active state from all buttons
    tabButtons.forEach((button) => button.classList.remove("active"));

    // Show the selected tab
    const selectedTab = document.getElementById(targetTabId);
    const selectedButton = document.querySelector(
      `[data-tab="${targetTabId}"]`
    );

    if (selectedTab && selectedButton) {
      selectedButton.classList.add("active");
      selectedTab.style.display = "block";
      setTimeout(() => selectedTab.classList.add("active"), 10);
    }
  }

  // Attach event listeners to tab buttons
  tabButtons.forEach((button) => {
    button.addEventListener("click", function () {
      switchTab(this.getAttribute("data-tab"));
    });
  });

  // Initialize first tab as active
  if (tabButtons.length > 0) {
    switchTab(tabButtons[0].getAttribute("data-tab"));
  }
});
