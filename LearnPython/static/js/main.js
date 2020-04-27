require([
    "static/js/cm/lib/codemirror", "static/js/cm/mode/python/python"
  ], function(CodeMirror) {
    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
      lineNumbers: true,
      mode: {
          name: "python",
          version: 3,
          singleLineStringErrors:false
      },
      lineNumbers: true,
      indentUnit: 4,
      matchBrackets: true
    });
    editor.on("change",function(){editor.save()});
  });
  