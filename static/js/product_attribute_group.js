var step = {
        //SKU信息组合
        Creat_Table: function (product_properties) {
             var product_property_list;
            if(product_properties!=undefined && product_properties !="None"){
                product_property_list = product_properties;
            }
            else{
                product_property_list = {};
                 $('div#attribute_price_stock>table>tbody>tr').each(function () {
                     var ss = {};
                     $('input.total', this).each(function(){
                         var _t = $(this).attr("name");
                         if(_t == "is_default"){
                             var  c = $(this).attr("checked");
                             if(c!=undefined){
                                 ss[_t] = 1;
                             }
                             else{
                                 ss[_t] = 0;
                             }
                         }
                         else{
                             ss[_t] = $(this).val();
                         }

                     })
                     product_property_list[ss["key"]]=ss;
                        });
            }
            step.hebingFunction();
            var SKUObj = $("#attribute_select_contents h5");
            var arrayTile = new Array();//标题组数
            var arrayInfor = new Array();//盛放每组选中的CheckBox值的对象
            var propertiesInfo = new Array();
            var propertyNameInfo = new Array();
            var arrayColumn = new Array();//指定列，用来合并哪些列
            var columnIndex = 0;
            $.each(SKUObj, function (i, item) {
                var itemName = "Father_Item" + i;
                //选中的CHeckBox取值
                var order = new Array();
                // 选中的属性值
                var good_properties = new Array();
                var good_property_names = new Array();

                $("." + itemName + " input[type=checkbox]:checked").each(function () {
                    var current_this = $(this);
                    order.push(current_this.val());
                    good_properties.push(current_this.attr("properties"))
                    good_property_names.push(current_this.attr("property_names"))
                });
                if (order.length > 0) {
                    arrayColumn.push(columnIndex);
                    columnIndex++;

                    arrayTile.push(SKUObj.eq(i).html().replace("：", ""));
                    arrayInfor.push(order);
                    propertiesInfo.push(good_properties);
                    propertyNameInfo.push(good_property_names);
                }
            });

            //开始创建Table表
            $("#attribute_price_stock").html("");
            if(arrayTile.length>0) {
                var RowsCount = 0;
                var table_title = '<h5 class="red">*请输入对应的单价及库存</h5>';
                var table = $(table_title+"<table class=\"table table-bordered table-hover\"></table>");
                table.appendTo($("#attribute_price_stock"));
                var thead = $("<thead></thead>");
                thead.appendTo(table);
                var trHead = $("<tr></tr>");
                trHead.appendTo(thead);
                //创建表头
                $.each(arrayTile, function (index, item) {
                    var td = $("<th>" + item + "</th>");
                    td.appendTo(trHead);
                });
                var itemColumHead = $("<th class='width-100px'>单价(元)</th><th class='width-100px'>库存</th><th class='width-100px'>首款展示?</th> ");
                itemColumHead.appendTo(trHead);
                var tbody = $("<tbody></tbody>");
                tbody.appendTo(table);
                ////生成组合
                var result_data = step.doExchange(arrayInfor, propertiesInfo, propertyNameInfo);
                var zuheDate = result_data[0], propertiesDate=result_data[1], propertyNameDate=result_data[2];
                if (zuheDate.length > 0) {
                    //创建行
                    $.each(zuheDate, function (index, item) {
                        var td_array = item.split(",");
                        var tr = $("<tr></tr>");
                        tr.appendTo(tbody);
                        $.each(td_array, function (i, values) {
                            var td = $("<td>" + values + "</td>");
                            td.appendTo(tr);
                        });
                        var price="";
                        var stock="";
                        var is_default=0;
                        var id=0;
                        var p_str = propertiesDate[index];
                        var p_list = p_str.split("^");
                        var attrs = new Array();
                        for (var p in p_list) {
                            attrs.push(p_list[p].split(":")[1]);
                        }
                        attrs.sort();
                        var k = attrs.join('');
                        if(product_property_list!=undefined){
                            var value_list = product_property_list[k];
                            if(value_list != undefined) {
                                price = value_list["price"];
                                stock = value_list["stock"];
                                is_default = value_list["is_default"];
                                id=value_list["property_id"];
                            }
                        }
                        if(index==0){
                            is_default=1;
                        }

                        var td1 = $("<td >" +
                            "<input name=\"property_id\" type=\"hidden\" class='total' value=\""+ id +"\">"+
                            "<input name=\"key\" type=\"hidden\" class='total' value=\""+ k +"\">"+
                            "<input name=\"properties\" type=\"hidden\" value=\""+ propertiesDate[index]+"\">"+
                            "<input name=\"property_names\" type=\"hidden\" value=\""+ propertyNameDate[index]+"\">"+
                            "<input name=\"price\" data-easyform='money;' data-message='价格必须为数字' data-easytip='class:easy-blue;position:bottom;' class='width-100px total'type=\"text\" value=\""+price+"\">" +
                            "</td>");
                        td1.appendTo(tr);
                        var td2 = $("<td ><input name=\"stock\" data-easyform='number;' data-message='库存必须为数字' data-easytip='class:easy-blue;position:top;' class='width-100px total' type=\"text\" value=\""+stock+"\"></td>");
                        td2.appendTo(tr);
                        var td3_str;
                        if(is_default==1){
                            td3_str = "<input name=\"is_default\" type=\"radio\" class='total' checked value=\""+index+"\">";
                        }
                        else{
                            td3_str = "<input name=\"is_default\" type=\"radio\" class='total' value=\""+index+"\">";
                        }
                         var td3 = $("<td class='text-center'>" +td3_str +"</td>");
                        td3.appendTo(tr);
                    });
                }
                //结束创建Table表
                arrayColumn.pop();//删除数组中最后一项
                //合并单元格
                $(table).mergeCell({
                    // 目前只有cols这么一个配置项, 用数组表示列的索引,从0开始
                    cols: arrayColumn
                });
            }
        },//合并行
        hebingFunction: function () {
            $.fn.mergeCell = function (options) {
                return this.each(function () {
                    var cols = options.cols;
                    for (var i = cols.length - 1; cols[i] != undefined; i--) {
                        // fixbug console调试
                        // console.debug(cols[i]);
                        mergeCell($(this), cols[i]);
                    }
                    dispose($(this));
                });
            };
            function mergeCell($table, colIndex) {
                $table.data('col-content', ''); // 存放单元格内容
                $table.data('col-rowspan', 1); // 存放计算的rowspan值 默认为1
                $table.data('col-td', $()); // 存放发现的第一个与前一行比较结果不同td(jQuery封装过的), 默认一个"空"的jquery对象
                $table.data('trNum', $('tbody tr', $table).length); // 要处理表格的总行数, 用于最后一行做特殊处理时进行判断之用
                // 进行"扫面"处理 关键是定位col-td, 和其对应的rowspan
                $('tbody tr', $table).each(function (index) {
                    // td:eq中的colIndex即列索引
                    var $td = $('td:eq(' + colIndex + ')', this);
                    // 取出单元格的当前内容
                    var currentContent = $td.html();
                    // 第一次时走此分支
                    if ($table.data('col-content') == '') {
                        $table.data('col-content', currentContent);
                        $table.data('col-td', $td);
                    } else {
                        // 上一行与当前行内容相同
                        if ($table.data('col-content') == currentContent) {
                            // 上一行与当前行内容相同则col-rowspan累加, 保存新值
                            var rowspan = $table.data('col-rowspan') + 1;
                            $table.data('col-rowspan', rowspan);
                            // 值得注意的是 如果用了$td.remove()就会对其他列的处理造成影响
                            $td.hide();
                            // 最后一行的情况比较特殊一点
                            // 比如最后2行 td中的内容是一样的, 那么到最后一行就应该把此时的col-td里保存的td设置rowspan
                            if (++index == $table.data('trNum'))
                                $table.data('col-td').attr('rowspan', $table.data('col-rowspan'));
                        } else { // 上一行与当前行内容不同
                            // col-rowspan默认为1, 如果统计出的col-rowspan没有变化, 不处理
                            if ($table.data('col-rowspan') != 1) {
                                $table.data('col-td').attr('rowspan', $table.data('col-rowspan'));
                            }
                            // 保存第一次出现不同内容的td, 和其内容, 重置col-rowspan
                            $table.data('col-td', $td);
                            $table.data('col-content', $td.html());
                            $table.data('col-rowspan', 1);
                        }
                    }
                });
            }

            // 同样是个private函数 清理内存之用
            function dispose($table) {
                $table.removeData();
            }
        },
        //组合数组
        doExchange: function (doubleArrays, propertiesInfo, propertyNameInfo) {
            var len = doubleArrays.length;
            if (len >= 2) {
                var arr1 = doubleArrays[0];
                var arr2 = doubleArrays[1];
                var arr1_properties  =propertiesInfo[0];
                var arr2_properties  =propertiesInfo[1];

                var arr1_property_name  =propertyNameInfo[0];
                var arr2_property_name  =propertyNameInfo[1];

                var len1 = arr1.length;
                var len2 = arr2.length;
                var newlen = len1 * len2;
                var temp = new Array(newlen);
                var pro_temp = new Array(newlen);
                var pro_name_temp = new Array(newlen);

                var index = 0;
                for (var i = 0; i < len1; i++) {
                    for (var j = 0; j < len2; j++) {
                        temp[index] = arr1[i] + "," + arr2[j];
                        pro_temp[index] = arr1_properties[i] + "^" + arr2_properties[j];
                        pro_name_temp[index] = arr1_property_name[i] + "^" + arr2_property_name[j];
                        index++;
                    }
                }
                var new_len_temp = len - 1;
                var newArray = new Array(new_len_temp);
                var per_newArray = new Array(new_len_temp);
                var per_name_newArray = new Array(new_len_temp);

                newArray[0] = temp;
                per_newArray[0] = pro_temp;
                per_name_newArray[0] = pro_name_temp;
                if (len > 2) {
                    var _count = 1;
                    for (var i = 2; i < len; i++) {
                        newArray[_count] = doubleArrays[i];
                        per_newArray[_count] = propertiesInfo[i];
                        per_name_newArray[_count] = propertyNameInfo[i];
                        _count++;
                    }
                }
                return step.doExchange(newArray, per_newArray, per_name_newArray);
            }
            else {
                return [doubleArrays[0], propertiesInfo[0], propertyNameInfo[0]];
            }
        }
    }

$(function () {
    //SKU信息
    $("#attribute_select_contents label").bind("change", function () {
        step.Creat_Table();
    });

})