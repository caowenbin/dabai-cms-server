var child_data_tip;
function verify_form_data() {

    if ($('div#uploader ul.filelist>li>span.success').length == 0) {
        child_data_tip.show();
        return false;
    }
    return true;
}

jQuery(function ($) {
    child_data_tip = $('#filePicker').easytip();
});