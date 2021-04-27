var form = document.querySelector('.images-container');
var imageBox = document.querySelectorAll('.image-box');

function eventHandler () {
	var imageBox = document.querySelectorAll('.image-box');
	imageBox.forEach(box => {
		box.onmouseover = () => {
			box.querySelector('.buttons').style.display = "flex";
		}
		box.onmouseout = () => {
			box.querySelector('.buttons').style.display = "none";
		}

		var deleteBtn = box.querySelectorAll('button');

		deleteBtn.forEach(btn => {
			btn.onclick = () => {
				btn.parentNode.parentNode.remove()
			}
		})

		var inpFile = box.querySelector('input');
		var previewImage = box.querySelector('img');

		inpFile.addEventListener("change", function () {
			var file = this.files[0];

			if (file) {
				var reader = new FileReader();

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
	var content = form.children[0].cloneNode(true);
	id = imageBox.length + 1;
	content.querySelector('input').id = "file"+id;
	content.querySelector('label').setAttribute("for", "file"+id);
	content.querySelector('img').src = "/images/no_image.jpg"
	form.appendChild(content);
	eventHandler()
})