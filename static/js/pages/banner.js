jQuery(function ($) {
    $(".chosen-select").chosen();
    $("select[name='banner_type']").on("change", function () {
        var content_type = $(this).val();
        console.log(content_type);
        if(content_type!=2) {
            $("#all_select_contents").show();
            $("#url_target").attr('type', "hidden");
            $("#select_target").html("");
            $("#select_target").chosen("destroy");
            $.ajax(
                {
                    type: "get",
                    url: "/select/content/list.html",
                    data: {"content_type": content_type, "req_page": "banner"},
                    dataType: 'json',
                    success: function (result) {
                        var data = result.data;
                        $.each(data, function (i) {
                            $("<option value='" + data[i].id + "'>" + data[i].title + "</option>").appendTo("#select_target");
                        });

                        $(".chosen-select").chosen();
                    }
                })
        }else{
            $("#url_target").attr('type', "text");
             $("#all_select_contents").hide();
        }
    });
});