mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlbmVhbCIsImEiOiJjamRqdXdkd3UxMzB2MndvNmkwbGIzZmllIn0.xVy7VGtquOc7rUUpRz-KaQ';


var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: [-122.411386, 37.788878],
    zoom: 15
});

for (coordinates of visitedLngLats) {
    var marker = new mapboxgl.Marker()
        .setLngLat(coordinates)
        .addTo(map);
}
