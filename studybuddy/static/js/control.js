document.addEventListener('DOMContentLoaded', function () {
    //  disable text selection
    function disableTextSelection(event) {
        // Allow text selection for input fields, textareas, and buttons
        const target = event.target;
        if (
            target.tagName === 'INPUT' ||
            target.tagName === 'TEXTAREA' ||
            target.tagName === 'BUTTON' ||
            target.tagName === 'A' ||
            target.contentEditable === 'true'
        ) {
            return; // Allow default behavior for these elements
        }
        event.preventDefault(); // Prevent text selection for all other elements
    }

    // Disable text selection for modern browsers
    document.addEventListener('selectstart', disableTextSelection); // For IE
    document.addEventListener('mousedown', disableTextSelection);   // For other browsers

    // disable right-click context menu (except for input fields)
    document.addEventListener('contextmenu', function (event) {
        const target = event.target;
        if (
            target.tagName === 'INPUT' ||
            target.tagName === 'TEXTAREA' ||
            target.tagName === 'BUTTON' ||
            target.tagName === 'A'
        ) {
            return; // Allow right-click for these elements
        }
        event.preventDefault(); // Prevent the context menu from appearing
    });
});


//  only for the h1,h2,h3

// document.querySelectorAll('h1, h2, h3').forEach(function (element) {
//     element.addEventListener('selectstart', function (event) {
//         event.preventDefault();
//     });
//     element.addEventListener('mousedown', function (event) {
//         event.preventDefault();
//     });
// });


// // disable all tags 
// document.addEventListener('DOMContentLoaded', function () {
//     function disableTextSelection(event) {
//         event.preventDefault(); // Prevent default text selection behavior
//     }

//     // Disable text selection for modern browsers
//     document.addEventListener('selectstart', disableTextSelection); // For IE
//     document.addEventListener('mousedown', disableTextSelection);   // For other browsers

//     // disable right-click context menu
//     document.addEventListener('contextmenu', function (event) {
//         event.preventDefault(); // Prevent the context menu from appearing
//     });
// });
