if (top.location != location) {
    top.location.href = document.location.href ;
}


$(function(){
    //console.log('begin')
    //jQuery('.petrol').text(1276.3)
    //updateStatus() 

volumn_chart = new Highcharts.chart('container_volumn', {
    chart: {
        type: 'line',
        zoomType: 'x'
    },
    title: {
        text: '楼花成交数量'
    },
    subtitle: {
        text: 'Source: dsf.gov.mo'
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
    series: [{
        name: 'Total',
        data: []
    }, 
    {
        name: 'Macau',
        data: []
    }, 
    {
        name: 'Taipa',
        data: []
    }, {
        name: 'Coloane',
        data: []
    }]
});

price_chart = new Highcharts.chart('container_price', {
    chart: {
        type: 'line',
        zoomType: 'x'
    },
    title: {
        text: '楼花成交价格'
    },
    subtitle: {
        text: 'Source: dsf.gov.mo'
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
    series: [{
        name: 'Total',
        data: []
    }, 
    {
        name: 'Macau',
        data: []
    }, 
    {
        name: 'Taipa',
        data: []
    }, {
        name: 'Coloane',
        data: []
    }]
});

function get_dsf_volumn(){
        $.getJSON('/api/dsf_louhua_volumn_price_query?query=volumn', function(json){
            //console.log(json)
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
        })
    }

    function get_dsf_price(){
        $.getJSON('/api/dsf_louhua_volumn_price_query?query=avage_price', function(json){
            //console.log(json)
            //console.log(json)
            price_chart.xAxis[0].categories = new Array()
            total = new Array();
            macau = new Array();
            taipa = new Array();
            coloane = new Array();
            for(var i = 0; i<json.length;i++){
                //console.log(json[i]['date'])
                
                price_chart.xAxis[0].categories.push(json[i]['date'])
                total.push(json[i]['total'])
                macau.push(json[i]['macau'])
                taipa.push(json[i]['taipa'])
                coloane.push(json[i]['coloane'])
            }
            price_chart.series[0].setData(total)
            price_chart.series[1].setData(macau)
            price_chart.series[2].setData(taipa)
            price_chart.series[3].setData(coloane)
        })
    }

get_dsf_volumn()
get_dsf_price()

});