function fnFormatDetails ( oTable, nTr )
{
    var aData = oTable.fnGetData( nTr );
    var sOut = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">';
    sOut += '<tr><td>region:</td><td>'+aData[7]+' </td></tr>';
    sOut += '<tr><td>age:</td><td>'+aData[8]+' </td></tr>';
    sOut += '<tr><td>layout:</td><td>'+aData[9]+'</td></tr>';
    console.log(aData[10].length)
    if(aData[10].length){
        console.log(aData[10].length)
        sOut += '<tr><td>photo:</td><td>'
        sOut += '<div class="carousel slide auto panel-body" id="c-slide">\
                            <ol class="carousel-indicators out">\
                                <li data-target="#c-slide" data-slide-to="0" class="active"></li>'
        for(var i = 1; i < aData[10].length; ++i){
            sOut += '<li data-target="#c-slide" data-slide-to="' + i + '"></li>'
        }
        sOut += '</ol>\
                            <div class="carousel-inner">\
                                <div class="item text-center active">\
                                    <img src="' + aData[10][0] + '", width=250, height=250 >\
                                </div>'

        for(var i = 1; i < aData[10].length; ++i){
            sOut += '<div class="item text-center">\
                                    <img src="' + aData[10][i] + '", width=250, height=250 >\
                                </div>'
        } 
        sOut += '</div>\
                            <a class="left carousel-control" href="#c-slide" data-slide="prev">\
                                <i class="fa fa-angle-left"></i>\
                            </a>\
                            <a class="right carousel-control" href="#c-slide" data-slide="next">\
                                <i class="fa fa-angle-right"></i>\
                            </a>\
                        </div>'
        sOut += '</td></tr>'
    }
    sOut += '</table>';

    return sOut;
}

$(document).ready(function() {

    $('#dynamic-table').dataTable( {
        "aaSorting": [[ 4, "desc" ]]
    } );

    /*
     * Insert a 'details' column to the table
     */
    var nCloneTh = document.createElement( 'th' );
    var nCloneTd = document.createElement( 'td' );
    nCloneTd.innerHTML = '<img src="/static/images/details_open.png">';
    nCloneTd.className = "center";
    nCloneTd.width = 20

    $('#hidden-table-info thead tr').each( function () {
        this.insertBefore( nCloneTh, this.childNodes[0] );
    } );

    $('#hidden-table-info tbody tr').each( function () {
        this.insertBefore(  nCloneTd.cloneNode( true ), this.childNodes[0] );
    } );

    /*
     * Initialse DataTables, with no sorting on the 'details' column
     */
    var oTable = $('#hidden-table-info').dataTable( {
        "aoColumnDefs": [
            { "bSortable": false, "aTargets": [ 0 ] }
        ],
        "aaSorting": [[1, 'asc']]
    });
    /* Add event listener for opening and closing details
     * Note that the indicator for showing which row is open is not controlled by DataTables,
     * rather it is done here
     */
    $(document).on('click','#hidden-table-info tbody td img',function () {
        var nTr = $(this).parents('tr')[0];
        if ( oTable.fnIsOpen(nTr) )
        {
            /* This row is already open - close it */
            this.src = "/static/images/details_open.png";
            oTable.fnClose( nTr );
        }
        else
        {
            /* Open this row */
            this.src = "/static/images/details_close.png";
            oTable.fnOpen( nTr, fnFormatDetails(oTable, nTr), 'details' );
        }
    } );
} );