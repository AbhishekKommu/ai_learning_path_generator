const genForm = document.getElementById("generate-form");
if (genForm) {
  genForm.addEventListener("submit", () => {
    const b = document.getElementById("generate-btn");
    b.disabled = true; b.textContent = "Building your path...";
  });
}
const timeline = document.querySelector(".timeline");
if (timeline) {
  timeline.addEventListener("change", async e => {
    const box = e.target;
    if (!box.matches("input[data-week]")) return;
    const url = timeline.dataset.toggleUrl.replace(/\/0$/, "/" + box.dataset.week);
    try {
      const res = await fetch(url, { method: "POST", headers: { "X-CSRFToken": csrfToken() } });
      if (!res.ok) throw new Error();
      const data = await res.json();
      box.closest(".week").classList.toggle("done", data.done);
      document.getElementById("progress-fill").style.width = data.progress + "%";
      document.getElementById("progress-text").textContent = data.progress;
    } catch (_) {
      box.checked = !box.checked;
      alert("Couldn't save that change. Check your connection and try again.");
    }
  });
}
