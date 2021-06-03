infoContributions = document.querySelectorAll(".info-contributions")
imageContributions = document.querySelectorAll(".image-contributions")
imageDeleteContributions = document.querySelectorAll(".delete-contributions")

infoContributions.forEach(contribution => {
	csrf = contribution.querySelector('input')
	contribution.querySelector("button").onclick = () => {
		fetch(`/book/aprove/`, {
			method: 'POST',
			headers:{"X-CSRFToken": csrf.value},
			body: JSON.stringify({
				id: contribution.querySelector("button").id
			})
		})
		.then (response => response.json())
		.then (result => {
			if (result.success) {
				contribution.remove()
			}
		})
	}
})

imageContributions.forEach(contribution => {
	csrf = contribution.querySelector('input')
	contribution.querySelector("button").onclick = () => {
		fetch(`/book/aprove_illustration/`, {
			method: 'POST',
			headers:{"X-CSRFToken": csrf.value},
			body: JSON.stringify({
				id: contribution.querySelector("button").id
			})
		})
		.then (response => response.json())
		.then (result => {
			if (result.success) {
				contribution.remove()
			}
		})
	}
})

imageDeleteContributions.forEach(contribution => {
	csrf = contribution.querySelector('input')
	contribution.querySelector("button").onclick = () => {
		fetch(`/book/aprove_illustration/`, {
			method: 'DELETE',
			headers:{"X-CSRFToken": csrf.value},
			body: JSON.stringify({
				id: contribution.querySelector("button").id
			})
		})
		.then (response => response.json())
		.then (result => {
			if (result.success) {
				contribution.remove()
			}
		})
	}
})