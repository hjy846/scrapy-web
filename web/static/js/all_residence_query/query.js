$(function(){
	//url = "/api/get_new_residence_coloane"
    //console.log(url)
	//$.getJSON(url, function(json){

        
    //})

    jQuery('#query_button').click(function(){
        jQuery('#query_button').attr('disabled', 'disabled')
        query_info = jQuery('#query_info').val()
        console.log(query_info)
        url = "/api/all_residence_query"
        //data = JSON.parse(query_info)
        data = {'params':query_info}

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
            jQuery('#result').empty()
            for(var i = 0; i <json['data'].length; ++i){

                content = '<div class="panel">\
                    <div class="panel-body">\
                        <div class="row">\
                            <div class="col-md-3">\
                                <section class="panel">\
                                    <div class="carousel panel-body" id="c-slide' + i + '">\
                                        <ol class="carousel-indicators out">'
                content += '<li data-target="#c-slide'+i+'" data-slide-to="0" class="active"></li>'
                if(json['data'][i]['image_list'].length !=0){
                    for(var j=1;j<json['data'][i]['image_list'].length;++j){
                        content += '<li data-target="#c-slide'+i+'" data-slide-to="'+j+'" class=""></li>'
                    }
                }
                content += '</ol><div class="carousel-inner"><div class="item text-center active">'
                if(json['data'][i]['image_list'].length ==0){
                    content += '<img src="/static/images/default_noimage.png"></div></div>'
                }else{
                    content += '<img src="' + json['data'][i]['image_list'][0] + '"></div>'
                    for (var j=1;j<json['data'][i]['image_list'].length;++j){
                        content += '<div class="item text-center">\
                                                <img src="' + json['data'][i]['image_list'][j] + '">\
                                            </div>'
                    }
                    content += '</div>'
                }
                content += '<a class="left carousel-control" href="#c-slide' + i + '" data-slide="prev">\
                                            <i class="fa fa-angle-left"></i>\
                                        </a>\
                                        <a class="right carousel-control" href="#c-slide' + i + '" data-slide="next">\
                                            <i class="fa fa-angle-right"></i>\
                                        </a></div></section></div>'
                content += '<div class="col-md-9">\
                                <h1 class=""><a href="#">' + json['data'][i]['building_name'] + '</a></h1>'
                content += '<p class=" auth-row"><strong><font color="red" size="5">$' + json['data'][i]['price'] +'</font></strong> 萬 |'
                if(json['data'][i]['size']){
                    content += '建築<font color="red">'+json['data'][i]['size']+'</font>|'
                }
                if(json['data'][i]['net_size']){
                    content += '實用<font color="red">'+json['data'][i]['net_size']+'</font>|'
                }
                if(json['data'][i]['layout']){
                    content += json['data'][i]['layout'] + '|'
                }
                if(json['data'][i]['price_per_ft2']){
                    content += '<font color="red">' + json['data'][i]['price_per_ft2'] + '</font>/呎|'
                }
                if(json['data'][i]['age']){
                    content += '樓齡:<font color="red">' + json['data'][i]['age'] + '</font>'
                }
                if(json['data'][i]['region']){
                    content += json['data'][i]['region'] + '|'
                }
                content += json['data'][i]['update_time']
                content += '</p>'
                content += '<p>' + json['data'][i]['remark'] + '</p></div></div>\
                    \
                </div>\
            </div>'
                                    /*
                            
                            
                                       
                            
                            

                            
                        
                        <div class="col-md-4">
                            <div id="graph-area-line"></div>
                        </div>
                        
                    </div>
                    
                </div>
            </div>"*/
                //console.log(content)
                jQuery('#result').append(content)
                jQuery('#c-slide'+i).carousel('pause')
            }
            jQuery('#query_button').removeAttr('disabled')
        })
    })
})