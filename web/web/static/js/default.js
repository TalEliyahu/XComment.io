function highlightJsChoicesMap(key) {
    let _map = {
        cpp: 'c',
        armasm: 'assembly',
        cs: 'csharp'
    }

    if(key in _map) {
        return _map[key];
    } else {
        return key;
    }
}

function makeEditor(textField) {
    let editor = CodeMirror.fromTextArea(textField, {
        lineNumbers: true,
        lineWrapping: true,
        styleSelectedText: true
    });
    editor.setSize(null, "100%");
    return editor;
}

function getMode(sourceContent) {
    let lang = hljs.highlightAuto(sourceContent).language;
    let mode = "javascript";
    mapped_lang_choice = highlightJsChoicesMap(lang);
    if(mapped_lang_choice in supported_langs && typeof lang != 'undefined') {
        mode = supported_langs[mapped_lang_choice];
    }
    return [mode, mapped_lang_choice];
}

function loadMode(mode, onLoadFn) {
    let script = document.createElement('script');
    script.onload = onLoadFn;
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.31.0/mode/" + mode +"/" + mode + ".js";
    document.body.appendChild(script);
}

function highlightCode(editor, mode) {
    editor.setOption("mode", mode);
}

function selectLangChoice(selectorNode, selected) {
    selectorNode.value = selected;
}

function highlightComments(editor) {

    let cursor, searchTerm;

    for(let i=0; i<highlightContent.length; i++) {
        searchTerm = highlightContent[i];
        cursor = editor.getSearchCursor(searchTerm)
        while(cursor.findNext()) {
            editor.markText(
                cursor.from(), cursor.to(), {className: "styled-background"});
        }

    }
}

let source = document.getElementById('id_source_content');
let results = document.getElementById('id_results_content');
let sourceEditor = makeEditor(source);
let resultsEditor = makeEditor(results);
let selectorNode = document.getElementById('id_language');
let mode_lang_choice = getMode(source.textContent);
let mode = mode_lang_choice[0];
let lang_choice = mode_lang_choice[1];

sourceEditor.on('change', function(editor, change) {
    console.log('content changed');
    doc = editor.getDoc();
    mode_lang_choice = getMode(doc.getValue());
    mode = mode_lang_choice[0];
    lang_choice = mode_lang_choice[1];
    loadMode(mode, function() {
        highlightCode(editor, mode);
        highlightCode(resultsEditor, mode);
        selectLangChoice(selectorNode, lang_choice);
    });
});
selectorNode.onchange = function() {
    mode = supported_langs[selectorNode.value];
    loadMode(mode, function() {
        highlightCode(sourceEditor, mode);
        highlightCode(resultsEditor, mode);
    });
}

loadMode(mode, function() {
    highlightCode(sourceEditor, mode);
    highlightCode(resultsEditor, mode);
});

highlightComments(sourceEditor);

