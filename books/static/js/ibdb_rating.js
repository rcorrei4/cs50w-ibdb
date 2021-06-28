let ibdbModal = document.getElementById("ibdb-rating-modal");
let ibdbBtn = document.getElementById("ibdb-rating-btn");
let ibdbSpan = document.getElementById("ibdb-modal-close");
id = document.querySelector(".book-title").dataset.id
scoreBars = document.querySelectorAll(".score-bar")

ibdbBtn.onclick = function() {
  ibdbModal.style.display = "block";
}

ibdbSpan.onclick = function() {
  ibdbModal.style.display = "none";
}

fetch(`/book/${id}/score`, {
  method: 'GET'
})
.then (response => response.json())
.then (result => {
    for (i = 4; i >= 0; i--) {
      width = (result["score_"+(i+1)] * 100) / result.total
      scoreBars[i].style.width = `${width}%`;
    }
  })