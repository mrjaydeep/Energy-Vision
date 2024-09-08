document.getElementById('weatherForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    // Function to check if a string is a valid floating point number
    function isValidFloat(str) {
      return /^\d*\.?\d*$/.test(str);
    }
  
    // Retrieve input values and validate them
    var pressure = document.getElementById('pressure').value;
    var globalRadiation = document.getElementById('globalRadiation').value;
    var tempMean = document.getElementById('tempMean').value;
    var tempMin = document.getElementById('tempMin').value;
    var tempMax = document.getElementById('tempMax').value;
    var windSpeed = document.getElementById('windSpeed').value;
    var windBearing = document.getElementById('windBearing').value;
  
    // Check if inputs are valid floating point numbers
    if (!isValidFloat(pressure) || !isValidFloat(globalRadiation) || !isValidFloat(tempMean) || !isValidFloat(tempMin) || !isValidFloat(tempMax) || !isValidFloat(windSpeed) || !isValidFloat(windBearing)) {
      alert('Please enter valid floating point numbers.');
      return;
    }
  
    // Do something with the values (e.g., send them to a server, process them locally, etc.)
    console.log("Pressure:", parseFloat(pressure));
    console.log("Global Radiation:", parseFloat(globalRadiation));
    console.log("Mean Temperature:", parseFloat(tempMean));
    console.log("Minimum Temperature:", parseFloat(tempMin));
    console.log("Maximum Temperature:", parseFloat(tempMax));
    console.log("Wind Speed:", parseFloat(windSpeed));
    console.log("Wind Bearing:", parseFloat(windBearing));
  
    // You can also reset the form if needed
    // event.target.reset();
  });
  