     // Get the canvas element
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // Set up the WebSocket connection
    const socket = new WebSocket('ws://localhost:8080');

    // Set up event listeners for the button and canvas
    document.getElementById('start-processing').addEventListener('click', () => {
      // Send a message to the server to start processing
      socket.send('{"type": "start"}');
    });

    canvas.addEventListener('mousedown', (event) => {
      // Start sending mouse position updates to the server
      sendMousePosition(event.clientX, event.clientY);
    });

    canvas.addEventListener('mousemove', (event) => {
      // Send updated mouse position to the server
      sendMousePosition(event.clientX, event.clientY);
    });

    canvas.addEventListener('touchstart', (event) => {
      // Start sending touch position updates to the server
      sendTouchPosition(event.touches[0].clientX, event.touches[0].clientY);
    });

    canvas.addEventListener('touchmove', (event) => {
      // Send updated touch position to the server
      sendTouchPosition(event.touches[0].clientX, event.touches[0].clientY);
    });

    // Function to send mouse or touch position updates to the server
    function sendPosition(x, y) {
      socket.send(`{"type": "position", "x": ${x}, "y": ${y}}`);
    }

    // Function to draw the processed image on the canvas
    function drawImage(data) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(data, 0, 0);
    }

    // Function to process the received data and update the canvas
    function processImage(data) {
      // Process the received data (e.g. apply filters, transformations)
      const processedData = data.filter((pixel) => {
        // Apply filter logic here
        return pixel;
      });

      // Draw the processed image on the canvas
      drawImage(processedData);
    }

    // Set up event listener for incoming data from the server
    socket.onmessage = (event => {
      // Process the received data and update the canvas
      processImage(JSON.parse(event.data));
    });
