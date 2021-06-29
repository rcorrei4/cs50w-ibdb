document.addEventListener('DOMContentLoaded' , function () {
	if (screen.width < 676) {
		container = document.createElement('div');
		container.classList.add('.responsive-container');

		searchBtn = document.querySelector('search-btn-responsive');
		loginBtn = document.querySelector('.login-btn');
		container.appendChild(loginBtn);

		document.body.querySelector(".navbar").appendChild(container);
	}
})

function menuControl() {
	if (document.querySelector('ul').style.display == 'block') {
		document.querySelector('ul').style.display = 'none';
	} else {
		document.querySelector('ul').style.display = 'block';
	}
};

function searchControl() {
	if (document.querySelector('.search-form').style.display == 'flex') {
		document.querySelector('.search-form').style.display = 'none';
		document.querySelector('.search-btn').style.display = 'none';
	} else {
		document.querySelector('.search-form').style.display = 'flex';
		document.querySelector('.search-btn').style.display = 'none';
	}
}