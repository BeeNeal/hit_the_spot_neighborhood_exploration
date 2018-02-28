$( document ).ready(function() {
mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlbmVhbCIsImEiOiJjamRqdXdkd3UxMzB2MndvNmkwbGIzZmllIn0.xVy7VGtquOc7rUUpRz-KaQ';


var meetupMap = new mapboxgl.Map({
    container: 'meetupMap',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: mC,
    zoom: 15
});


console.log($("#LonLat").data('center'));

// what I need to do here - 
// 2) make a 'Feature' object that duplicates below feature

// 
// marker mill - getting coordinates from coded hidden divs 
let markerList = [];

$('.location').each(function(i, obj) {

    uniqueMarker = {
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: [
                  obj.dataset.lat,
                  obj.dataset.lon,
                ]
            },
            properties: {
                // 'title': obj.dataset.name,
                'marker-symbol': 'pitch',
                'marker-size': 'large',
                'marker-color': '#FF0066',
            }
        };

    // x.push(obj);
    markerList.push(uniqueMarker);
    // console.log(obj['dataset']['lat'])
});

var geojson = {
  type: 'FeatureCollection',
  features: []
};
geojson.features = markerList;
console.log(geojson);


// $(".location").each(function(i, obj) {
//   x.push(mObj)
// });

//   var mObj = {'lon': $(this).data('lon'), 'lat': $(this).data('lat')}
// console.log(mObj)

  // var coords = ['$(this).data('lon')', '$(this).data('lat')'];
  //   var m1 = {
  //       coordinates: coords,
  //       name: $(this).data('name');
  //   };
  //   markerList.push(m1)


 // let x = [$(".location").each]
// var features = [];

//     for (var i=0; i< x.length; i++){
//         var uniqueLocation = x[i];
//         uniqueMarker = {
//             type: 'Feature',
//             geometry: {
//                 type: 'Point',
//                 coordinates: [
//                   uniqueLocation.lat,
//                   uniqueLocation.lon
//                 ]
//             },
//             properties: {
//                 title: uniqueLocation.address,
//                 'marker-symbol': 'pitch',
//                 'marker-size': 'large',
//                 'marker-color': '#FF0066',
//             }
        // };
    //     features.push(uniqueMarker);
    // }





    // ['lon': '$(this).data('lon')', 'lat': '$(this).data('lat')']
console.log(markerList)

    // console.log($(this).data('lon'));
// need to loop through the above list of lat lons and make new features with these

// geojson = []

var geojson = {
  type: 'FeatureCollection',
  features: [{
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates: [-122.411981039, 37.8013699309]
    },
    properties: {
      title: 'Test',
      description: 'Test'
    }
  },
  {
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates: [-122.414, 37.776]
    },
    properties: {
      title: 'Mapbox',
      description: 'San Francisco, California'
    }
  }]
};

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