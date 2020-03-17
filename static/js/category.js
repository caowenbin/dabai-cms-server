function first_category(f_id, s_id, t_id) {
    $.ajax(
        {
            type: "post",
            url: "/admin/category/child.html",
            data: {"parent_id": "0", "_xsrf": getCookie("_xsrf")},
            dataType: 'json',
            success: function (result) {
                var first = $("#first_category");
                first.append("<option value=''>&nbsp;</option>");
                var data = result.data;

                $.each(data, function (i) {
                    var c_id = data[i].id;
                    if (f_id == c_id) {
                        $("<option value='" + c_id + "' selected >" + data[i].name + "</option>").appendTo("#first_category");
                    }
                    else {
                        $("<option value='" + c_id + "'>" + data[i].name + "</option>").appendTo("#first_category");
                    }
                });
                if (f_id == "" || f_id == undefined) {
                    second_category("", "", 1);
                }
                $(".chosen-select").chosen();
                if (f_id != "" && f_id != undefined) {
                    second_category(s_id, t_id, 1);
                }
            }
        })
};

function second_category(s_id, t_id, is_edit) {
    $("#second_category").html("");
    $("#second_category").chosen("destroy");
    $("#second_category").append("<option value=''>&nbsp;</option>");
    var parent_id = $('#first_category').val();
    if (parent_id != "") {
        $.ajax(
            {
                type: "post",
                url: "/admin/category/child.html",
                dataType: 'json',
                data: {"parent_id": parent_id, "_xsrf": getCookie("_xsrf")},
                success: function (result) {
                    var data = result.data;
                    $.each(data, function (i) {
                        var c_id = data[i].id;
                        if (s_id == c_id) {
                            $("<option value='" + c_id + "' selected >" + data[i].name + "</option>").appendTo("#second_category");
                        }
                        else {
                            $("<option value='" + c_id + "'>" + data[i].name + "</option>").appendTo("#second_category");
                        }

                    });
                    if (is_edit != 1 || is_edit == undefined) {
                        third_category("");
                    }
                    $(".chosen-select").chosen();
                    if (is_edit == 1) {
                        third_category(t_id);
                    }
                }
            })
    }
    else{
        third_category("");
    }
};

function third_category(t_id) {
    $("#third_category").html("");
    $("#third_category").chosen("destroy");
    $("#third_category").append("<option value=''>&nbsp;</option>");
    var parent_id = $('#second_category').val();
    if (parent_id != "") {
        $.ajax(
            {
                type: "post",
                dataType: 'json',
                url: "/admin/category/child.html",
                data: {"parent_id": parent_id, "_xsrf": getCookie("_xsrf")},
                success: function (result) {
                    var data = result.data;
                    $.each(data, function (i) {
                        var c_id = data[i].id;
                        if (t_id == c_id) {
                            $("<option value='" + c_id + "' selected >" + data[i].name + "</option>").appendTo("#third_category");
                        }
                        else {
                            $("<option value='" + c_id + "'>" + data[i].name + "</option>").appendTo("#third_category");
                        }
                    });
                    $(".chosen-select").chosen();
                }
            })
    }
    else{
         $(".chosen-select").chosen();
    }
};

function init_category(f_id, s_id, t_id){
    first_category(f_id, s_id, t_id);
    $('#first_category').bind("change", second_category);
    $('#second_category').bind("change", third_category);
}