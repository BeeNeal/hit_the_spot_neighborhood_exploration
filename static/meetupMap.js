$( document ).ready(function() {
mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlbmVhbCIsImEiOiJjamRqdXdkd3UxMzB2MndvNmkwbGIzZmllIn0.xVy7VGtquOc7rUUpRz-KaQ';


var meetupMap = new mapboxgl.Map({
    container: 'meetupMap',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: mC,
    zoom: 12
});


// console.log($("#LonLat").data('center'));

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

// add markers to map
geojson.features.forEach(function(marker) {

  // create a HTML element for each feature
  var el = document.createElement('div');
  el.className = 'marker';

  // make a marker for each feature and add to the map
  let m = new mapboxgl.Marker(el)
  .setLngLat(marker.geometry.coordinates)
  .addTo(meetupMap);

});

// add address1, address2 markers

a1 = {
    type: 'Feature',
    geometry: {
        type: 'Point',
        coordinates: a1
    },
    properties: {
        // 'title': obj.dataset.name,
        'marker-symbol': 'pitch',
        'marker-size': 'large',
        'marker-color': '#FF0066',
    }
}; // closes a1 object

a2 = {
    type: 'Feature',
    geometry: {
        type: 'Point',
        coordinates: a2
    },
    properties: {
        // 'title': obj.dataset.name,
        'marker-symbol': 'pitch',
        'marker-size': 'large',
        'marker-color': '#FF0066',
    }
};

// let addressMarkers = [a1, a2];

var geojson2 = {
    type: 'FeatureCollection',
  features: [a1, a2]
};

// add markers to map
geojson2.features.forEach(function(marker) {

  // create a HTML element for each feature
  var el = document.createElement('div');
  el.className = 'addressMarker';

  // make a marker for each feature and add to the map
  let am = new mapboxgl.Marker(el)
  .setLngLat(marker.geometry.coordinates)
  .addTo(meetupMap);

});

// add meetup midpoint marker

var markerm = new mapboxgl.Marker()
    .setLngLat(mC)
    .addTo(meetupMap);

// draw circle
var myCircle = new MapboxCircle({lat: mC[1], lng: mC[0]}, searchRadius, {
        editable: true,
        minRadius: searchRadius,
        fillColor: '#29AB87'
    }).addTo(meetupMap);
 
myCircle.on('centerchanged', function (circleObj) {
        console.log('New center:', circleObj.getCenter());
    });
myCircle.once('radiuschanged', function (circleObj) {
        console.log('New radius (once!):', circleObj.getRadius());
    });
myCircle.on('click', function (mapMouseEvent) {
        console.log('Click:', mapMouseEvent.point);
    });
myCircle.on('contextmenu', function (mapMouseEvent) {
        console.log('Right-click:', mapMouseEvent.lngLat);
    });


//the below }) ends the .ready function which ensures loading order 
});