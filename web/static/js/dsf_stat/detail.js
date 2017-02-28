if (top.location != location) {
    top.location.href = document.location.href ;
}


$(function(){
    //console.log('begin')
    //jQuery('.petrol').text(1276.3)
    //updateStatus() 



var options_age = {
    chart: {
        zoomType: 'x',
        renderTo: "container_age"
    },
    title: {
        text: '樓齡成交數據'
    },
    xAxis: {
        type: 'category',
        categories: []
    },
    legend: {
        enabled: false
    },
    yAxis: {
        title: {
            text: '成交宗數'
        }
    },
    labels: {
        items: [{
            html: '',
            style: {
                left: '50px',
                top: '18px',
                color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
            }
        }]
    },
    series: [{
        type: 'column',
        name: '樓齡',
        data: [['1',3],['1',4],['2',5],['4',1],['2',2]],
        colorByPoint: true,
        dataLabels: {
            enabled: true,
            rotation: 0,
            color: '#FFFFFF',
            align: 'center',
            format: '{point.y:f}', // one decimal
            y: -1, // 10 pixels down from the top
            style: {
                fontSize: '13px',
                fontFamily: 'Verdana, sans-serif'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:f}</b>宗<br/>'
        },
    }, {
        type: 'pie',
        name: '佔比',
        data: [{
            name: 'Jane',
            y: 13,
            color: Highcharts.getOptions().colors[0] // Jane's color
        }, {
            name: 'John',
            y: 23,
            color: Highcharts.getOptions().colors[1] // John's color
        }, {
            name: 'Joe',
            y: 19,
            color: Highcharts.getOptions().colors[2] // Joe's color
        }],
        center: [50, 50],
        size: 100,
        showInLegend: false,
        dataLabels: {
            enabled: false
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        }
    }]
}

var options_price = {
    chart: {
        zoomType: 'x',
        renderTo: "container_price"
    },
    title: {
        text: '成交價格數據'
    },
    xAxis: {
        categories: []
    },
    legend: {
        enabled: false
    },
    yAxis: {
        title: {
            text: '成交宗數'
        }
    },
    labels: {
        items: [{
            html: '',
            style: {
                left: '50px',
                top: '18px',
                color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
            }
        }],

    },
    series: [{
        type: 'column',
        name: '平米價格',
        data: [3, 2, 1, 3, 4],
        colorByPoint: true,
        dataLabels: {
            enabled: true,
            rotation: 0,
            color: '#FFFFFF',
            align: 'center',
            format: '{point.y:f}', // one decimal
            y: -1, // 10 pixels down from the top
            style: {
                fontSize: '10px',
                fontFamily: 'Verdana, sans-serif'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:f}</b>宗<br/>'
        }
    }, {
        type: 'pie',
        name: '佔比',
        data: [{
            name: 'Jane',
            y: 13,
            color: Highcharts.getOptions().colors[0] // Jane's color
        }, {
            name: 'John',
            y: 23,
            color: Highcharts.getOptions().colors[1] // John's color
        }, {
            name: 'Joe',
            y: 19,
            color: Highcharts.getOptions().colors[2] // Joe's color
        }],
        center: [50, 50],
        size: 100,
        showInLegend: false,
        dataLabels: {
            enabled: false
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        }
    }]
}

var options_total_price = {
    chart: {
        zoomType: 'x',
        renderTo: "container_total_price"
    },
    title: {
        text: '成交總價數據'
    },
    subtitle: {
        text: '只有統計到區的數據，跟實際成交數據有出入，僅供參考'
    },
    xAxis: {
        categories: []
    },
    legend: {
        enabled: false
    },
    yAxis: {
        title: {
            text: '成交宗數'
        }
    },
    labels: {
        items: [{
            html: '',
            style: {
                left: '50px',
                top: '18px',
                color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
            }
        }],

    },
    series: [{
        type: 'column',
        name: '總價',
        data: [3, 2, 1, 3, 4],
        colorByPoint: true,
        dataLabels: {
            enabled: true,
            rotation: 0,
            color: '#FFFFFF',
            align: 'center',
            format: '{point.y:f}', // one decimal
            y: -1, // 10 pixels down from the top
            style: {
                fontSize: '10px',
                fontFamily: 'Verdana, sans-serif'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:f}</b>宗<br/>'
        }
    }, {
        type: 'pie',
        name: '佔比',
        data: [{
            name: 'Jane',
            y: 13,
            color: Highcharts.getOptions().colors[0] // Jane's color
        }, {
            name: 'John',
            y: 23,
            color: Highcharts.getOptions().colors[1] // John's color
        }, {
            name: 'Joe',
            y: 19,
            color: Highcharts.getOptions().colors[2] // Joe's color
        }],
        center: [350, 50],
        size: 100,
        showInLegend: false,
        dataLabels: {
            enabled: false
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        }
    }]
}

var options_region = {
    chart: {
        renderTo: 'container_region',
        zoomType: 'xy'
    },
    title: {
        text: '地區數據'
    },
    subtitle: {
        text: 'Source: dsf.gov.mo'
    },
    xAxis: [{
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        crosshair: true
    }],
    yAxis: [{ // Primary yAxis
        labels: {
            format: '{value} 宗',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        },
        title: {
            text: '地區成交量',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        }

    }, { // Secondary yAxis
        gridLineWidth: 0,
        title: {
            text: '地區成交平方價',
            style: {
                color: Highcharts.getOptions().colors[1]
            }
        },
        labels: {
            format: '{value} 萬/平方',
            style: {
                color: Highcharts.getOptions().colors[1]
            }
        },
        opposite: true

    }, { // Tertiary yAxis
        gridLineWidth: 0,
        title: {
            text: '地區成交平均面積',
            style: {
                color: Highcharts.getOptions().colors[2]
            }
        },
        labels: {
            format: '{value} 平方',
            style: {
                color: Highcharts.getOptions().colors[2]
            }
        },
        opposite: true
    }],
    tooltip: {
        shared: true
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        x: 80,
        verticalAlign: 'top',
        y: 55,
        floating: true,
        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
    },
    series: [{
        name: '地區成交量',
        type: 'column',
        yAxis: 0,
        data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4],
        tooltip: {
            valueSuffix: ' 宗'
        }

    }, {
        name: '地區成交平方價',
        type: 'column',
        yAxis: 1,
        data: [1016, 1016, 1015, 1015, 1012, 1009, 1009, 1010, 1013, 1016, 1018, 1016],
        
        
        tooltip: {
            valuePrefix: '$ ',
            valueSuffix: ' 萬/平方'
        }

    }, {
        name: '地區成交平均面積',
        type: 'column',
        yAxis: 2,
        data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6],
        tooltip: {
            valueSuffix: ' 平方'
        }
    }]
}

