let modal = document.getElementById("myModal");
let btn = document.getElementById("myBtn");
let span = document.getElementsByClassName("close")[0];
let book = document.querySelector(".book-title");
let csrf = document.getElementsByName('csrfmiddlewaretoken')
let rateBtn = document.getElementById("rate-btn");
let removeRating = document.getElementById("rate-remove-btn");
let ratingStar = document.querySelectorAll('input[name="rating"]');

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

rateBtn.onclick = function() {
	for(var i = 0; i < ratingStar.length; i++){
	    if(ratingStar[i].checked){
	        fetch(`/book/rate/`, {
				method: 'POST',
				headers:{"X-CSRFToken": csrf[0].value},
				body: JSON.stringify({
					rating: ratingStar[i].value,
					book_id: book.dataset.id
				})

			})
			.then (response => response.json())
			.then (result => {
				if (result.success) {
					btn.innerHTML = "<span class='review-rating-user'>\
									 <i class='bi bi-star-fill'></i> "+result.score+
									 "<span class='max-rating'>/5</span></span>"

					modal.style.display = "none";
				}
				if (result.error == "login_required") {
					window.location.href = '/login'
				}
			})
	    }
	}
}

removeRating.onclick = function () {
	fetch(`/book/rate/`, {
		method: 'DELETE',
		headers:{"X-CSRFToken": csrf[0].value},
		body: JSON.stringify({
			book_id: book.dataset.id
		})

	})
	.then (response => response.json())
	.then (result => {
		console.log(result)
		btn.innerHTML = "<span class='review-rating'><i class='bi bi-star'></i> Rate</span></span>"
		modal.style.display = "none";

		if (result.error == "login_required") {
			window.location.href = '/login'
		}
	})
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}