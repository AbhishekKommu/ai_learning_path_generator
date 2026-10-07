window.csrfToken = () => document.querySelector('meta[name="csrf-token"]').content;
document.querySelectorAll(".flash").forEach(el => {
  if (el.classList.contains("success") || el.classList.contains("info")) {
    setTimeout(() => { el.style.transition = "opacity .5s"; el.style.opacity = 0; }, 5000);
  }
});
