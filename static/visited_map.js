mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlbmVhbCIsImEiOiJjamRqdXdkd3UxMzB2MndvNmkwbGIzZmllIn0.xVy7VGtquOc7rUUpRz-KaQ';


var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: addressLonLat,
    zoom: 12
});

for (coordinates of visitedLngLats) {
    var marker = new mapboxgl.Marker()
        .setLngLat(coordinates)
        .addTo(map);
}
