(function () {
  "use strict";
  const menu = {};
  JSON.parse(document.getElementById("menu-data").textContent).forEach((i) => (menu[i.id] = i));
  const taxRate = parseFloat(document.body.dataset.taxRate);
  const cur = document.body.dataset.currency;
  const MAX = parseInt(document.body.dataset.maxQty, 10);

  const linesEl = document.getElementById("cartLines");
  const content = document.getElementById("cartContent");
  const empty = document.getElementById("emptyCart");
  const warnEl = document.getElementById("cartWarnings");
  const form = document.getElementById("checkoutForm");
  const btn = document.getElementById("placeOrder");

  const fmt = (n) => cur + Number(n).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  function showTotals(sub, tax, total) {
    document.getElementById("subtotal").textContent = fmt(sub);
    document.getElementById("tax").textContent = fmt(tax);
    document.getElementById("grand").textContent = fmt(total);
  }

  function render() {
    const cart = Cart.read();
    // Drop anything not on the (available) menu.
    Object.keys(cart).forEach((id) => { if (!menu[id]) delete cart[id]; });
    const ids = Object.keys(cart);

    empty.classList.toggle("d-none", ids.length > 0);
    content.classList.toggle("d-none", ids.length === 0);
    btn.disabled = ids.length === 0;

    let subtotal = 0;
    linesEl.innerHTML = ids.map((id) => {
      const item = menu[id], q = cart[id];
      const lt = parseFloat(item.price) * q;
      subtotal += lt;
      return `
        <div class="cart-line" data-id="${id}">
          <span class="diet-mark ${item.veg ? "veg" : "nonveg"}"></span>
          <div class="name">${esc(item.name)}<span class="unit">${fmt(item.price)} each</span></div>
          <div class="stepper">
            <button type="button" data-act="dec" aria-label="Decrease quantity"><i class="bi bi-dash"></i></button>
            <span class="qty">${q}</span>
            <button type="button" data-act="inc" aria-label="Increase quantity" ${q >= MAX ? "disabled" : ""}><i class="bi bi-plus"></i></button>
          </div>
          <div class="line-total">${fmt(lt)}</div>
          <button type="button" class="remove" data-act="rm" aria-label="Remove ${esc(item.name)}"><i class="bi bi-x-lg"></i></button>
        </div>`;
    }).join("");

    const tax = Math.round(subtotal * taxRate * 100) / 100;
    showTotals(subtotal, tax, subtotal + tax); // provisional; server totals replace these after sync
  }

  linesEl.addEventListener("click", (e) => {
    const b = e.target.closest("[data-act]");
    if (!b) return;
    const id = b.closest(".cart-line").dataset.id;
    if (b.dataset.act === "inc") Cart.add(id);
    else if (b.dataset.act === "dec") Cart.set(id, Cart.qty(id) - 1);
    else Cart.remove(id);
  });

  function showWarnings(list) {
    warnEl.innerHTML = (list || []).map((w) => `<div class="alert alert-warning">${esc(w)}</div>`).join("");
  }

  Cart.on("change", render);
  Cart.on("sync", (data) => {
    showWarnings(data.warnings);
    if (Object.keys(data.cart).length) showTotals(data.subtotal, data.tax, data.total);
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    btn.disabled = true;
    btn.textContent = "Placing order...";
    const data = await Cart.syncNow(); // make sure the session cart is current
    if (!data || !Object.keys(data.cart).length) {
      btn.textContent = "Place order";
      btn.disabled = false;
      showWarnings([data ? "Your cart is empty." : "Could not reach the server. Please try again."]);
      return;
    }
    form.submit();
  });

  render();
  Cart.syncNow();
})();
