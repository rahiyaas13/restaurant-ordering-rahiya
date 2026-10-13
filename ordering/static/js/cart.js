/* Shared cart: UI state lives in localStorage, validated copy lives in the Django session. */
(function () {
  "use strict";
  const KEY = "emberleaf_cart_v1";
  const body = document.body;
  const SYNC_URL = body.dataset.syncUrl;
  const MAX = parseInt(body.dataset.maxQty || "20", 10);
  const listeners = { change: [], sync: [] };
  let timer = null;

  function getCookie(name) {
    const m = document.cookie.match(new RegExp("(?:^|; )" + name + "=([^;]*)"));
    return m ? decodeURIComponent(m[1]) : "";
  }

  function sanitize(cart) {
    const out = {};
    Object.keys(cart || {}).forEach((k) => {
      const q = Math.min(MAX, parseInt(cart[k], 10));
      if (/^\d+$/.test(k) && q > 0) out[k] = q;
    });
    return out;
  }

  function read() {
    try {
      const obj = JSON.parse(localStorage.getItem(KEY));
      return obj && typeof obj === "object" && !Array.isArray(obj) ? sanitize(obj) : {};
    } catch (e) {
      return {};
    }
  }

  function persist(cart) {
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) { /* storage disabled */ }
  }

  function count(cart) {
    cart = cart || read();
    return Object.keys(cart).reduce((n, k) => n + cart[k], 0);
  }

  function badge() {
    const el = document.getElementById("cartCount");
    if (!el) return;
    const n = count();
    el.textContent = n;
    el.classList.toggle("d-none", n === 0);
  }

  function emit(name, data) { listeners[name].forEach((fn) => fn(data)); }

  function write(cart) {
    cart = sanitize(cart);
    persist(cart);
    badge();
    emit("change", cart);
    clearTimeout(timer);
    timer = setTimeout(syncNow, 350);
  }

  async function syncNow() {
    clearTimeout(timer);
    try {
      const res = await fetch(SYNC_URL, {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({ cart: read() }),
      });
      if (!res.ok) throw new Error("sync failed: " + res.status);
      const data = await res.json();
      // The server is authoritative: drop anything it rejected.
      if (JSON.stringify(data.cart) !== JSON.stringify(read())) {
        persist(data.cart);
        badge();
        emit("change", data.cart);
      }
      emit("sync", data);
      return data;
    } catch (e) {
      console.warn(e);
      return null;
    }
  }

  const Cart = {
    read, count, syncNow,
    qty: (id) => read()[String(id)] || 0,
    set(id, q) {
      const cart = read();
      q = Math.min(MAX, Math.max(0, parseInt(q, 10) || 0));
      if (q === 0) delete cart[String(id)]; else cart[String(id)] = q;
      write(cart);
    },
    add(id) { this.set(id, this.qty(id) + 1); },
    remove(id) { this.set(id, 0); },
    clear() { persist({}); badge(); emit("change", {}); },
    on(name, fn) { listeners[name].push(fn); },
  };
  window.Cart = Cart;

  if (body.dataset.clearCart === "1") Cart.clear(); // order was just placed
  badge();
  window.addEventListener("storage", badge);
})();
