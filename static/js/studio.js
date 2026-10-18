(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    // ---------- Shape picker live preview ----------
    const shapeRadios = document.querySelectorAll('.shape-picker input[type="radio"]');
    const previewFrame = document.querySelector('[data-preview-frame]');

    function applyShape(shape) {
      if (!previewFrame) return;
      const classes = previewFrame.className
        .split(/\s+/)
        .filter(function (c) { return c && !c.startsWith("shape-"); });
      classes.push("shape-" + shape);
      previewFrame.className = classes.join(" ");
    }

    shapeRadios.forEach(function (radio) {
      radio.addEventListener("change", function () {
        if (this.checked) applyShape(this.value);
      });
    });

    // ---------- File input → live image preview ----------
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function (input) {
      input.addEventListener("change", function () {
        if (!this.files || !this.files[0]) return;
        if (!this.files[0].type.startsWith("image/")) return;
        if (!previewFrame) return;

        const url = URL.createObjectURL(this.files[0]);
        let img = previewFrame.querySelector("[data-preview-image]");
        if (img) {
          img.src = url;
        } else {
          img = document.createElement("img");
          img.src = url;
          img.alt = "Preview";
          img.setAttribute("data-preview-image", "");
          previewFrame.innerHTML = "";
          previewFrame.appendChild(img);
        }
      });
    });
  });
})();