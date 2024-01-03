var map = L.map('homemap1').setView([6.5244, 3.3792], 13); // Default to Lagos
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Create a custom icon
var smallIcon = new L.Icon({
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-icon.png',
    iconSize: [25, 41], // size of the icon
});

document.addEventListener('DOMContentLoaded', function() {
    const index_page_city_select = document.getElementById('area-select-search');
    const index_page_state_select = document.getElementById('state-select-search');
    var markers = []; // to store all markers

    index_page_state_select.addEventListener('change', function() {
        const stateName = index_page_state_select.value;

        // Remove all options except the first one
        while (index_page_city_select.options.length > 1) {
            index_page_city_select.remove(1);
        }

        fetch('/load-town-city?state=' + encodeURIComponent(stateName))
            .then(response => {
                if (!response.ok) {
                    throw new Error("HTTP error " + response.status);
                }
                // index_page_city_select.value = '';         
                return response.json();
            })
            .then(townsCities => {

                townsCities.towns_cities.forEach(townCity => {
                    const option = document.createElement('option');
                    option.value = townCity.name;
                    option.text = townCity.name;
                    index_page_city_select.appendChild(option);
                });
                index_page_city_select.dispatchEvent(new Event('change'));
            })
            .catch(function(error) {
                console.error('Error:', error);
            });
    });    

    index_page_city_select.addEventListener('change', function() {
        const townCityName = index_page_city_select.value;
        const stateName = index_page_state_select.value;

        // Clear existing markers
        markers.forEach(marker => map.removeLayer(marker));
        markers = [];

        fetch(`/check_for_masons?state=${stateName}`)
            .then(response=> response.json())
            .then(data => {
                let masonInState = data.mason_in_state;
                let statesWithMasons = data.states_with_masons;
                if (masonInState != true)
                {
                    if (statesWithMasons.length == 1)
                    {
                        alert(`There are no masons in ${stateName}  only ${statesWithMasons.join(' ')}   state has masons for now`)
                    }

                    else if (statesWithMasons.length > 1)
                    {
                        alert(`There are no masons in ${stateName}, list of states with masons are ${statesWithMasons.join(', ')}`)
                    }

                    else 
                    {
                        alert(`Register now to be our first Mason!`)
                    }
                }

                else
                {
                    fetch(`/get-location?state=${stateName}&town_city=${townCityName}`)
                    .then(response => response.json())
                    .then(location => {
                    if (location && location.latitude && location.longitude) {
                            map.setView([location.latitude, location.longitude], 14); // Zoom level adjusted to 14
                        }
                    })
                    .then (
                        fetch(`/get-people?state=${stateName}&town_city=${townCityName}`)
                        .then(response => response.json())
                        .then(people => {
                            people.forEach(person => {
                                var marker = L.marker([person.latitude, person.longitude], {icon: smallIcon}).addTo(map);
                                markers.push(marker); // add the marker to the array
                                var personName = `${person.firstname} ${person.lastname}`;
                                var personInfo = `<strong>Contact:</strong>: ${person.phone_number}. <br> <strong>Email</strong> ${person.email}. <br> <strong>Services:</strong> ${person.service_name}`;
                                marker.bindPopup(`<b>${personName}</b><br>${personInfo}`).openPopup();
                        })})
                    )
                    .catch((error) => {
                        console.error('Error:', error);
                    })               
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                }
            })

        
});
});
