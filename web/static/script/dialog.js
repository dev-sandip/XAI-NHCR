
const canvas = document.getElementById('drawing-board');


// Get the 2D rendering context of the canvas
var ctx = canvas.getContext('2d');

// Initialize variables to track pointer movements
var isDrawing = false;
var lastX = 0;
var lastY = 0;

// Event listener to track pointer movements and draw lines
canvas.addEventListener('pointerdown', function (e) {
    isDrawing = true;
    [lastX, lastY] = [e.offsetX, e.offsetY];
});

canvas.addEventListener('pointermove', function (e) {
    if (isDrawing) {
        var x = e.offsetX;
        var y = e.offsetY;
        drawLine(lastX, lastY, x, y);
        lastX = x;
        lastY = y;
    }
});

canvas.addEventListener('pointerup', function () {
    isDrawing = false;
});

canvas.addEventListener('pointerout', function () {
    isDrawing = false;
});

// Function to draw lines on the canvas
function drawLine(startX, startY, endX, endY) {
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = '#000'; // Color of the line
    ctx.lineWidth = 2; // Thickness of the line
    ctx.stroke();
    ctx.closePath();
}



function showDialog() {

    const modal = document.getElementById("dialog-area")
    const overlay = document.getElementById("overlay");


    const canvas = document.getElementById("drawing-board");
    const ctx = canvas.getContext('2d');



    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    modal.style.display = 'flex';
    overlay.style.display = 'block';

}



function closeDialog() {
    const modal = document.getElementById("dialog-area");
    const overlay = document.getElementById("overlay");

    const canvas = document.getElementById("drawing-board");
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    modal.style.display = 'none';
    overlay.style.display = 'none';

}


function clearCanvas() {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}