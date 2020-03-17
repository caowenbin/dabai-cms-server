var child_data_tip;
function verify_form_data() {
    if ($('.inline-field-list input[name="attribute_item_name"]').val() == undefined) {
        child_data_tip.show();
        return false;
    }
    return true;
}

jQuery(function ($) {

    $("#attribute-item-button").bind('click', function (e) {
        var $template = $($('.inline-field-template').html());
        $("input[name='attribute_item_name']", $template).each(function (e) {
            $(this).attr('type', "text");

        });
        $(".inline-field-list").append($template);
    });
    $('body').on('click', '.inline-remove-field', function (e) {
        e.preventDefault();

        var form = $(this).closest('.inline-field');
        form.remove();
    });
    child_data_tip = $('#attribute-item-button').easytip();
});