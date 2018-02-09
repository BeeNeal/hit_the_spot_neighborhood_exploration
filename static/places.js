
$(".addToList").click(function(evt) {
    let status = $(this).data("status");
    let address = $(this).data("address");
    let latitude = $(this).data("latitude");
    let longitude = $(this).data("longitude");
    let pic = $(this).data("pic");
    let url = $(this).data("url");
    let yelpId = $(this).data("yelpId");

	// the below payload is all the data we need to instantiate a location
    let payload = {"status": status,
                   "yelp_id": yelpId,
                   "address": address,
                   "latitude": latitude,
                   "longitude": longitude,
                   "pic": pic,
                   "url": url,
               };

	// AJAX post to server and give visual indicator that user has clicked button
    $.post("/add-to-list", payload, function toggle_btn(results) {
    	console.log("made it to toggle")
    	if ($('#interested').innerText==='I want to go!'){
			($('#interested').innerText='Interested')}

    	else {
    		console.log("inside visited")

    		$('visited').innerHTML='Visited'
    	}

    });

});
// results here are what we got back from AJAX
    	 // if (results['status'] === 'interested') && () {
    	 // 	console.log("inside interested");
    	 // 	$('#interested').innerText='Interested';
    	 
// tried:   $('.addToList').value='Interested';
    	 	// $('.addToList').innerHTML='Interested';
    	 	// $('#interested').innerHTML='Interested';
    	 	// $('#interested').value='Interested';
    	 	// $('#interested').innerText='Interested';
