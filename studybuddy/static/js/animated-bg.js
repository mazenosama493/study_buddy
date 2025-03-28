document.addEventListener("DOMContentLoaded", function () {
  const background = document.querySelector(".background-animate");

  // Clear existing animations
  background.innerHTML = "";

  // Icons array using the passed static URLs
  const icons = [
    { src: ICONS.book, alt: "Book" },
    { src: ICONS.boook, alt: "Boook" },
    { src: ICONS.map, alt: "map" },
    { src: ICONS.maap, alt: "map" },
    { src: ICONS.pen, alt: "Pen" },
    { src: ICONS.glasses, alt: "Glasses" },
  ];

  // Color palette
  const colors = ["#A9C9B4", "#6E91A5", "#A3C6DC", "#8ABEB7", "#5F8392"];

  // Function to create a flying item
  function createFlyingItem(icon, top, left, delay, directionX, directionY) {
    const div = document.createElement("div");
    div.classList.add("flying-item");

    const img = document.createElement("img");
    img.src = icon.src;
    img.alt = icon.alt;
    img.classList.add("icon");

    const size = Math.random() * (60 - 20) + 20; // Random size between 20px and 60px
    img.style.width = `${size}px`;
    img.style.height = `${size}px`;
    // console.log(size);

    // Random color from the palette
    img.style.filter = `drop-shadow(0 0 10px ${
      colors[Math.floor(Math.random() * colors.length)]
    })`;

    div.appendChild(img);

    // Random position
    div.style.top = `${top}%`;
    div.style.left = `${left}%`;

    // Random animation properties
    div.style.animationDelay = `${delay}s`;
    div.style.animationDuration = `${Math.random() * 10 + 10}s`;
    div.style.animationName = directionX > 0 ? "float-right" : "float-left";

    background.appendChild(div);
  }

  // Generate multiple flying items
  const numberOfItems = Math.floor(Math.random() * (25 - 15 + 1)) + 15; // Random number of items (15 to 25)
  for (let i = 0; i < numberOfItems; i++) {
    const randomIcon = icons[Math.floor(Math.random() * icons.length)];
    const randomTop = Math.random() * 80 + 10; // Random top position between 10% and 90%
    const randomLeft = Math.random() * 100; // Random left position between 0% and 100%
    const randomDelay = Math.random() * 5; // Random delay up to 5 seconds
    const randomDirectionX = Math.random() > 0.5 ? 1 : -1; // Random horizontal direction
    const randomDirectionY = Math.random() > 0.5 ? 1 : -1; // Random vertical direction

    createFlyingItem(
      randomIcon,
      randomTop,
      randomLeft,
      randomDelay,
      randomDirectionX,
      randomDirectionY
    );
  }
  // Mouse shadow effect
  // function initMouseShadow(containerSelectors = []) {
  //   const mouseShadow = document.createElement("div");
  //   mouseShadow.classList.add("mouse-shadow");
  //   document.body.appendChild(mouseShadow);

  //   // Track scroll position explicitly
  //   let lastScrollY = window.scrollY;

  //   // Update shadow position on both mousemove and scroll events
  //   const updateShadowPosition = (event) => {
  //     const { clientX, pageY } = event; // Use pageY for vertical positioning

  //     // Check if the mouse is inside any excluded containers
  //     let shouldShowShadow = true;
  //     if (containerSelectors.length > 0) {
  //       shouldShowShadow = !containerSelectors.some((selector) => {
  //         const container = document.querySelector(selector);
  //         if (container) {
  //           const containerRect = container.getBoundingClientRect();
  //           return (
  //             clientX > containerRect.left &&
  //             clientX < containerRect.right &&
  //             event.clientY > containerRect.top && // Use clientY here for viewport-relative checks
  //             event.clientY < containerRect.bottom
  //           );
  //         }
  //         return false;
  //       });
  //     }

  //     // Update shadow visibility and position
  //     mouseShadow.style.opacity = shouldShowShadow ? "1" : "0";
  //     mouseShadow.style.left = `${clientX}px`;
  //     mouseShadow.style.top = `${pageY}px`; // Use pageY for accurate positioning
  //   };

  //   // Attach event listeners
  //   document.addEventListener("mousemove", updateShadowPosition);
  //   window.addEventListener("scroll", () => {
  //     lastScrollY = window.scrollY; // Update scroll position
  //     updateShadowPosition({
  //       clientX: mouseShadow.offsetLeft,
  //       pageY: mouseShadow.offsetTop + lastScrollY,
  //     });
  //   });
  // }

  // // Initialize mouse shadow with different containers
  // initMouseShadow([".login-container", ".tab-content", ".comments-list"]);
});
