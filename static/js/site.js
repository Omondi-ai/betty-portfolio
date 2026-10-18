(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    // Smooth scroll for on-page anchors
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener("click", function (e) {
        var href = link.getAttribute("href");
        if (!href || href === "#") return;
        var target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: "smooth", block: "start" });
          var nav = document.querySelector("[data-nav-links]");
          if (nav) nav.classList.remove("is-open");
          var toggle = document.querySelector("[data-nav-toggle]");
          if (toggle) toggle.setAttribute("aria-expanded", "false");
        }
      });
    });

    // Mobile nav toggle
    var toggle = document.querySelector("[data-nav-toggle]");
    var links = document.querySelector("[data-nav-links]");
    if (toggle && links) {
      toggle.addEventListener("click", function () {
        var isOpen = links.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      });
    }
  });
})();