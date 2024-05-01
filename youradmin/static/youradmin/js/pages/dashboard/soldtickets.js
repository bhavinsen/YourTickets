loadPanel('panel_soldtickets', function (msg) {
    $('#dashboard_soldtickets_total').html(msg.total);
});