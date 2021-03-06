// Need: address (comes from server, DB, attached to user_profile, if already need to send
// this, may as well API call in python, geocode, and then send to JS )
// want to display map on JS

mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlbmVhbCIsImEiOiJjamRqdXdkd3UxMzB2MndvNmkwbGIzZmllIn0.xVy7VGtquOc7rUUpRz-KaQ';

var destinationsMap = new mapboxgl.Map({
    container: 'destinationsMap',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: addressLonLat,
    zoom: 12
});

// want markers 
// var geocoderControl = L.mapbox.geocoderControl('mapbox.places');

// var destinationMarkers = map.featureLayer;
// var features = []

// var geoObject = {
//     type: "FeatureCollection",
//     features: features
// };
// ajax call as soon as page loads on pageload 
// store on page and fetch from there in json, json dumps, include on the html page
// hidden (likely be faster than ajax)

// marker mill below
for (coordinates of destinationLngLats) {
    var marker = new mapboxgl.Marker()
        .setLngLat(coordinates)
        .addTo(destinationsMap);
}

// make sure to add all pins onto ONE feature layer (they don't need their own)

// establish feature  map.featurelayer
// build array for features []
// geoObject = {type; "FeatureCollection",
    // features: features (2nd features is our features array)}
// one pin is 1 geoJSON, push to array, call featurelayer.setGeoJSON
// then .setGeoJSON(geoObject)