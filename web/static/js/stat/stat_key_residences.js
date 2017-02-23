if (top.location != location) {
    top.location.href = document.location.href ;
}


$(function(){
    //console.log('begin')
    //jQuery('.petrol').text(1276.3)
    //updateStatus()
/*
new_chart = new Highcharts.chart('container_price', {
    chart: {
        type: 'line',
        zoomType: 'x'
    },
    title: {
        text: '每月新放盘'
    },
    subtitle: {
        text: ''
    },
    tooltip: {
        shared: true
    },
    xAxis: {
        labels:{
            rotation:-45
        },
        categories: []
    },
    yAxis: {
        title: {
            text: ''
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: false
            },
            enableMouseTracking: true
        }
    },
    series: [
    ]
});
*/
var options_price = {
    chart: {
        type: 'line',
        zoomType: 'x',
        renderTo: "container_price"
    },
    title: {
        text: '重點樓盤呎價數據'
    },
    subtitle: {
        text: ''
    },
    tooltip: {
        shared: true
    },
    xAxis: {
        labels:{
            rotation:-45
        },
        categories: []
    },
    yAxis: {
        title: {
            text: '呎價'
        },
        labels:{
            format: '$ {value}',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: false
            },
            enableMouseTracking: true
        },
        series:{
            connectNulls:true
        }
    },
    series: [
    ]
}

var options_total = {
    chart: {
        type: 'line',
        zoomType: 'x',
        renderTo: "container_total"
    },
    title: {
        text: '重點樓盤放盤量數據'
    },
    subtitle: {
        text: ''
    },
    tooltip: {
        shared: true
    },
    xAxis: {
        labels:{
            rotation:-45
        },
        categories: []
    },
    yAxis: {
        title: {
            text: '放盤量'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: false
            },
            enableMouseTracking: true
        }
    },
    series: [
    ]
}


function get_key_residences_info(){
        $.getJSON('/api/get_key_residences_info', function(json){
            console.log(json)
            //new_chart.xAxis[0].categories = new Array()
            //options.xAxis.categories = new Array()
            options_price.xAxis.categories = json[0]['date']
            options_price.series = new Array()
            for(var i = 0; i<json.length;i++){
                //console.log(json[i]['date'])
                //total.push(json[i]['new'])
                options_price.series[i] = new Object()
                options_price.series[i].name = json[i]['_id']
                options_price.series[i].data = json[i]['avg']
                options_price.series[i].tooltip = {valuePrefix: '$'}
            }
            chart = new Highcharts.Chart(options_price)

            options_total.xAxis.categories = json[0]['date']
            options_total.series = new Array()
            for(var i = 0; i<json.length;i++){
                //console.log(json[i]['date'])
                //total.push(json[i]['new'])
                options_total.series[i] = new Object()
                options_total.series[i].name = json[i]['_id']
                options_total.series[i].data = json[i]['total']
            }
            chart = new Highcharts.Chart(options_total)
            //new_chart.series[0].setData(total)
            //new_chart.series[1].setData(macau)
            //new_chart.series[2].setData(taipa)
            //new_chart.series[4].setData(coloane)
            
        })
    }

get_key_residences_info()

});