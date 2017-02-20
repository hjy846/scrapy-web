if (top.location != location) {
    top.location.href = document.location.href ;
}


$(function(){
    //console.log('begin')
    //jQuery('.petrol').text(1276.3)
    //updateStatus() 

total_chart = new Highcharts.chart('container_total', {
    chart: {
        type: 'line',
        zoomType: 'x'
    },
    title: {
        text: '每日放盘'
    },
    subtitle: {
        text: ''
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

new_chart = new Highcharts.chart('container_new', {
    chart: {
        type: 'line',
        zoomType: 'x'
    },
    title: {
        text: '每日新放盘'
    },
    subtitle: {
        text: ''
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

    function get_residence_num(){
        $.getJSON('/api/get_residence_num', function(json){
            total_chart.xAxis[0].categories = new Array()
            total = new Array();
            macau = new Array();
            taipa = new Array();
            coloane = new Array();
            for(var i = 0; i<json.length;i++){
                //console.log(json[i]['date'])
                
                total_chart.xAxis[0].categories.push(json[i]['date'])
                total.push(json[i]['total'])
                macau.push(json[i]['macau'])
                taipa.push(json[i]['taipa'])
                coloane.push(json[i]['coloane'])
        
            }
            total_chart.series[0].setData(total)
            total_chart.series[1].setData(macau)
            total_chart.series[2].setData(taipa)
            total_chart.series[3].setData(coloane)
        })
    }

    function get_residence_num_new(){
        $.getJSON('/api/get_residence_num_new', function(json){
            //console.log(json)
            new_chart.xAxis[0].categories = new Array()
            total = new Array();
            macau = new Array();
            taipa = new Array();
            coloane = new Array();
            for(var i = 0; i<json.length;i++){
                //console.log(json[i]['date'])
                new_chart.xAxis[0].categories.push(json[i]['date'])
                total.push(json[i]['total_new'])
                macau.push(json[i]['macau_new'])
                taipa.push(json[i]['taipa_new'])
                coloane.push(json[i]['coloane_new'])
        
            }
            new_chart.series[0].setData(total)
            new_chart.series[1].setData(macau)
            new_chart.series[2].setData(taipa)
            new_chart.series[3].setData(coloane)
        })
    }

get_residence_num()
get_residence_num_new()
});