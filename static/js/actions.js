var AdminModelActions = function(actionErrorMessage, actionConfirmations) {
    this.execute = function(name) {
        var selected = $('input.action-checkbox:checked').size();

        if (selected === 0) {
            layer.msg(actionErrorMessage, {
                time: 5000, //20s后自动关闭
                btn: ['知道了'],
                icon: 7
            });
            return false;
        }
        var $msg = actionConfirmations[name];

        if (!!$msg){
            var $bath_delete_index = layer.confirm($msg, {
                btn: ['确定', '取消'],
                title: false
            }, function () {
                return submit_form(name);
            }, function(){
                layer.close($bath_delete_index);
                return false;
            });
        }

        return false;
    };
    function submit_form(name){
        var $form = $('#action_form');
        $('#action', $form).val(name);

        $('input.action-checkbox', $form).remove();
        $('input.action-checkbox:checked').each(function() {
            $form.append($(this).clone());
        });

        $form.submit();
        return true
    };

    $(function() {
       $('table th input:checkbox').on('click', function () {
                var that = this;
                $(this).closest('table').find('tr > td:first-child input:checkbox')
                        .each(function () {
                            this.checked = that.checked;
                            $(this).closest('tr').toggleClass('selected');
                        });

            });
    });
};
