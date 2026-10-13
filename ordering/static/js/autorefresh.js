(function () {
  "use strict";
  const el = document.querySelector("[data-autorefresh]");
  if (!el) return;
  const seconds = parseInt(el.dataset.autorefresh, 10) || 30;
  setInterval(() => {
    if (document.visibilityState === "visible") {
      // Reload without resubmitting forms or keeping ?placed=1
      window.location.replace(window.location.pathname);
    }
  }, seconds * 1000);
})();
