// Need: address (comes from server, DB, attached to user_profile, if already need to send
// this, may as well API call in python, geocode, and then send to JS )
// want to display map on JS

mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlbmVhbCIsImEiOiJjamRqdXdkd3UxMzB2MndvNmkwbGIzZmllIn0.xVy7VGtquOc7rUUpRz-KaQ';

// base map that gets put on every page, will have separate markers that correspond to each pg
// will want center to be address lon/lat
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: [-122.411386, 37.788878],
    zoom: 15
});

// need marker mill here:

// can I do 
var markera = new mapboxgl.Marker()
  .setLngLat([-122.41138, 37.78887])
  .addTo(map);

// let testPin = mapboxgl.featureLayer({
//     type: 'Feature',
//     geometry: {
//         type: 'Point',
//         coordinates: [-122.411386, 37.788878]
//     },

//     properties: {
//         title: 'You',
//         description: 'Latitude: ' + -122.411380 + 'Longitude: ' + 37.788870,
//         'marker-symbol': 'star-stroked',
//         'marker-size': 'large',
//         'marker-color': '#2EB8B8',
//     }
// });