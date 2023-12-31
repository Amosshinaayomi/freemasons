document.addEventListener('DOMContentLoaded', function() {

    const state_select = document.getElementById('state-select');
    const areaselect = document.getElementById('area-select');
    
    state_select.addEventListener('change', function() {
        console.log('got here')
        const stateName = state_select.value;
        fetch('/load-town-city?state=' + encodeURIComponent(stateName))
            .then(response => {
                if (!response.ok) {
                    throw new Error("HTTP error " + response.status);
                }
                return response.json();
            })
            .then(townsCities => {
                console.log(townsCities);  // Log the towns and cities to the console
    
                // Clear the select field
                areaselect.innerHTML = '';
                
                // Populate the select field with the names of the towns and cities
                townsCities.towns_cities.forEach(townCity => {
                    const option = document.createElement('option');
                    option.value = townCity.name;
                    option.text = townCity.name;
                    areaselect.appendChild(option);
                });
            });
    });
    

});