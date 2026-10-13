(function () {
  var root = document.documentElement;

  function current() {
    return root.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    try {
      localStorage.setItem("saad-theme", theme);
    } catch (error) {
      /* Storage can be blocked. The theme still applies for this visit. */
    }
    var button = document.getElementById("theme-toggle");
    if (!button) return;
    var isLight = theme === "light";
    button.setAttribute("aria-pressed", isLight ? "true" : "false");
    button.setAttribute("aria-label", isLight ? "Switch to dark theme" : "Switch to light theme");
    var meta = document.querySelector('meta[name="theme-color"]:not([media])');
    if (meta) meta.setAttribute("content", isLight ? "#F8FAFC" : "#0B1020");
  }

  document.addEventListener("DOMContentLoaded", function () {
    apply(current());
    var button = document.getElementById("theme-toggle");
    if (!button) return;
    button.addEventListener("click", function () {
      apply(current() === "light" ? "dark" : "light");
    });
  });
})();