jQuery('#query_button').click(function(){
    url = "/api/get_dsf_detail"

    var dsf_type = jQuery('#dropdown-dsf-type').attr('dsf-type')
    var query_date = jQuery('#query_date').val()
    
    data = {"date":query_date, "dsf_type": dsf_type}
    //console.log(data)
    $.getJSON(url, data, function(json){
        //console.log(json)
        //options_age.title.text += '(' + json.date + ')'
            options_age.xAxis.categories = json.age_categories
            options_age.series[0].data = new Array()
            options_age.series[1].data = new Array()
            for(var i = 0;i<json.age_categories.length;++i){
                pd = new Object()
                pd.name = json.age_categories[i]
                pd.y = json.age[i]
                pd.color = Highcharts.getOptions().colors[i]
                options_age.series[1].data.push(pd)
                options_age.series[0].data.push(pd)
            }
            //console.log(options_age.series[0])
            chart_age = new Highcharts.Chart(options_age)

            //options_price.title.text += '(' + json.date + ')'
            options_price.xAxis.categories = json.price_categories
            options_price.series[0].data = new Array()
            options_price.series[1].data = new Array()
            for(var i = 0;i<json.price_categories.length;++i){
                d = new Object()
                d.name = json.price_categories[i]
                d.y = json.price[i]
                d.color = Highcharts.getOptions().colors[i]
                options_price.series[1].data.push(d)
                options_price.series[0].data.push(d)
            }
            //console.log(options_price.series[1])
            chart_price = new Highcharts.Chart(options_price)

            options_total_price.xAxis.categories = json.total_price_categories
            options_total_price.series[0].data = new Array()
            options_total_price.series[1].data = new Array()
            for(var i = 0;i<json.total_price_categories.length;++i){
                d = new Object()
                d.name = json.total_price_categories[i]
                d.y = json.total_price[i]
                d.color = Highcharts.getOptions().colors[i]
                options_total_price.series[1].data.push(d)
                options_total_price.series[0].data.push(d)
            }
            //console.log(options_price.series[1])
            chart_total_price = new Highcharts.Chart(options_total_price)
            
            //options_region.title.text += '(' + json.date + ')'
            options_region.xAxis[0].categories = json.region_categories
            options_region.series[0].data = json.region
            options_region.series[1].data = json.region_price
            options_region.series[2].data = json.region_size
            
            chart_region = new Highcharts.Chart(options_region)
    })

})

