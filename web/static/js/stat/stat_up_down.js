if (top.location != location) {
    top.location.href = document.location.href ;
}


$(function(){
    //console.log('begin')
    //jQuery('.petrol').text(1276.3)
    //updateStatus() 

var chart = Highcharts.chart('container', {

    chart: {
        type: 'column',
        zoomType: 'x'
    },

    title: {
        text: '涨跌价数量'
    },

    xAxis: {
        labels:{
            rotation:-45
        },
        categories: ['Apples', 'Oranges', 'Pears', 'Grapes', 'Bananas']
    },

    yAxis: {
        allowDecimals: false,
        min: 0,
        title: {
            text: ''
        }
    },

    tooltip: {
        formatter: function () {
            return '<b>' + this.x + '</b><br/>' +
                this.series.name + ': ' + this.y + '<br/>' +
                'Total: ' + this.point.stackTotal;
        }
    },

    plotOptions: {
        column: {
            stacking: 'normal'
        }
    },

    series: [{
        name: '路環(涨)',
        data: [],
        stack: 'up'
    }, {
        name: '氹仔(涨)',
        data: [],
        stack: 'up'
    }, {
        name: '澳門(涨)',
        data: [],
        stack: 'up'
    }, {
        name: '路環(跌)',
        data: [],
        stack: 'down'
    }, {
        name: '氹仔(跌)',
        data: [],
        stack: 'down'
    }, {
        name: '澳門(跌)',
        data: [],
        stack: 'down'
    }]
});

function get_up_down_num_by_month(){
        $.getJSON('/api/get_up_down_num_by_month', function(json){
            //console.log(json)
            chart.xAxis[0].categories = new Array()
            
            up_macau = new Array();
            up_taipa = new Array();
            up_coloane = new Array();
            down_macau = new Array();
            down_taipa = new Array();
            down_coloane = new Array();
            for(var i = 0; i<json.length;i++){
                //console.log(json[i]['date'])
                chart.xAxis[0].categories.push(json[i]['date'])
                up_macau.push(json[i]['up_macau'])
                up_taipa.push(json[i]['up_taipa'])
                up_coloane.push(json[i]['up_coloane'])
                down_macau.push(json[i]['down_macau'])
                down_taipa.push(json[i]['down_taipa'])
                down_coloane.push(json[i]['down_coloane'])
        
            }
            chart.series[0].setData(up_coloane)
            chart.series[1].setData(up_taipa)
            chart.series[2].setData(up_macau)
            chart.series[3].setData(down_coloane)
            chart.series[4].setData(down_taipa)
            chart.series[5].setData(down_macau)
        })
    }   
get_up_down_num_by_month()
});