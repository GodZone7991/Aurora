console.log("JavaScript loaded");

let pollingInterval; // Declare variable for storing the interval ID
let questionCount = 1; // Initialize question count

document.addEventListener('DOMContentLoaded', function() {
  const csvFile = document.getElementById('csvFile');
  const progressBar = document.getElementById('progressBar');
  const uploadMessage = document.getElementById('upload-message');
  const addQuestionButton = document.getElementById('add-question');
  const removeQuestionButton = document.getElementById('remove-question');

  // Initially hide the progress bar
  progressBar.style.display = 'none';

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

  // Add event listener to "Question+1" button
  addQuestionButton.addEventListener('click', function() {
    questionCount++;
    const inputSection = document.getElementById('input-section');
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = `question${questionCount}`;
    newInput.placeholder = 'Drop Here';
    inputSection.appendChild(newInput);
  });

  // Add event listener to "Remove Question" button
  removeQuestionButton.addEventListener('click', function() {
    if (questionCount > 1) { // Don't remove the first question
      const inputSection = document.getElementById('input-section');
      inputSection.removeChild(inputSection.lastChild);
      questionCount--;
    }
  });

  // Start polling when form is submitted
  document.querySelector('form').addEventListener('submit', function() {
    progressBar.style.display = 'block'; // Show the progress bar
    pollingInterval = setInterval(updateProgress, 1000); // Set the interval and store the ID
  });
});
