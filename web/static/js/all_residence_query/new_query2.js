$(function(){
	//url = "/api/get_new_residence_coloane"
    //console.log(url)
	//$.getJSON(url, function(json){

        
    //})
    jQuery('#dropdown-menu-region li a').click(function(){
        var val = $(this).html()
        var region = $(this).attr('region')
        jQuery('#dropdown-region').html(val + '<span class="caret"></span>')
        jQuery('#dropdown-region').attr('region', region)
    })

    jQuery('#dropdown-menu-sort li a').click(function(){
        var val = $(this).html()
        var sort = $(this).attr('sort')
        jQuery('#dropdown-sort').html(val + '<span class="caret"></span>')
        jQuery('#dropdown-sort').attr('sort', sort)
    })

    function query_residence(query_infos){
        jQuery('#query_button').attr('disabled', 'disabled')

        query_info = query_infos.sql
        //console.log(query_info)
        query_page = query_infos.page
        url = "/api/all_residence_query"
        //data = JSON.parse(query_info)
        data = query_infos

        $.getJSON(url, data, function(json){
            console.log(json)
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
                                <h1 class=""><a target="_blank" href="http://www.malimalihome.net/residential/' + json['data'][i]['_id'] + '">' + json['data'][i]['building_name'] + '</a></h1>'
                //content += '<button type="button" class="btn btn-primary" data-toggle="modal" data-target=".charts-modal">Morris Chart in Bootstrap Modal</button>'
                content += '<div aria-hidden="true" aria-labelledby="myModalLabel" role="dialog" tabindex="-1" id="myModal' + i + '" class="modal fade charts-modal">\
                                        <div class="modal-dialog">\
                                            <div class="modal-content">\
                                                <div class="modal-header">\
                                                    <button aria-hidden="true" data-dismiss="modal" class="close" type="button">×</button>\
                                                    <h4 class="modal-title">' + json['data'][i]['building_name'] + '</h4>\
                                                </div>\
                                                <div class="modal-body">\
                                                    <div id="area-example' + i + '"></div>\
                                                </div>\
                                                <div class="modal-footer">\
                                                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
                                                </div>\
                                            </div>\
                                        </div>\
                                    </div>'
                content += '<p class=" auth-row"><strong><font color="red" size="5">$' + json['data'][i]['price'] +'</font></strong> 萬 |'                     
                //price_history少于1的话不展示曲线
                if (Object.keys(json['data'][i]['price_history']).length > 1){
                    content += '<a href="#myModal' + i + '" bid="' + i + '" data-toggle="modal"><font color="red">价格走势</font></a> |'                    
                }
                
                content += '<div aria-hidden="true" aria-labelledby="myModalLabel" role="dialog" tabindex="-1" id="myModal_price_per_ft2' + i + '" class="modal fade charts-modal-price-per-ft2">\
                                        <div class="modal-dialog">\
                                            <div class="modal-content">\
                                                <div class="modal-header">\
                                                    <button aria-hidden="true" data-dismiss="modal" class="close" type="button">×</button>\
                                                    <h4 class="modal-title">' + json['data'][i]['building_name'] + '</h4>\
                                                </div>\
                                                <div class="modal-body">\
                                                    <div id="area-example-price-per-ft2' + i + '"></div>\
                                                </div>\
                                                <div class="modal-footer">\
                                                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
                                                </div>\
                                            </div>\
                                        </div>\
                                    </div>'
                content += '<a href="#myModal_price_per_ft2' + i + '" bid="' + i + '" data-toggle="modal"><font color="red">樓盤呎價走势</font></a> |'                    
                
                //else
                //    content += '<p class=" auth-row"><a href="#myModal' + i + '" bid="' + i + '" data-toggle="modal"><strong><font color="red" size="5">$' + json['data'][i]['price'] +'</font></strong></a> 萬 |'

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
                jQuery('#result').append(content)
                jQuery('#c-slide'+i).carousel('pause')
            }

            

            //pagina
            var query_pagination = jQuery('#query_pagination')
            query_pagination.attr('class', 'pagination pagination-lg')
            query_pagination.empty()
            present_num_left = 3

            //json['page'] = 2
            //json['total_page'] = 3
            min = Math.max(1, (json['page'] - present_num_left * 2))
            max = Math.min(json['total_page'], min + present_num_left * 2)
            
            var i = min
            for(; i < json['page'] - present_num_left; ++i){
                console.log(i)
                max = Math.min(json['total_page'], i + present_num_left * 2)
                if(max >= json['total_page']){
                    break
                }
            }
            min = i;
            max = Math.min(json['total_page'], min + present_num_left * 2)
            prepage = Math.max(1, json['page'] - 1)
            nextpage = Math.min(json['total_page'], json['page'] + 1)
            query_pagination.append('<li><a href="#" page="' + prepage + '">«</a></li>')
            for(var i = min; i <= max; ++i){
                
                if(i == json['page'])
                    content = '<li class="active"><a href="#" page="' + i + '">' + i + '</a></li>'
                else{
                    content = '<li><a href="#" page="' + i + '">' + i + '</a></li>'
                }
                query_pagination.append(content)
                
            }
            query_pagination.append('<li><a href="#" page="' + nextpage + '">»</a></li>')
            /*
            if(json['total_page'] - json['page'] * 2){
                query_pagination.append('<li class="disabled"><a href="#">«</a></li>')
                query_pagination.append('<li class="active"><a href="#" page="1">1</a></li>')
                var i = 1
                for(;i<present_num&&i<json['total_page'];++i){
                    content = '<li><a href="#" page="' + (i+ 1) + '">' + (i+ 1) + '</a></li>'
                    query_pagination.append(content)
                }
                query_pagination.append('<li><a href="#" page="' + 2 + '">»</a></li>')
            }else if (json['page'] == 1){
                jQuery('#query_pagination').append('<li><a>«</a></li>')
            }*/
            //$("#graph-area-line").empty()

            jQuery('#query_button').removeAttr('disabled')
            $(".charts-modal").on('show.bs.modal', function (event) {
                var id = $(event.relatedTarget).attr('bid')

                price_data = []
                for(var key in json['data'][id]['price_history']){
                    item = {}
                    item['date'] = key
                    item['value'] = json['data'][id]['price_history'][key]
                    price_data.push(item)
                }
                //console.log(price_data)
                setTimeout(function(){
                    element_id = 'area-example' + id
                    var mr = Morris.Line({
                      element: element_id,
                      data: [],
                      xkey: 'date',
                      ykeys: ['value'],
                      labels: ['Price']
                    });
                    // When you open modal several times Morris charts over loading. So this is for destory to over loades Morris charts.
                    // If you have better way please share it. 

                    if($('#' + element_id).find('svg').length > 1){
                        // Morris Charts creates svg by append, you need to remove first SVG
                        $('#' + element_id + ' svg:first').remove();
                        // Also Morris Charts created for hover div by prepend, you need to remove last DIV
                        $(".morris-hover:last").remove();
                    }
                    //console.log(mr)
                    //console.log(price_data)
                    mr.setData(price_data)
                    
                    // Smooth Loading
                    //$('.js-loading').addClass('hidden');
                },1000);
            });

            $(".charts-modal-price-per-ft2").on('show.bs.modal', function (event) {
                var id = $(event.relatedTarget).attr('bid')
                
                var building = json['data'][id]['building']
                //console.log(building)
                $.getJSON('/api/get_key_residence?query_building=' + building, function(json){
                    //console.log(json)
                    price_data = []
                    for(var i = 0; i < json['date'].length; i++){
                        item = {}
                        item['date'] = json['date'][i]
                        item['value'] = json['avg'][i]
                        price_data.push(item)
                    }
                    //console.log(price_data)
                    setTimeout(function(){
                        element_id = 'area-example-price-per-ft2' + id
                        var mr = Morris.Line({
                          element: element_id,
                          data: [],
                          xkey: 'date',
                          ykeys: ['value'],
                          labels: ['Price']
                        });
                        // When you open modal several times Morris charts over loading. So this is for destory to over loades Morris charts.
                        // If you have better way please share it. 

                        if($('#' + element_id).find('svg').length > 1){
                            // Morris Charts creates svg by append, you need to remove first SVG
                            $('#' + element_id + ' svg:first').remove();
                            // Also Morris Charts created for hover div by prepend, you need to remove last DIV
                            $(".morris-hover:last").remove();
                        }
                        //console.log(mr)
                        //console.log(price_data)
                        mr.setData(price_data)
                        
                        // Smooth Loading
                        //$('.js-loading').addClass('hidden');
                    },1000);
                })
            });
        })
    }

    function get_query_info(page){
        var q_id = jQuery('.tab-pane.active').attr('id')
        var ret = new Object()
        ret['page'] = 1
        if(!isNaN(page)){
            ret['page'] = page
        }
        if(q_id == 'query'){
            var building = jQuery('#building').val()
            var region = jQuery('#dropdown-region').attr('region')
            var sort = jQuery('#dropdown-sort').attr('sort')
            var date_beg = jQuery('.custom-date-range .dpd1').val()
            var date_end = jQuery('.custom-date-range .dpd2').val()
            var price_per_ft2_low = jQuery('#price-per-ft2-low').val()
            
            var price_per_ft2_high = jQuery('#price-per-ft2-high').val()
            
            var price_low = jQuery('#price-low').val()
            
            var price_high = jQuery('#price-high').val()
            
            var size_low = jQuery('#size-low').val()
            
            var size_high = jQuery('#size-high').val()
            
            ret['building'] = building
            ret['region'] = region
            ret['sort'] = sort
            ret['date_beg'] = date_beg
            ret['date_end'] = date_end
            ret['price_per_ft2_low'] = price_per_ft2_low
            ret['price_per_ft2_high'] = price_per_ft2_high
            ret['price_low'] = price_low
            ret['price_high'] = price_high
            ret['size_low'] = size_low
            ret['size_high'] = size_high
            ret['query_type'] = 'query'
        }else{
            ret['sql'] = jQuery('#query_info').val()
            ret['query_type'] = 'query_by_sql'
        }
        return ret
    }
    
    jQuery('.query-button').click(function(){
        var ret = get_query_info()
        console.log(ret)
        query_residence(ret)
    })

    jQuery('a[page]').live('click', function(e){
        //console.log(jQuery(e.target).attr('page'))
        var page = parseInt(jQuery(e.target).attr('page'))
        var ret = get_query_info(page)
        console.log(ret)
        query_residence(ret)
    })

    
})