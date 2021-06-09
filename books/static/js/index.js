var swiper = new Swiper('.swiper1', {
  // Optional parameters
  loop: true,
  preventClicks: false,
  preventClicksPropagation: false,

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

});

var swiper2 = new Swiper('.swiper2', {
  direction: 'vertical',
  loop: true,
  slidesPerView: 3,
  initialSlide: 1,
  allowTouchMove: false,
});

var swiper3 = new Swiper('.swiper3', {
  slidesPerView: 7,
  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});

var swiper4 = new Swiper('.swiper4', {
  slidesPerView: 7,
  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});

swiper.on('slideChangeTransitionEnd', function() {
	var book = document.querySelector('.swiper-slide-active');

	fetch(`/book/${book.dataset.id}`)
	.then(response => response.json())
	.then(result => {
		document.querySelector('#book-title').innerText = result.book.title;
		document.querySelector('#book-author').innerText = "by "+result.book.author;
		document.querySelector('#book-synopsis').innerText = result.book.synopsis;
    document.querySelector('#book-genre').innerText = result.book.genre;
	})
})

swiper.on('slideNextTransitionEnd', function() {
	swiper2.slideNext()
})

swiper.on('slidePrevTransitionEnd', function() {
	swiper2.slidePrev()
})