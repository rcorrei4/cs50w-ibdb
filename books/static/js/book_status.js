function bookStatus () {
	option = document.getElementById("want-read")
	id = document.querySelector(".book-title").dataset.id
	form = document.querySelector(".want-read-form")
	csrf = form.querySelector("input")

	if (option == "Add Book") {
		
	} else {
		fetch(`/book/status/${id}`, {
			method: 'POST',
			headers: {"X-CSRFToken": csrf.value},
			body: JSON.stringify({
				option: option.value
			})
		})
		.then (response => response.json())
		.then (result => {
			if (result.success) {
				console.log("sucess")

				if (option.value == "want_read") {
					option[1].innerText = "Want to read ✓"
					option[2].innerText = "Currently reading"
					option[3].innerText = "Read"
				} 
				else if (option.value == "reading") {
					option[1].innerText = "Want to read"
					option[2].innerText = "Currently reading ✓"
					option[3].innerText = "Read"	
				} 
				else if (option.value == "read") {
					option[1].innerText = "Want to read"
					option[2].innerText = "Currently reading"
					option[3].innerText = "Read ✓"	
				}
			}
		})
	}
}

function wantRead () {
	
}