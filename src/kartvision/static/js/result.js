let lastData = null;

function fetchData() {
  fetch("/api/data")
    .then(response => response.json())
    .then(newData => {
      if (lastData && JSON.stringify(lastData) !== JSON.stringify(newData)) {
        triggerHighlight();
      }
      lastData = newData;
      updateResults(newData);
    })
    .catch(error => console.error("データ取得エラー:", error));
}

function updateResults(data) {
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";
  data.forEach(item => {
    const scoreDiv = document.createElement("div");
    scoreDiv.className = "team-score";
    scoreDiv.innerHTML = `
      <div class="tag-name">${item.tag}</div>
      <div class="points">${item.sum_points}</div>
    `;
    resultsDiv.appendChild(scoreDiv);
  });
}

function triggerHighlight() {
  const resultsDiv = document.getElementById("results");
  resultsDiv.classList.add("highlight");
  setTimeout(() => {
    resultsDiv.classList.remove("highlight");
  }, 3000);
}

fetchData();
setInterval(fetchData, 3000);
