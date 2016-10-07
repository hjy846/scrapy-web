$(function(){
	url = "/api/get_new_residence_total"
    console.log(url)
	$.getJSON(url, function(json){

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
                arr.push(vo[label_key[j]]);
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


})