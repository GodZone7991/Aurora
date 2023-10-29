console.log("JavaScript loaded");

let pollingInterval; // Declare variable for storing the interval ID

document.addEventListener('DOMContentLoaded', function() {
  const csvFile = document.getElementById('csvFile');
  const progressBar = document.getElementById('progressBar');
  const uploadMessage = document.getElementById('upload-message');

  csvFile.addEventListener('change', function() {
    const file = csvFile.files[0];
    if (file) {
      uploadMessage.innerText = `File: ${file.name} is uploaded`;
      uploadMessage.classList.add('white-text');
    }
  });

  // Function to update progress by polling the server
  function updateProgress() {
    // Use jQuery to make the AJAX request
    $.get('/progress', function(data) {
      progressBar.value = data.progress;

      if (data.progress >= 100) {
        alert('File processing complete.');
        clearInterval(pollingInterval); // Stop the polling when progress is 100%
      }
    });
  }

  document.querySelector('form').addEventListener('submit', function() {
    progressBar.style.display = 'block'; // Show the progress bar
    pollingInterval = setInterval(updateProgress, 1000); // Set the interval and store the ID
  });
});
