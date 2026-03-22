// Import the express module
const express = require('express');

// Create an Express application
const app = express();

// Read port from environment variable or command line argument
const PORT = process.env.PORT || process.argv[2] || 3000;

// Middleware to parse JSON requests
app.use(express.json());

// Define a simple route
app.get('/', (req, res) => {
  res.send('Hello, World! This is a sample Node.js app.');
});

// Example POST route
app.post('/data', (req, res) => {
  const userData = req.body;
  res.json({
    message: 'Data received successfully!',
    data: userData
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