jQuery('.dropdown-menu li a').click(function(){
        var val = $(this).html()
        var dsf_type = $(this).attr('dsf-type')
        jQuery('#dropdown-dsf-type').html(val + '<span class="caret"></span>')
        jQuery('#dropdown-dsf-type').attr('dsf-type', dsf_type)
    })

function get_dsf_detail(){
        $.getJSON('/api/get_dsf_detail?dsf_type=total&date=201701', function(json){
            console.log(json)
            //options_age.title.text += '(' + json.date + ')'
            options_age.xAxis.categories = json.age_categories
            options_age.series[0].data = new Array()
            options_age.series[1].data = new Array()
            for(var i = 0;i<json.age_categories.length;++i){
                pd = new Object()
                pd.name = json.age_categories[i]
                pd.y = json.age[i]
                pd.color = Highcharts.getOptions().colors[i]
                options_age.series[1].data.push(pd)
                options_age.series[0].data.push(pd)
            }
            //console.log(options_age.series[0])
            chart_age = new Highcharts.Chart(options_age)

            //options_price.title.text += '(' + json.date + ')'
            options_price.xAxis.categories = json.price_categories
            options_price.series[0].data = new Array()
            options_price.series[1].data = new Array()
            for(var i = 0;i<json.price_categories.length;++i){
                d = new Object()
                d.name = json.price_categories[i]
                d.y = json.price[i]
                d.color = Highcharts.getOptions().colors[i]
                options_price.series[1].data.push(d)
                options_price.series[0].data.push(d)
            }

            chart_price = new Highcharts.Chart(options_price)
            
            options_total_price.xAxis.categories = json.total_price_categories
            options_total_price.series[0].data = new Array()
            options_total_price.series[1].data = new Array()
            for(var i = 0;i<json.total_price_categories.length;++i){
                d = new Object()
                d.name = json.total_price_categories[i]
                d.y = json.total_price[i]
                d.color = Highcharts.getOptions().colors[i]
                options_total_price.series[1].data.push(d)
                options_total_price.series[0].data.push(d)
            }
            //console.log(options_price.series[1])
            chart_total_price = new Highcharts.Chart(options_total_price)

            //options_region.title.text += '(' + json.date + ')'
            options_region.xAxis[0].categories = json.region_categories
            options_region.series[0].data = json.region
            options_region.series[1].data = json.region_price
            options_region.series[2].data = json.region_size
            
            chart_region = new Highcharts.Chart(options_region)
            
        })
    }

get_dsf_detail()
//get_dsf_price()

});
