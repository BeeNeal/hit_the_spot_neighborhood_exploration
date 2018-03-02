

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
    // $.post("/add-to-list", payload, function change_btn_color(results) {
    //   if (results.status === 'interested') {
    //     $(`button[data-id='${yelpId}'][data-status='interested']`)
    //       .css("backgroundColor", 'red')
    //       .css("color", "purple");
    //     }
    //   else if (results.status === 'visited') {
    //     $(`button[data-id='${yelpId}'][data-status='visited']`)
    //       .css("backgroundColor", 'red')
    //       .css("color", "purple");
    //   }

    // });
    $.post("/add-to-list", payload, function change_btn_color(results) {
      if (results.status === 'interested') {
        $(`button[data-id='${yelpId}'][data-status='interested']`)
          .css("backgroundColor", 'red')
          .css("color", "purple");
        $(`button[data-id='${yelpId}'][data-status='visited']`)
          .css("backgroundColor", 'green')
          .css("color", "white");
        }
      else if (results.status === 'visited') {
        $(`button[data-id='${yelpId}'][data-status='visited']`)
          .css("backgroundColor", 'red')
          .css("color", "purple");
        $(`button[data-id='${yelpId}'][data-status='interested']`)
          .css("backgroundColor", 'green')
          .css("color", "white");
      }

    });
});
// results here are what we got back from AJAX
         // if (results['status'] === 'interested') && () {
         //     console.log("inside interested");
         //     $('#interested').innerText='Interested';
         
// $(window).load(function() {
//     $('#questionsModal').modal('show');
// });
// To handle Modal below
// function addQuestionData(evt) {
//   let answers = [];
//   answers.push($('#question1').val())
// }

// $("#question1").on('click', function(evt) {
function sendAnswers() {
  let answers = {
    'cuisine': responses[0],
    'hobby': responses[1],
    'outdoorsy': responses[2],
  };
  console.log(answers);

  $.post("/questions", answers);

    // function(){$('#q3modal').modal('hide');});
}
  var responses = [];

  function grabAnswers(evt) {
  responses.push($('.answers')[responses.length].value);

  if (responses.length === 3){
    sendAnswers();

  (function() {
    $('#modalwindow').modal('hide');
    window.location.replace("/");
    })();

  }
  }
