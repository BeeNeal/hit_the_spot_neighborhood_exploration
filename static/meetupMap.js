$( document ).ready(function() {
mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlbmVhbCIsImEiOiJjamRqdXdkd3UxMzB2MndvNmkwbGIzZmllIn0.xVy7VGtquOc7rUUpRz-KaQ';


var meetupMap = new mapboxgl.Map({
    container: 'meetupMap',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: mC,
    zoom: 15
});

console.log($("#LonLat").data('center'));

$(".location").each(function() {
    console.log($(this).data('lat'));
    console.log($(this).data('lon'));
    console.log($(this).data('name'));
});




//the below }) end the .ready function which ensures loading order 
});