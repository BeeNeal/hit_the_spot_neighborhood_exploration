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

// draw circle
var myCircle = new MapboxCircle({lat: mC[1], lng: mC[0]}, 1200, {
        editable: true,
        minRadius: 1500,
        // fillColor: '#29AB87'
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