$(function(){
    function get_and_render(){
        var region = jQuery('#dropdown-region').attr('region')
        var date_beg = jQuery('.custom-date-range .dpd1').val()
        var date_end = jQuery('.custom-date-range .dpd2').val()

        url = "/api/get_new_residence_total?"
        url += 'region=' + region + '&from=' + date_beg + '&to=' + date_end
    
        $.getJSON(url, function(json){
            console.log(json)
            var label_key = ["building_name","size","net_size","price", "price_per_ft2", "remark", "region", "age", "layout", "image_list"];
            var table = jQuery('#hidden-table-info')
            var oTable = table.dataTable();
            var oSettings = oTable.fnSettings();
            oTable.fnClearTable();
            var list = json;
            for (var i = 0; i < list.length; i++) {
                var vo = list[i]
                if (!vo) {continue;}
                var arr = ['<img src="/static/images/details_open.png">'];
                for(var j=0;j<label_key.length;j++){
                    var value = vo[label_key[j]]
                    if(label_key[j] == "price_per_ft2"){
                        if(value == ''){value = '-'}
                    }
                    else if(label_key[j] == "net_size"){
                        if(value == 0){value = '-'}
                    }
                    else if(label_key[j] == "size"){
                        if(value == 0){value = '-'}
                    }
                    else if(label_key[j] == "building_name"){
                        value = '<a target="_blank" href="http://www.malimalihome.net/residential/' + vo['_id'] + '">' + value + '</a>'
                    }
                    arr.push(value);
                }
                //console.log(arr)
                oTable.oApi._fnAddData(oSettings, arr);
            };
            oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
            oTable.fnDraw();
            //$.each(json.paymodeData, function(i, field){ 
                //console.log(i)
            //    select.append('<option value="' + field.payMode + '">' + field.payName + '</option>')
            //})console.log(json)
        })
    }

    get_and_render()

    jQuery('#query_button').click(function(){
        get_and_render()
    })

    jQuery('.dropdown-menu li a').click(function(){
        var val = $(this).html()
        var region = $(this).attr('region')
        jQuery('#dropdown-region').html(val + '<span class="caret"></span>')
        jQuery('#dropdown-region').attr('region', region)
    })
})