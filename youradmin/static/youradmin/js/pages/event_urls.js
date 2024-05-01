
var table = $('#maintable').DataTable();

YT.subscribe('event_url_add_saved', function(args){
    table.ajax.reload(null, false);
});


YT.subscribe('event_url_edit_saved', function(args){
    table.ajax.reload(null, false);
});

YT.subscribe('event_url_delete_confirm_success', function(args){
    table.ajax.reload(null, false);
});

$(document).on('changed.bs.select', 'select[name="event"]', function (e, clickedIndex, isSelected, previousValue) {
    $('select[name="multiticketshop"]').selectpicker('deselectAll');
});

$(document).on('changed.bs.select', 'select[name="multiticketshop"]', function (e, clickedIndex, isSelected, previousValue) {
    $('select[name="event"]').selectpicker('deselectAll');
});

$('#event_url_add').on('shown.bs.modal', function(){
    $('select[name="event"]').selectpicker('deselectAll');
    $('select[name="multiticketshop"]').selectpicker('deselectAll');
});

$('#event_url_edit').on('shown.bs.modal', function(){
    $('.selectpicker').selectpicker('refresh');
});