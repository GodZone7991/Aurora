document.addEventListener('DOMContentLoaded', function() {
  const csvFile = document.getElementById('csvFile');
  const progressBar = document.getElementById('progressBar');
  const uploadMessage = document.getElementById('upload-message');

  csvFile.addEventListener('change', function() {
      const file = csvFile.files[0];
      if (file) {
          uploadMessage.innerText = `File: ${file.name} is uploaded`;
          uploadMessage.classList.add('white-text'); // Add the white-text class to the uploadMessage element

      // Simulate file processing
      let progress = 0;
      const interval = setInterval(function() {
        progress += 10;
        progressBar.value = progress;
        
        if (progress >= 100) {
          clearInterval(interval);
          alert('File processing complete.');
        }
      }, 1000);
    }
  });
});

  