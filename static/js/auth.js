document.querySelectorAll("form[data-auth]").forEach(form => {
  form.addEventListener("submit", e => {
    let ok = true;
    form.querySelectorAll("input.input").forEach(i => {
      const bad = !i.value.trim();
      i.classList.toggle("invalid", bad);
      if (bad) ok = false;
    });
    if (!ok) e.preventDefault();
  });
});
