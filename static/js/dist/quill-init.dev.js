"use strict";

(function () {
  "use strict";

  function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
  }

  function buildFullToolbar() {
    return ['<div class="quill-toolbar">', '  <span class="ql-formats">', '    <select class="ql-header" title="Heading">', '      <option value="1">H1</option>', '      <option value="2">H2</option>', '      <option value="3">H3</option>', '      <option selected></option>', '    </select>', '  </span>', '  <span class="ql-formats">', '    <button class="ql-bold" type="button" title="Bold"></button>', '    <button class="ql-italic" type="button" title="Italic"></button>', '    <button class="ql-underline" type="button" title="Underline"></button>', '  </span>', '  <span class="ql-formats">', '    <button class="ql-list" value="ordered" type="button" title="Numbered list"></button>', '    <button class="ql-list" value="bullet" type="button" title="Bulleted list"></button>', '  </span>', '  <span class="ql-formats">', '    <button class="ql-blockquote" type="button" title="Quote"></button>', '    <button class="ql-link" type="button" title="Link"></button>', '    <button class="ql-image" type="button" title="Image"></button>', '  </span>', '  <span class="ql-formats">', '    <button class="ql-clean" type="button" title="Clear formatting"></button>', '  </span>', "</div>"].join("");
  }

  function buildInlineToolbar() {
    return ['<div class="quill-toolbar quill-toolbar-inline">', '  <span class="ql-formats">', '    <button class="ql-bold" type="button" title="Bold"></button>', '    <button class="ql-italic" type="button" title="Italic"></button>', '    <button class="ql-underline" type="button" title="Underline"></button>', '  </span>', '  <span class="ql-formats">', '    <button class="ql-link" type="button" title="Link"></button>', '  </span>', '  <span class="ql-formats">', '    <button class="ql-clean" type="button" title="Clear formatting"></button>', '  </span>', "</div>"].join("");
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (typeof Quill === "undefined") return;
    var textareas = document.querySelectorAll("textarea[data-quill]");
    if (!textareas.length) return;
    var csrfToken = getCookie("csrftoken");
    textareas.forEach(function (textarea) {
      var isInline = textarea.getAttribute("data-quill-inline") === "true";
      var wrapper = document.createElement("div");
      wrapper.className = "quill-wrapper";
      wrapper.innerHTML = (isInline ? buildInlineToolbar() : buildFullToolbar()) + '<div class="quill-editor"></div>';
      textarea.parentNode.insertBefore(wrapper, textarea.nextSibling);
      textarea.style.display = "none";
      var editorEl = wrapper.querySelector(".quill-editor");
      var toolbarEl = wrapper.querySelector(".quill-toolbar");
      var modules = {
        toolbar: {
          container: toolbarEl
        }
      };

      if (!isInline) {
        modules.toolbar.handlers = {
          image: function image() {
            var input = document.createElement("input");
            input.type = "file";
            input.accept = "image/*";

            input.onchange = function () {
              var file = input.files[0];
              if (!file) return;

              if (!file.type.startsWith("image/")) {
                alert("Please choose an image file.");
                return;
              }

              var formData = new FormData();
              formData.append("image", file);
              fetch("/studio/upload-image/", {
                method: "POST",
                headers: {
                  "X-CSRFToken": csrfToken
                },
                body: formData,
                credentials: "same-origin"
              }).then(function (r) {
                return r.json();
              }).then(function (data) {
                if (data.url) {
                  var range = quill.getSelection(true) || {
                    index: quill.getLength()
                  };
                  quill.insertEmbed(range.index, "image", data.url);
                  quill.setSelection(range.index + 1);
                } else if (data.error) {
                  alert(data.error);
                }
              })["catch"](function () {
                alert("Upload failed. Please try again.");
              });
            };

            input.click();
          }
        };
      }

      var quill = new Quill(editorEl, {
        theme: "snow",
        placeholder: textarea.getAttribute("placeholder") || "Write here…",
        modules: modules
      });

      if (textarea.value) {
        quill.clipboard.dangerouslyPasteHTML(textarea.value);
      }

      var form = textarea.closest("form");

      if (form) {
        form.addEventListener("submit", function () {
          textarea.value = quill.root.innerHTML;
        });
      }
    });
  });
})();
//# sourceMappingURL=quill-init.dev.js.map
