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

YT.subscribe('order_delete_confirm_success', function(args){
    $('#maintable').DataTable().ajax.reload(null, false);
});