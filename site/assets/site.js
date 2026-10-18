// Site chrome for the Markus docs: the color-scheme switch and the contents menu.
(function () {
  var root = document.documentElement;
  var storageKey = "markus-color-scheme";

  function readSaved() {
    try {
      var saved = localStorage.getItem(storageKey);
      return saved === "light" || saved === "dark" ? saved : "system";
    } catch (error) {
      return "system";
    }
  }

  function apply(scheme) {
    if (scheme === "system") {
      root.removeAttribute("data-color-scheme");
    } else {
      root.setAttribute("data-color-scheme", scheme);
    }
    document.querySelectorAll(".site-scheme button").forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.dataset.scheme === scheme));
    });
  }

  document.querySelectorAll(".site-scheme button").forEach(function (button) {
    button.addEventListener("click", function () {
      var scheme = button.dataset.scheme;
      try {
        if (scheme === "system") localStorage.removeItem(storageKey);
        else localStorage.setItem(storageKey, scheme);
      } catch (error) {}
      apply(scheme);
    });
  });
  apply(readSaved());

  // The sidebar is a <details> so it folds into a menu on narrow screens; keep it open when wide.
  var menu = document.querySelector(".site-menu");
  if (menu && window.matchMedia) {
    var wide = window.matchMedia("(min-width: 64rem)");
    var sync = function () { menu.open = wide.matches; };
    sync();
    if (wide.addEventListener) wide.addEventListener("change", sync);
  }
})();
