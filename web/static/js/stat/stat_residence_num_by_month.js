if (top.location != location) {
    top.location.href = document.location.href ;
}


$(function(){
    //console.log('begin')
    //jQuery('.petrol').text(1276.3)
    //updateStatus() 

total_chart = Highcharts.chart('container_total', {
    chart: {
        zoomType: 'xy'
    },
    title: {
        text: '放盤量和均價'
    },
    subtitle: {
        text: ''
    },
    xAxis: [{
        categories: [],
        crosshair: true
    }],
    yAxis: [{ // Primary yAxis
        labels: {
            
            style: {
                color: Highcharts.getOptions().colors[1]
            }
        },
        title: {
            text: '放盤量',
            style: {
                color: Highcharts.getOptions().colors[1]
            }
        }
    }, { // Secondary yAxis
        title: {
            text: '呎價',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        },
        labels: {
            format: '$ {value}',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        },
        opposite: true
    }],
    tooltip: {
        shared: true
    },
    series: [{
        type: 'column',
        name: '全澳放盤量',
        data: []
    }, {
        type: 'column',
        name: '澳門放盤量',
        data: []
    }, {
        type: 'column',
        name: '氹仔放盤量',
        data: []
    }, {
        type: 'column',
        name: '路環放盤量',
	visible: false,
        data: []
    }, {
        name: '全澳均價',
        type: 'spline',
        yAxis: 1,
        data: [],
        tooltip: {
            valuePrefix: '$'
        }
    }, {
        name: '澳門均價',
        type: 'spline',
        yAxis: 1,
        data: [],
        tooltip: {
            valuePrefix: '$'
        }
    },{
        name: '氹仔均價',
        type: 'spline',
        yAxis: 1,
        data: [],
        tooltip: {
            valuePrefix: '$'
        }
    },{
        name: '路環均價',
        type: 'spline',
        yAxis: 1,
        data: [],
	visible: false,
        tooltip: {
            valuePrefix: '$'
        }
    }]
});

new_chart = new Highcharts.chart('container_new', {
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
    series: [{
        name: '全部',
        data: []
    }, 
    {
        name: '澳門',
        data: []
    }, 
    {
        name: '氹仔',
        data: []
    }, 
    {
        name: '路環',
        data: []
    }
    ]
});


function get_total_residence_num_by_month(){
        $.getJSON('/api/get_residence_num_by_month', function(json){
            console.log(json)
            total_chart.xAxis[0].categories = new Array()
            total = new Array();
            macau = new Array();
            taipa = new Array();
            coloane = new Array();
            avg_total = new Array();
            avg_macau = new Array();
            avg_taipa = new Array();
            avg_coloane = new Array();
            for(var i = 0; i<json.length;i++){
                //console.log(json[i]['date'])
                
                total_chart.xAxis[0].categories.push(json[i]['date'])
                total.push(json[i]['total'])
                macau.push(json[i]['macau'])
                taipa.push(json[i]['taipa'])
                coloane.push(json[i]['coloane'])
                avg_total.push(json[i]['avg_total'])
                avg_macau.push(json[i]['avg_macau'])
                avg_taipa.push(json[i]['avg_taipa'])
                avg_coloane.push(json[i]['avg_coloane'])

        
            }
            total_chart.series[0].setData(total)
            total_chart.series[1].setData(macau)
            total_chart.series[2].setData(taipa)
            total_chart.series[3].setData(coloane)
            total_chart.series[4].setData(avg_total)
            total_chart.series[5].setData(avg_macau)
            total_chart.series[6].setData(avg_taipa)
            total_chart.series[7].setData(avg_coloane)
        })
    }

function get_new_residence_num_by_month(){
        $.getJSON('/api/get_new_residence_num_by_month', function(json){
            //console.log(json)
            new_chart.xAxis[0].categories = new Array()
            total = new Array();
            macau = new Array();
            taipa = new Array();
            coloane = new Array();
            for(var i = 0; i<json.length;i++){
                //console.log(json[i]['date'])
                new_chart.xAxis[0].categories.push(json[i]['date'])
                total.push(json[i]['new'])
                macau.push(json[i]['new_macau'])
                taipa.push(json[i]['new_taipa'])
                coloane.push(json[i]['new_coloane'])
        
            }
            new_chart.series[0].setData(total)
            new_chart.series[1].setData(macau)
            new_chart.series[2].setData(taipa)
            new_chart.series[3].setData(coloane)
        })
    }

get_total_residence_num_by_month()
get_new_residence_num_by_month()

});
