var map = L.map('map').setView([6.5244, 3.3792], 13); // Default to Lagos
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
// Initialize a variable to store the marker
var marker;
// Listen for click events on the map
map.on('click', function(e) {
    // Get the latitude and longitude of the clicked location
    var lat = e.latlng.lat;
    var lon = e.latlng.lng;
    // If a marker already exists, remove it
    if (marker) {
        map.removeLayer(marker);
    }
    // Create a new marker at the clicked location
    marker = L.marker([lat, lon]);

    // Add the marker to the map
    marker.addTo(map);

});


document.addEventListener('DOMContentLoaded', function() {

    const cityStateDiv = document.querySelector('.citystate');
    const [user_city, user_state] = cityStateDiv.textContent.split(', ');
    fetch(`/get-location?state=${user_state}&town_city=${user_city}`)
        .then(response => response.json())
        .then(location => {
            if (location && location.latitude && location.longitude) {
                var map = L.map('map').setView([location.latitude, location.longitude], 18);
                map.invalidateSize();
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(map);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    
    const profile_page_city_select = document.querySelector('.profile-select-towns');
    const profile_page_state_select = document.querySelector('.profile-select-state');
    const state_select = document.getElementById('state-select');
    const areaselect = document.getElementById('area-select');
    profile_page_state_select.addEventListener('change', function() {
        console.log('got here')
        const stateName = profile_page_state_select.value;

        // Clear the city select field
        profile_page_city_select.innerHTML = '';

        fetch('/load-town-city?state=' + encodeURIComponent(stateName))
            .then(response => {
                if (!response.ok) {
                    throw new Error("HTTP error " + response.status);
                }
                return response.json();
                console.log('here too')
            })
            .then(townsCities => {
                // Populate the select field with the names of the towns and cities
                townsCities.towns_cities.forEach(townCity => {
                    const option = document.createElement('option');
                    option.value = townCity.name;
                    option.text = townCity.name;
                    profile_page_city_select.appendChild(option);
                });
                // Trigger the change event for the city select input
                profile_page_city_select.dispatchEvent(new Event('change'));
            })
            .catch(function(error) {
                console.error('Error:', error);  // Log any errors to the console
            });
    });    

    profile_page_city_select.addEventListener('change', function() {
        const townCityName = profile_page_city_select.value;
        const stateName = profile_page_state_select.value; // assuming you have a state select input

        fetch(`/get-location?state=${stateName}&town_city=${townCityName}`)
            .then(response => response.json())
            .then(location => {
                if (location && location.latitude && location.longitude) {
                    map.setView([location.latitude, location.longitude], 10);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    state_select.addEventListener('change', function() {
        console.log('got here')
        const stateName = state_select.value;

        // Clear the area select field
        areaselect.innerHTML = '';

        fetch('/load-town-city?state=' + encodeURIComponent(stateName))
            .then(response => {
                if (!response.ok) {
                    throw new Error("HTTP error " + response.status);
                }
                return response.json();
            })
            .then(townsCities => {
                console.log(townsCities);  // Log the towns and cities to the console
                
                // Populate the select field with the names of the towns and cities
                townsCities.towns_cities.forEach(townCity => {
                    const option = document.createElement('option');
                    option.value = townCity.name;
                    option.text = townCity.name;
                    areaselect.appendChild(option);
                });
            })
            .catch(function(error) {
                console.error('Error:', error);
            });
    });
});
