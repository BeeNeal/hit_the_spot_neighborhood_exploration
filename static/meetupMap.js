$( document ).ready(function() {
mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlbmVhbCIsImEiOiJjamRqdXdkd3UxMzB2MndvNmkwbGIzZmllIn0.xVy7VGtquOc7rUUpRz-KaQ';


var meetupMap = new mapboxgl.Map({
    container: 'meetupMap',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: mC,
    zoom: 15
});


console.log($("#LonLat").data('center'));

// marker mill - getting coordinates from coded hidden divs 
let markerList = [];

$('.location').each(function(i, obj) {

    uniqueMarker = {
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: [
                  obj.dataset.lon,
                  obj.dataset.lat,
                ]
            },
            properties: {
                // 'title': obj.dataset.name,
                'marker-symbol': 'pitch',
                'marker-size': 'large',
                'marker-color': '#FF0066',
            }
        };

    markerList.push(uniqueMarker);
});

var geojson = {
  type: 'FeatureCollection',
  features: []
};
geojson.features = markerList;
console.log(geojson);

// add markers to map
geojson.features.forEach(function(marker) {
    console.log('marker:', marker);

  // create a HTML element for each feature
  var el = document.createElement('div');
  el.className = 'marker';

  // make a marker for each feature and add to the map
  let m = new mapboxgl.Marker(el)
  .setLngLat(marker.geometry.coordinates)
  .addTo(meetupMap);

});

//the below }) ends the .ready function which ensures loading order 
});