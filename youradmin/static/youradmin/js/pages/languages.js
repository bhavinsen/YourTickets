var table = $('#language_table').DataTable();
YT.subscribe('language_add_saved', function(args){
    table.ajax.reload(null, false);
});
YT.subscribe('language_edit_saved', function(args){
    table.ajax.reload(null, false);
});
YT.subscribe('language_delete_confirm_success', function(args){
    table.ajax.reload(null, false);
});