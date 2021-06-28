csrf = document.querySelectorAll('input')[2]

function aprove (id) {
	fetch(`/book/aprove/`, {
		method: 'POST',
		headers:{"X-CSRFToken": csrf.value},
		body: JSON.stringify({
			id: id
		})
	})
	.then (response => response.json())
	.then (result => {
		if (result.success) {
			location.reload()
		}
	})
}

function aproveIllustration (id) {
	fetch(`/book/aprove_illustration/`, {
		method: 'POST',
		headers:{"X-CSRFToken": csrf.value},
		body: JSON.stringify({
			id: id
		})
	})
	.then (response => response.json())
	.then (result => {
		if (result.success) {
			location.reload()
		}
	})
}

function aproveDeleteIllustration (id) {
	fetch(`/book/aprove_illustration/`, {
		method: 'DELETE',
		headers:{"X-CSRFToken": csrf.value},
		body: JSON.stringify({
			id: id
		})
	})
	.then (response => response.json())
	.then (result => {
		if (result.success) {
			location.reload()
		}
	})
}

function reprove (id) {
	reproveFetch(id, 'book');
}

function reproveIllustration (id) {
	reproveFetch(id, 'illustration');
}

function reproveIllustrationDelete (id) {
	reproveFetch(id, 'remove_illustration');
}

function reproveFetch (id, model) {
	fetch(`/book/reprove/`, {
		method: 'POST',
		headers:{"X-CSRFToken": csrf.value},
		body: JSON.stringify({
			id: id,
			model: model
		})
	})
	.then (response => response.json())
	.then (result => {
		if (result.success) {
			location.reload()
		}
	})
}