(function () {
  "use strict";
  const sections = document.querySelectorAll(".menu-section");
  const chips = document.querySelectorAll("#filterBar .chip");
  const vegOnly = document.getElementById("vegOnly");
  const noMatch = document.getElementById("noMatch");
  let activeCat = "all";

  function applyFilters() {
    let visibleTotal = 0;
    sections.forEach((sec) => {
      const catOk = activeCat === "all" || sec.dataset.category === activeCat;
      let visible = 0;
      sec.querySelectorAll(".menu-item").forEach((card) => {
        const show = catOk && (!vegOnly.checked || card.dataset.veg === "1");
        card.classList.toggle("d-none", !show);
        if (show) visible++;
      });
      sec.classList.toggle("d-none", visible === 0);
      visibleTotal += visible;
    });
    noMatch.classList.toggle("d-none", visibleTotal !== 0);
  }

  chips.forEach((chip) =>
    chip.addEventListener("click", () => {
      chips.forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      activeCat = chip.dataset.filter;
      applyFilters();
    })
  );
  vegOnly.addEventListener("change", applyFilters);

  // Add / stepper controls
  function renderControl(ctl) {
    const q = Cart.qty(ctl.dataset.id);
    ctl.querySelector(".btn-add").classList.toggle("d-none", q > 0);
    ctl.querySelector(".stepper").classList.toggle("d-none", q === 0);
    ctl.querySelector(".qty").textContent = q;
  }
  const controls = document.querySelectorAll(".dish-ctl");
  const renderAll = () => controls.forEach(renderControl);

  controls.forEach((ctl) =>
    ctl.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-action]");
      if (!btn) return;
      const id = ctl.dataset.id;
      const action = btn.dataset.action;
      if (action === "add" || action === "inc") Cart.add(id);
      else Cart.set(id, Cart.qty(id) - 1);
    })
  );

  Cart.on("change", renderAll);
  renderAll();
  Cart.syncNow(); // refresh the server session and drop items that became unavailable
})();
