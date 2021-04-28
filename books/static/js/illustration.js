//Wait for document load
document.addEventListener('DOMContentLoaded', () => {
	//Event listeners and functions
	document.querySelector('.bi-plus-circle').addEventListener('click', () => addImageBox())
	document.querySelector('#saveBtn').addEventListener('click', () => deleteImages())
	changeImage()
	eventHandler()
});

//Count deleted illustrations for fetching delete request
let deleteIllu = []

//Preview image before upload
function changeImage () {
	//Get form
	let addForm = document.querySelector('.add-form')
	imageBox = addForm.querySelectorAll('.image-box');
	imageBox.forEach(box => {
		let inpFile = box.querySelector('input');
		let img = box.querySelector('img')
		
		inpFile.addEventListener("change", function () {
			let file = this.files[0];

			if (file) {
				let reader = new FileReader();

				reader.addEventListener("load", function () {
					img.setAttribute("src", this.result);
				})

				reader.readAsDataURL(file);
			}
		})
	})
}

function eventHandler () {
	imageBox = document.querySelectorAll('.image-box');
	imageBox.forEach(box => {
		box.onmouseover = () => {
			box.querySelector('.buttons').style.display = "flex";
		}
		box.onmouseout = () => {
			box.querySelector('.buttons').style.display = "none";
		}

		let deleteBtn = box.querySelectorAll('button');

		deleteBtn.forEach(btn => {
			btn.onclick = () => {
				imageBox = document.querySelectorAll('.image-box');
				if (imageBox.length == 1) {
				} else {
					deleteIllu.push(btn.id)
					btn.parentNode.parentNode.remove()
				}
			}
		})
	})
}

//Count to prevent input id duplication
let count = 2;

function addImageBox () {
	let imagesDiv = document.querySelector('.images-container-add');
	let content = imagesDiv.children[0].cloneNode(true);
	content.querySelector('input').id = "file"+count;
	content.querySelector('input').setAttribute("name", "file"+count);
	content.querySelector('label').setAttribute("for", "file"+count);
	content.querySelector('img').src = "/images/no_image.jpg";
	imagesDiv.appendChild(content);

	eventHandler()
	changeImage()
	count++;
}

function deleteImages () {
	const csrf = document.getElementsByName('csrfmiddlewaretoken');
	const book_id = document.querySelector('.content').id;

	fetch(`/book/${book_id}/illustration`, {
		method: 'DELETE',
		headers:{"X-CSRFToken": csrf[0].value},
		body: JSON.stringify(deleteIllu)
	})
	.then (response => response.json())
	.then (result => {
		if (result.success) {
			window.location.href = `/book/show/${book_id}`
		}
	})
}