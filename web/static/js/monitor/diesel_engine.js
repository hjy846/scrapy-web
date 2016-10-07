if (top.location != location) {
    top.location.href = document.location.href ;
}
$(function(){
    //console.log('begin')
    //jQuery('.petrol').text(1276.3)
    //updateStatus()
    setInterval(updateStatus, 10000);  
    function updateStatus(){
        console.log('update')
        $.getJSON('/monitor/get_diesel_engine_status', function(json){
            console.log(json)
            jQuery('.petrol').text(json.saleinfo.petrol)
            jQuery('.diesel').text(json.saleinfo.diesel)
            jQuery('.tranxcount').text(json.saleinfo.tranxcount)
            jQuery('.salesamount').text(json.saleinfo.salesamount)
            var insertStatus = jQuery("#diesel-engine-status").text("")
            var statusMap = {"1":"锁定", "3":"空闲", "5":"授权中", "8":"加油中"}
            $.each(json.nozinfo, function(i, field){

                var state = new Array('<div class="col-md-3 col-sm-3">', 
                                    '<div class="panel">',
                                        '<div class="panel-body">',
                                            '<h4>', field.nozid, '<span class="text-muted small"> -', field.fuelname, '</span></h4>',
                                            '<div class="media small">',
                                                '<a class="pull-left" >',
                                                    '<img class="media-object" style="width:90px" src="/static/images/dispenser.png" alt="">',
                                                '</a>',
                                                '<div class="media-body small">',
                                                        '<strong>状态: </strong>', statusMap[field.state], '<br>',
                                                        '<strong>单价: </strong>', field.price, '<br>',
                                                        '<strong>升数: </strong>', field.volume, '<br>',
                                                        '<strong>金额: </strong>', field.amount, '<br>',
                                                        '<strong>泵码: </strong>', field.total, '<br>',
                                                '</div>',
                                            '</div>',
                                        '</div>',
                                    '</div>',
                                '</div>')
                var str = state.join('')
                insertStatus.append(str)
            })
            console.log('end')
        })
    }

});
