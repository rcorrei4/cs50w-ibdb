document.addEventListener('DOMContentLoaded' , function () {
	document.getElementById("want-read").onchange = function () {
		option = document.getElementById("want-read").value
		id = document.querySelector(".book-title").dataset.id
		form = document.querySelector(".want-read-form")
		csrf = form.querySelector("input")

		if (option == "Add Book") {
			
		} else {
			fetch(`/book/status/${id}`, {
				method: 'POST',
				headers: {"X-CSRFToken": csrf.value},
				body: JSON.stringify({
					option: option
				})
			})
			.then (response => response.json())
			.then (result => {
				if (result.success) {
					console.log("sucess")
				}
			})
		}
	}
})