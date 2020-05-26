require([
  "static/js/cm/lib/codemirror", "static/js/cm/mode/python/python", "static/js/cm/addon/hint/show-hint", "static/js/cm/addon/edit/closebrackets"
], function (CodeMirror) {
  var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    mode: {     // 语言模式
      name: "python",
      version: 3,
      singleLineStringErrors: false,
    },
    lineWrapping: true,
    indentUnit: 4,
    indentWithTabs: true, // 使用制表符进行智能缩进
    autoCloseBrackets: true,
    styleActiveLine: true, // 显示选中行的样式
    theme: "base16-light",
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"], 
  });
  editor.on("keypress", function () { editor.showHint() })
  editor.on("change", function () { editor.save() });
});
