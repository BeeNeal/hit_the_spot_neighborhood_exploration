
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

// function btnVisFeedback(results) {
//   if (results.status === 'added') {
//     $(`#details-${yelp_id}`).css
//   }
// }

function checkLoginStatus(results) {
  
  let status = results['status'];
  let qAnswers = results['answer']
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
  else if (status === 'success' && qAnswers === true) {
        window.location="/explore";
      }
  else if (status === 'success' && qAnswers == false) {
        window.location='/questions';
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




