// Problems on this page - 1) Jquery not working 2) Toggle only works on first button

// let buttons = document.querySelectorAll(".addToList");
// let buttons = document.querySelectorAll(".addToList");
// 
    $(".addToList").on('click', function(evt) {
    let status = $(this).data("status");
    let name = $(this).data("name");
    let address = $(this).data("address");
    let latitude = $(this).data("latitude");
    let longitude = $(this).data("longitude");
    let pic = $(this).data("pic");
    let url = $(this).data("url");
    let yelpId = $(this).data("id");

    // the below payload is all the data we need to instantiate a location
    let payload = {"status": status,
                   "name": name,
                   "yelp_id": yelpId,
                   "address": address,
                   "latitude": latitude,
                   "longitude": longitude,
                   "pic": pic,
                   "url": url,
               };


    // AJAX post to server and give visual indicator that user has clicked button
    //should get back status as results

    // use [][] to select specific buttons being changed
    $.post("/add-to-list", payload, function change_btn_color(results) {
      if (results.status === 'interested') {
        $(`button[data-id='${yelpId}'][data-status='interested']`)
          .css("backgroundColor", 'red')
          .css("color", "purple");
        }
      else if (results.status === 'visited') {
        $(`button[data-id='${yelpId}'][data-status='visited']`)
          .css("backgroundColor", 'red')
          .css("color", "purple");
      }

    });

});
// results here are what we got back from AJAX
         // if (results['status'] === 'interested') && () {
         //     console.log("inside interested");
         //     $('#interested').innerText='Interested';
         