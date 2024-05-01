function loadPanel(type, callback){

    var panel = $('#'+type);
    var panel_body = panel.find('.panel-body');

    YT.showLoader(panel_body);

    $.ajax({
        url: YT.urls['dashboard_'+type],
        type: 'GET'
    })
    .done(function (msg) {
        if (msg.success === true) {
            callback(msg)
        } else {
            YT.showError('Error',msg.error,panel.find('.alert-danger'))
        }
        YT.hideLoader(panel_body);
    });
}