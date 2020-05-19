require([
  "static/js/cm/lib/codemirror", "static/js/cm/mode/python/python", "static/js/cm/addon/hint/show-hint", "static/js/cm/addon/edit/closebrackets"
], function (CodeMirror) {
  var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    mode: {
      name: "python",
      version: 3,
      singleLineStringErrors: false
    },
    lineNumbers: true,
    indentUnit: 4,
    autoCloseBrackets: true,
    theme: "base16-light"
  });
  editor.on("keypress", function () { editor.showHint() })
  editor.on("change", function () { editor.save() });
});
