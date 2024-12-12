// Create an array to store the cursor trail elements
const trail = [];
const trailLength = 10; // Shortened trail length for a more compact trail
let currentHue = 0; // Starting hue value for the gradient

// Function to create new cursor trail
function createTrail(x, y) {
    const trailElement = document.createElement('div');
    trailElement.classList.add('cursor-trail');
    document.body.appendChild(trailElement);
    trail.push(trailElement);

    // Set initial position, accounting for the scroll position
    trailElement.style.left = `${x - 5}px`; // Centering the cursor element (smaller)
    trailElement.style.top = `${y - 5}px`;

    // Set initial size and color for the trail element, using the current hue
    trailElement.style.width = '10px'; // Smaller initial size
    trailElement.style.height = '10px'; // Smaller initial size
    trailElement.style.backgroundColor = `hsl(${currentHue}, 100%, 50%)`;

    // Increment the hue for the next circle to create a smooth gradient effect
    currentHue = (currentHue + 2) % 360; // Smaller increments for smoother gradient effect

    // Set the opacity to 1 for the trail
    trailElement.style.opacity = 1;

    // Gradually shrink and fade the trail elements over time
    setTimeout(() => {
        trailElement.style.opacity = 0; // Fade out the circle
        trailElement.style.transform = 'scale(0.5)'; // Shrink the circle
        trailElement.style.width = '5px'; // Gradually reduce size
        trailElement.style.height = '5px'; // Gradually reduce size
    }, 100); // Shrink and fade after a brief moment

    // Remove old trail elements once they have faded out
    if (trail.length > trailLength) {
        const oldElement = trail.shift();
        oldElement.remove();
    }
}

// Event listener for mouse movement
document.addEventListener('mousemove', (e) => {
    const x = e.pageX; // Use pageX to account for scroll position
    const y = e.pageY; // Use pageY to account for scroll position

    // Create a new trail at the mouse position
    createTrail(x, y);
});
