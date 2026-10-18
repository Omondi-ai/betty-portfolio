(function () {
  "use strict";

  function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
  }

  function buildFullToolbar() {
    return [
      '<div class="quill-toolbar">',
      '  <span class="ql-formats">',
      '    <select class="ql-header" title="Heading">',
      '      <option value="1">H1</option>',
      '      <option value="2">H2</option>',
      '      <option value="3">H3</option>',
      '      <option selected></option>',
      '    </select>',
      '  </span>',
      '  <span class="ql-formats">',
      '    <button class="ql-bold" type="button" title="Bold"></button>',
      '    <button class="ql-italic" type="button" title="Italic"></button>',
      '    <button class="ql-underline" type="button" title="Underline"></button>',
      '  </span>',
      '  <span class="ql-formats">',
      '    <button class="ql-list" value="ordered" type="button" title="Numbered list"></button>',
      '    <button class="ql-list" value="bullet" type="button" title="Bulleted list"></button>',
      '  </span>',
      '  <span class="ql-formats">',
      '    <button class="ql-blockquote" type="button" title="Quote"></button>',
      '    <button class="ql-link" type="button" title="Link"></button>',
      '    <button class="ql-image" type="button" title="Image"></button>',
      '  </span>',
      '  <span class="ql-formats">',
      '    <button class="ql-clean" type="button" title="Clear formatting"></button>',
      '  </span>',
      "</div>",
    ].join("");
  }

  function buildInlineToolbar() {
    return [
      '<div class="quill-toolbar quill-toolbar-inline">',
      '  <span class="ql-formats">',
      '    <button class="ql-bold" type="button" title="Bold"></button>',
      '    <button class="ql-italic" type="button" title="Italic"></button>',
      '    <button class="ql-underline" type="button" title="Underline"></button>',
      '  </span>',
      '  <span class="ql-formats">',
      '    <button class="ql-link" type="button" title="Link"></button>',
      '  </span>',
      '  <span class="ql-formats">',
      '    <button class="ql-clean" type="button" title="Clear formatting"></button>',
      '  </span>',
      "</div>",
    ].join("");
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (typeof Quill === "undefined") return;

    const textareas = document.querySelectorAll("textarea[data-quill]");
    if (!textareas.length) return;

    const csrfToken = getCookie("csrftoken");

    textareas.forEach(function (textarea) {
      const isInline = textarea.getAttribute("data-quill-inline") === "true";

      const wrapper = document.createElement("div");
      wrapper.className = "quill-wrapper";
      wrapper.innerHTML =
        (isInline ? buildInlineToolbar() : buildFullToolbar()) +
        '<div class="quill-editor"></div>';

      textarea.parentNode.insertBefore(wrapper, textarea.nextSibling);
      textarea.style.display = "none";

      const editorEl = wrapper.querySelector(".quill-editor");
      const toolbarEl = wrapper.querySelector(".quill-toolbar");

      const modules = {
        toolbar: {
          container: toolbarEl,
        },
      };

      if (!isInline) {
        modules.toolbar.handlers = {
          image: function () {
            const input = document.createElement("input");
            input.type = "file";
            input.accept = "image/*";
            input.onchange = function () {
              const file = input.files[0];
              if (!file) return;
              if (!file.type.startsWith("image/")) {
                alert("Please choose an image file.");
                return;
              }
              const formData = new FormData();
              formData.append("image", file);

              fetch("/studio/upload-image/", {
                method: "POST",
                headers: { "X-CSRFToken": csrfToken },
                body: formData,
                credentials: "same-origin",
              })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                  if (data.url) {
                    const range = quill.getSelection(true) || {
                      index: quill.getLength(),
                    };
                    quill.insertEmbed(range.index, "image", data.url);
                    quill.setSelection(range.index + 1);
                  } else if (data.error) {
                    alert(data.error);
                  }
                })
                .catch(function () {
                  alert("Upload failed. Please try again.");
                });
            };
            input.click();
          },
        };
      }

      const quill = new Quill(editorEl, {
        theme: "snow",
        placeholder: textarea.getAttribute("placeholder") || "Write here…",
        modules: modules,
      });

      if (textarea.value) {
        quill.clipboard.dangerouslyPasteHTML(textarea.value);
      }

      const form = textarea.closest("form");
      if (form) {
        form.addEventListener("submit", function () {
          textarea.value = quill.root.innerHTML;
        });
      }
    });
  });
})();