let form = document.querySelector('.images-container');
let imageBox = document.querySelectorAll('.image-box');

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
					btn.parentNode.parentNode.remove()
				}
			}
		})

		let inpFile = box.querySelector('input');
		let previewImage = box.querySelector('img');

		inpFile.addEventListener("change", function () {
			let file = this.files[0];

			if (file) {
				let reader = new FileReader();

				reader.addEventListener("load", function () {
					previewImage.setAttribute("src", this.result);
				})

				reader.readAsDataURL(file);
			}
		})
	})
}

eventHandler()

addBtn = document.querySelector('.bi-plus-circle');

addBtn.addEventListener("click", function() {
	imageBox = document.querySelectorAll('.image-box');
	let content = form.children[0].cloneNode(true);
	id = Math.floor(Math.random() * 100000);
	content.querySelector('input').id = "file"+id;
	content.querySelector('input').setAttribute("name", "file"+id);
	content.querySelector('label').setAttribute("for", "file"+id);
	content.querySelector('img').src = "/images/no_image.jpg"
	form.appendChild(content);
	eventHandler()
})