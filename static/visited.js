
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

    $.post("/add-notes", payload, alert(notes))
        // FIXME Need to change alert(notes) to do something else

}

function btnVisFeedback(results) {
  if (results.status === 'added')
}

function checkLoginStatus(results) {
  
  let status = results['status'];
  //  we know that this function is being activated, and status is what we expect
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
  else if (status === 'success') {
        window.location="/explore";
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

// why is results not coming through, when it's making it to server?
// 1) most likely a syntax error, most likely in JS

  // else if results === 'wrongPassword'


// }


