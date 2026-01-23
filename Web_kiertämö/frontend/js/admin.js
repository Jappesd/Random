const loginBtn = document.getElementById("login-btn");
const adminKeyInput = document.getElementById("admin-key");
const loginError = document.getElementById("login-error");
const loginContainer = document.getElementById("login-container");

const adminActions = document.getElementById("admin-actions");
const exportBtn = document.getElementById("export-btn");
const exportStatus = document.getElementById("export-status");
const statsContainer = document.getElementById("stats-container");
const statsTableBody = document.querySelector("#stats-table tbody");
//Store key in memory (not localStorage)
let adminKey = "";

//ehtii statsit
function fetchStats() {
  fetch("/stats", {
    headers: { "X-Admin-Key": adminKey },
  })
    .then((res) => res.json())
    .then((data) => {
      statsTableBody.innerHTML = ""; //clears old rows

      //ensure all ratings are displayed
      const ratings = ["huono", "ok", "hyvä"];
      ratings.forEach((rating) => {
        const countObj = data.find((d) => d.rating === rating);
        const count = countObj ? countObj.count : 0;

        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${rating}</td><td>${count}</td>`;
        statsTableBody.appendChild(tr);
      });

      statsContainer.classList.remove("hidden");
    })
    .catch((err) => {
      console.error(err);
      statsContainer.classList.add("hidden");
    });
}

// Login button
loginBtn.addEventListener("click", () => {
  const key = adminKeyInput.value.trim();
  if (!key) return;

  //Simple test: call /stats with the key
  fetch("/stats", {
    headers: { "X-Admin-Key": key },
  })
    .then((res) => {
      if (res.status === 200) {
        //login success
        adminKey = key;
        loginContainer.classList.add("hidden");
        adminActions.classList.remove("hidden");

        fetchStats();
      } else {
        loginError.classList.remove("hidden");
      }
    })
    .catch(() => {
      loginError.classList.remove("hidden");
    });
});

//export csv button
exportBtn.addEventListener("click", () => {
  exportStatus.textContent = "Exporting...";

  fetch("/export.csv", {
    headers: { "X-Admin-Key": adminKey },
  })
    .then((res) => res.blob())
    .then((blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "ratings.csv";
      a.click();
      window.URL.revokeObjectURL(url);
      exportStatus.textContent = "CSV downloaded!";
    })
    .catch((err) => {
      console.error(err);
      exportStatus.textContent = "Export Failed :(";
    });
});
