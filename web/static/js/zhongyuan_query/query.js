

$(function(){
    //url = "/api/get_new_residence_coloane"
    //console.log(url)
    //$.getJSON(url, function(json){

        
    //})
    $('#dynamic-table').dataTable( {
        "aaSorting": [[ 2, "asc" ]]
    } );

    jQuery('#query_button').click(function(){
        //query_info = jQuery('#query_info').val()
        url = "/api/zhongyuan_query"
        //data = JSON.parse(query_info)
        //data = {'params':query_info}

        var region = jQuery('#dropdown-region').attr('region')
        var building = jQuery('#building').val()
        var date_beg = jQuery('.custom-date-range .dpd1').val()
        var date_end = jQuery('.custom-date-range .dpd2').val()
        data = {"building":building, "date_beg": date_beg, "date_end": date_end, "region":region}
        $.getJSON(url, data, function(json){

            if(json.errorno != 0){
                alert(json.errormsg)
                jQuery('#query_button').removeAttr('disabled')
                return
            }
            if(json['data'].length == 0){
                alert('no result')
                jQuery('#query_button').removeAttr('disabled')
                return
            }
            jQuery('#result').removeAttr('class')
            //jQuery('#dynamic-table tbody').empty()
            //console.log(json['data'])
            var label_key = ["building","block_floor","update_time","price", "price_per_ft2", "region", "remark"];
            var table = jQuery('#dynamic-table')
            var oTable = table.dataTable();
            var oSettings = oTable.fnSettings();
            oTable.fnClearTable();
            var list = json['data'];
            for (var i = 0; i < list.length; i++) {
                var vo = list[i]
                if (!vo) {continue;}
                var arr = [];
                for(var j=0;j<label_key.length;j++){
                    if(!vo.hasOwnProperty(label_key[j])){
                        arr.push('');
                    }
                    else{
                        arr.push(vo[label_key[j]]);
                    }
                    
                }
                //console.log(arr)
                oTable.oApi._fnAddData(oSettings, arr);
            };
            oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
            oTable.fnDraw();
        })
        
    })

    jQuery('.dropdown-menu li a').click(function(){
        var val = $(this).html()
        var region = $(this).attr('region')
        jQuery('#dropdown-region').html(val + '<span class="caret"></span>')
        jQuery('#dropdown-region').attr('region', region)
    })
})