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
    ykeys: ['total_new', 'macau_new', 'taipa_new', 'coloane_new'],
    labels: ['total_new', 'macau_new', 'taipa_new', 'coloane_new']
});

    function get_residence_num(){
        $.getJSON('/api/get_residence_num', function(json){
            morrisResidenceNum.setData(json)
        })
    }

    function get_residence_num_new(){
        $.getJSON('/api/get_residence_num_new', function(json){
            console.log(json)
            morrisResidenceNumNew.setData(json)
        })
    }

get_residence_num()
get_residence_num_new()
});