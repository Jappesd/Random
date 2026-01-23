//hoitaa emoji clickit, lähettää datan backendiin,
//näyttää kiitos viestin ja auto resettaa

const ratingContainer = document.getElementById("rating-container");
const thankYou = document.getElementById("thank-you");

ratingContainer.addEventListener("click", (event) => {
  const target = event.target;

  if (!target.dataset.rating) return;

  const rating = target.dataset.rating;

  //lähettää arvostelun backendiin
  fetch("/rate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ rating }),
  }).catch(() => {});

  //ui feedback
  ratingContainer.classList.add("hidden");
  thankYou.classList.remove("hidden");

  //resettaa näkymän 3 sekunnin jälkeen
  setTimeout(() => {
    thankYou.classList.add("hidden");
    ratingContainer.classList.remove("hidden");
  }, 3000);
});
