function insertHtml(html) {
    wwei_editor.execCommand('insertHtml', html);
    wwei_editor.undoManger.save();
    return true;
}
