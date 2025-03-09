const API_EDIT_URL = "/api/edit_points";
const API_EDIT_TAG_URL = "/api/edit_tag";
const API_DATA_URL = "/api/data";

function fetchData() {
  fetch(API_DATA_URL)
    .then(response => response.json())
    .then(data => {
      renderTeams(data);
      adjustSize();
    })
    .catch(error => console.error("データ取得エラー:", error));
}

function renderTeams(teams) {
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";
  teams.forEach(team => {
    const card = document.createElement("div");
    card.className = "team-card";
    card.setAttribute("draggable", "true");
    card.dataset.tag = team.tag;

    // チーム情報エリア
    const infoDiv = document.createElement("div");
    infoDiv.className = "team-info";
    const tagEl = document.createElement("div");
    tagEl.className = "team-tag";
    tagEl.textContent = team.tag;
    const tagInput = document.createElement("input");
    tagInput.className = "edit-tag-input";
    tagInput.type = "text";
    tagInput.value = team.tag;
    tagInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        updateTag(team.tag, tagInput.value);
      }
    });

    const pointsEl = document.createElement("div");
    pointsEl.className = "team-points";
    pointsEl.textContent = team.sum_points;
    const editInput = document.createElement("input");
    editInput.className = "edit-input";
    editInput.type = "number";
    editInput.value = team.sum_points;
    editInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        updatePoints(team.tag, parseInt(editInput.value));
      }
    });

    infoDiv.appendChild(tagEl);
    infoDiv.appendChild(tagInput);
    infoDiv.appendChild(pointsEl);
    infoDiv.appendChild(editInput);

    // アクションボタンエリア
    const actionsDiv = document.createElement("div");
    actionsDiv.className = "actions";

    // 絶対編集用ボタン
    const editBtn = document.createElement("button");
    editBtn.className = "action-button edit-button";
    editBtn.textContent = "点数編集";
    editBtn.addEventListener("click", () => {
      editBtn.style.display = "none";
      saveBtn.style.display = "inline-block";
      pointsEl.style.display = "none";
      editInput.style.display = "inline-block";
    });
    const saveBtn = document.createElement("button");
    saveBtn.className = "action-button save-button";
    saveBtn.textContent = "保存";
    saveBtn.style.display = "none";
    saveBtn.addEventListener("click", () => {
      updatePoints(team.tag, parseInt(editInput.value));
    });

    // タグ編集用ボタン
    const editTagBtn = document.createElement("button");
    editTagBtn.className = "action-button tag-edit-button";
    editTagBtn.textContent = "タグ編集";
    editTagBtn.addEventListener("click", () => {
      editTagBtn.style.display = "none";
      saveTagBtn.style.display = "inline-block";
      tagEl.style.display = "none";
      tagInput.style.display = "inline-block";
    });
    const saveTagBtn = document.createElement("button");
    saveTagBtn.className = "action-button tag-save-button";
    saveTagBtn.textContent = "タグ保存";
    saveTagBtn.style.display = "none";
    saveTagBtn.addEventListener("click", () => {
      updateTag(team.tag, tagInput.value);
    });

    // 相対編集用：＋／－ボタン＋入力欄（Enterキーで確定）
    const relativeInput = document.createElement("input");
    relativeInput.className = "relative-input";
    relativeInput.type = "number";
    relativeInput.value = 5;
    relativeInput.style.display = "none";
    let currentRelativeOperation = null;
    const plusBtn = document.createElement("button");
    plusBtn.className = "action-button relative-button";
    plusBtn.textContent = "＋";
    plusBtn.addEventListener("click", () => {
      currentRelativeOperation = "plus";
      relativeInput.style.display = "inline-block";
      relativeInput.focus();
    });
    const minusBtn = document.createElement("button");
    minusBtn.className = "action-button relative-button";
    minusBtn.textContent = "－";
    minusBtn.addEventListener("click", () => {
      currentRelativeOperation = "minus";
      relativeInput.style.display = "inline-block";
      relativeInput.focus();
    });
    relativeInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        const currentPoints = parseInt(pointsEl.textContent);
        const adjust = parseInt(relativeInput.value);
        let newPoints = currentPoints;
        if (currentRelativeOperation === "plus") {
          newPoints += adjust;
        } else if (currentRelativeOperation === "minus") {
          newPoints -= adjust;
        }
        updatePoints(team.tag, newPoints);
        relativeInput.style.display = "none";
        currentRelativeOperation = null;
      }
    });

    actionsDiv.appendChild(editBtn);
    actionsDiv.appendChild(saveBtn);
    actionsDiv.appendChild(editTagBtn);
    actionsDiv.appendChild(saveTagBtn);
    actionsDiv.appendChild(plusBtn);
    actionsDiv.appendChild(minusBtn);
    actionsDiv.appendChild(relativeInput);

    card.appendChild(infoDiv);
    card.appendChild(actionsDiv);

    // ドラッグ＆ドロップ用イベント
    card.addEventListener("dragstart", dragStart);
    card.addEventListener("dragover", dragOver);
    card.addEventListener("dragleave", dragLeave);
    card.addEventListener("drop", drop);

    resultsDiv.appendChild(card);
  });
}

function updatePoints(tag, newPoints) {
  fetch(API_EDIT_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tag: tag, points: newPoints })
  })
    .then(response => response.json())
    .then(result => {
      if (result.status === "success") {
        fetchData();
      } else {
        alert("点数更新エラー: " + result.message);
      }
    })
    .catch(error => console.error("更新エラー:", error));
}

function updateTag(tag, newTag) {
  fetch(API_EDIT_TAG_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tag: tag, new_tag: newTag })
  })
    .then(response => response.json())
    .then(result => {
      if (result.status === "success") {
        fetchData();
      } else {
        alert("タグ更新エラー: " + result.message);
      }
    })
    .catch(error => console.error("タグ更新エラー:", error));
}

// ドラッグ＆ドロップ処理
let draggedTag = null;
function dragStart(event) {
  draggedTag = event.currentTarget.dataset.tag;
  event.dataTransfer.setData("text/plain", draggedTag);
  event.currentTarget.style.opacity = "0.5";
}
function dragOver(event) {
  event.preventDefault();
  event.currentTarget.classList.add("drag-over");
}
function dragLeave(event) {
  event.currentTarget.classList.remove("drag-over");
}
function drop(event) {
  event.preventDefault();
  event.currentTarget.classList.remove("drag-over");
  const targetTag = event.currentTarget.dataset.tag;
  if (draggedTag && draggedTag !== targetTag) {
    fetch(API_EDIT_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tag: draggedTag, target_tag: targetTag })
    })
      .then(response => response.json())
      .then(result => {
        if (result.status === "success") {
          fetchData();
        } else {
          alert("統合エラー: " + result.message);
        }
      })
      .catch(error => console.error("統合エラー:", error));
  }
  draggedTag = null;
  event.currentTarget.style.opacity = "1";
}

// サイズ自動調整：全チームが画面内に収まるようにする
function adjustSize() {
  const resultsDiv = document.getElementById("results");
  // ヘッダーとフッターの分を除いた利用可能な高さ（例: 150px を引く）
  const availableHeight = window.innerHeight - 150;
  const currentHeight = resultsDiv.offsetHeight;
  let scale = 1;
  if (currentHeight > availableHeight) {
    scale = availableHeight / currentHeight;
  }
  resultsDiv.style.transform = "scale(" + scale + ")";
  resultsDiv.style.transformOrigin = "top center";
}

document.addEventListener("DOMContentLoaded", () => {
  fetchData();
  window.addEventListener("resize", adjustSize);
});
