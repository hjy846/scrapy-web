if (top.location != location) {
    top.location.href = document.location.href ;
}


$(function(){
    //console.log('begin')
    //jQuery('.petrol').text(1276.3)
    //updateStatus() 

var morrisResidenceNum = Morris.Line({
    element: 'graph-area-line',
    behaveLikeLine: false,
    data: [
        
    ],
    xkey: 'date',
    ykeys: ['total', 'macau', 'taipa', 'coloane'],
    labels: ['total', 'macau', 'taipa', 'coloane']
});

var morrisResidenceNumNew = Morris.Line({
    element: 'graph-area-line-new',
    behaveLikeLine: false,
    data: [
        
    ],
    xkey: 'date',
    ykeys: ['total', 'macau', 'taipa', 'coloane'],
    labels: ['total', 'macau', 'taipa', 'coloane']
});

    function get_dsf_volumn(){
        $.getJSON('/api/dsf_total_volumn_price_query?query=volumn', function(json){
            console.log(json)
            morrisResidenceNum.setData(json)
        })
    }

    function get_dsf_price(){
        $.getJSON('/api/dsf_total_volumn_price_query?query=avage_price', function(json){
            //console.log(json)
            console.log(json)
            morrisResidenceNumNew.setData(json)
        })
    }

get_dsf_volumn()
get_dsf_price()
});