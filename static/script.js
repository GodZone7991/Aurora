document.addEventListener('DOMContentLoaded', function() {
    const csvFile = document.getElementById('csvFile');
    const progressBar = document.getElementById('progressBar');
    
    csvFile.addEventListener('change', function() {
      const file = csvFile.files[0];
      if (file) {
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
  