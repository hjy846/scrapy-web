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

var options_region = {
    chart: {
        zoomType: 'x',
        renderTo: "container_region"
    },
    title: {
        text: '地区成交數據'
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
        }]
    },
    series: [{
        type: 'column',
        name: '地区',
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
                fontSize: '8px',
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
        center: [50, 20],
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

function get_dsf_detail(){
        $.getJSON('/api/get_dsf_detail?dsf_type=total&date=201612', function(json){
            console.log(json)
            options_age.title.text += '(' + json.date + ')'
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
            console.log(options_age.series[0])
            chart_age = new Highcharts.Chart(options_age)

            options_price.title.text += '(' + json.date + ')'
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
            console.log(options_price.series[1])
            chart_price = new Highcharts.Chart(options_price)

            options_region.title.text += '(' + json.date + ')'
            options_region.xAxis.categories = json.region_categories
            options_region.series[0].data = new Array()
            options_region.series[1].data = new Array()
            for(var i = 0;i<json.region_categories.length;++i){
                d = new Object()
                d.name = json.region_categories[i]
                d.y = json.region[i]
                d.color = Highcharts.getOptions().colors[i]
                options_region.series[1].data.push(d)
                options_region.series[0].data.push(d)
            }
            console.log(options_region.series[1])
            chart_region = new Highcharts.Chart(options_region)
            /*
            volumn_chart.xAxis[0].categories = new Array()
            total = new Array();
            macau = new Array();
            taipa = new Array();
            coloane = new Array();
            for(var i = 0; i<json.length;i++){
                //console.log(json[i]['date'])
                
                volumn_chart.xAxis[0].categories.push(json[i]['date'])
                total.push(json[i]['total'])
                macau.push(json[i]['macau'])
                taipa.push(json[i]['taipa'])
                coloane.push(json[i]['coloane'])
            }
            volumn_chart.series[0].setData(total)
            volumn_chart.series[1].setData(macau)
            volumn_chart.series[2].setData(taipa)
            //console.log(coloane)
            volumn_chart.series[3].setData(coloane)
            */
        })
    }

get_dsf_detail()
//get_dsf_price()

});
