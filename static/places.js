

$(".add-to-list").click(function(evt) {
    let status = $(this).data("status");
    let yelpId = $(this).data("yelp-id");
    let address = $(this).data("address");
    let latitude = $(this).data("latitude");
    let longitude = $(this).data("longitude");
    let pic = $(this).data("pic");
    let url = $(this).data("url");

// the below payload is everything we need to instantiate a location
    let payload = {"status": status,
                   "yelp-id": yelpId,
                   "address": address,
                   "latitude": latitude,
                   "longitude": longitude,
                   "pic": pic,
                   "url": url,
               };

    $.post("/add-to-list", payload, function (results) {

    });


});


//give visual indicator that user has clicked button

function toggle_btn {

}

$('interested').on('click', toggle_btn)