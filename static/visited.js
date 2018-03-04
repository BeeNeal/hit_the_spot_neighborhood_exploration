
// $(".addDetails").on('click', function(evt) {
//     let yelpId = $(this).data('id');
//     let notes = $(this).data('notes');
//     let favorite = $(this).data('favorite');
//     // let rating = $(this).data('id');

//     let payload = {"yelp_id": yelpId,
//                    "notes": notes,
//                    "favorite": favorite,
//                    // "rating":rating
//                   };

// $.post("/add-notes", payload, (modalNotes)

// }
// // , function solidifyTextbox(results)
// function modalNotes() {

// }

// function addToVisitedList(yelp_id) {
//   let 
// }


function addDetailsOnClick(yelp_id) {
    
    let notes = $(`#notes-${yelp_id}`).val();
    let favorite = $(`#favorite-${yelp_id}`).val();
    // let rating = $(`#rating-${yelp_id}`.value())

    let payload = {"yelp_id": yelp_id,
                   "notes": notes,
                   "favorite": favorite,
                   // "rating":rating
                  };


// below updateNotesDiv is taking the response of the ajax call as the argument to the callback.
// see what the server is sending back in the response and parse it into the jquery
    $.post("/add-notes", payload, function updateNotesDiv(results) {
        $(`#div${yelp_id}`).removeClass('hidden').html;
        $(`#div${yelp_id}`).html(notes);
    });

}

function checkLoginStatus(results) {
  console.log("checkLoginStatus");
  let status = results['status'];
  let qAnswers = results['answer'];

  if (status === 'noUser') {
      (function displayNotification() {
        $('#notification').text('No user with these credentials - please try again');
      })()
  }
  else if (status === 'wrongPassword') {
    (function displayNotification() {
        $('#notification').text('Incorrect password - please try again');
     })()
  }
  else if (status === 'success' && qAnswers === true) {
    console.log("explore");
        window.location.replace("/explore");
      }
  else if (status === 'success' && qAnswers == false) {
    console.log("q");
        window.location.replace('/questions');
  };
}

function checkLoginData() {
  let id = $('#userInfo').val();
  let password = $('#userPassword').val();

  let userPayload = {"user_info": id,
                     "password": password
                    };

  $.post("/login", userPayload, checkLoginStatus);
}

function fillStar(yelp_id) {
  $(`#star${yelp_id}`)
}

// I want to change glyphicon color to gold, and fill, also send that info to 

