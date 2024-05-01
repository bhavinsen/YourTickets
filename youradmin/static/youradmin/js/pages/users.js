function truefalse_field_renderer(data, type, row, meta){
    var color = data==true ? 'green' : '#e6e6e6';
    var html = '<span style="color:'+color+'" class="glyphicon glyphicon-ok"></span>';
    return html;
}

function view_info(config){
    var url = slot.urls.gameconfig_config_info.replace('_placeholder', config.id);
    return '<span class="button-icon glyphicon glyphicon-info-sign" data-url=' +
        url + ' data-toggle="modal" data-target="#configinfo"></span>';
}

var tablee = $('#maintable').DataTable();

//$('#search-button').click(function(){
//
//
//    tablee.on('preXhr.dt', function ( e, settings, data ) {
//
//        data.searching = true;
//
//        data.search_id = $('#user_id').val();
//        data.search_firstname = $('#firstname').val();
//        data.search_lastname = $('#lastname').val();
//        data.search_username = $('#username').val();
//        data.search_email = $('#email').val();
//        //data.test = ["a","b"]
//        //data.search_id = $('#user_id').val();
//    });
//
//    tablee.draw();
//});

$('#user_id').on('keyup change',function(){
    tablee.columns(0).search(this.value).draw();
});
$('#firstname').on('keyup change',function(){
    tablee.columns(1).search(this.value).draw();
});
$('#lastname').on('keyup change',function(){
    tablee.columns(2).search(this.value).draw();
});
$('#username').on('keyup change',function(){
    tablee.columns(3).search(this.value).draw();
});
$('#email').on('keyup change',function(){
    tablee.columns(4).search(this.value).draw();
});



YT.subscribe('user_delete_confirm_success', function(args){
    $('#maintable').DataTable().ajax.reload(null, false);
});

//view_tickets = function(order){
//
//    var url = YT.urls.youradmin_orders_get_tickets.replace('_placeholder', order.pk);
//    return '<span class="button-icon glyphicon glyphicon-info-sign" data-url=' +
//        url + ' data-toggle="modal" data-target="#tickets_for_order"></span>';
//};
//$('#tickets_for_order').on('show.bs.modal', function (e) {
//    console.log("yeps")
//});
