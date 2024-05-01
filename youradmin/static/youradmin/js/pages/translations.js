$(function(){

    $('#changemode').click(function(){

        if($('#rightcolumn').hasClass('hidden')){
            $('#leftcolumn').removeClass('col-md-11').addClass('col-md-5');
            $('#rightcolumn').removeClass('hidden');
        }else{
            $('#leftcolumn').addClass('col-md-11').removeClass('col-md-5');
            $('#rightcolumn').addClass('hidden');
        }


    });


});

var tableLeft = $('#table_left').DataTable();

$('.page-translations #leftcolumn select[name="language_id"]').on('change',function(){
    //tablee.columns(4).search(this.value).draw();
    var url = YT.urls.translations_refresh.replace('_placeholder',$(this).val());
    tableLeft.ajax.url(url).load();

    url = $('#button_left_add').data('ajax_submit_url_placeholder');
    $('#button_left_add').data('ajax_submit_url', url.replace('_placeholder', $(this).val()));

});

$('.page-translations #leftcolumn input[name="key"]').on('keyup change',function(){
    tableLeft.columns(0).search(this.value).draw();
});

$('.page-translations #leftcolumn input[name="value"]').on('keyup change',function(){
    tableLeft.columns(1).search(this.value).draw();
});

var tableRight = $('#table_right').DataTable();

$('.page-translations #rightcolumn select[name="language_id"]').on('change',function(){
    //tablee.columns(4).search(this.value).draw();
    var url = YT.urls.translations_refresh.replace('_placeholder',$(this).val());
    tableRight.ajax.url(url).load();

    url = $('#button_right_add').data('ajax_submit_url_placeholder');
    $('#button_right_add').data('ajax_submit_url', url.replace('_placeholder', $(this).val()));
});

$('.page-translations #rightcolumn input[name="key"]').on('keyup change',function(){
    tableRight.columns(0).search(this.value).draw();
});

$('.page-translations #rightcolumn input[name="value"]').on('keyup change',function(){
    tableRight.columns(1).search(this.value).draw();
});


//saver listeners
YT.subscribe('translation_left_add_saved', function(args){
    tableLeft.ajax.reload(null, false);
});

YT.subscribe('translation_right_add_saved', function(args){
    tableRight.ajax.reload(null, false);
});

YT.subscribe('translation_edit_saved', function(args){
    tableRight.ajax.reload(null, false);
    tableLeft.ajax.reload(null, false);
});

YT.subscribe('translation_delete_confirm_success', function(args){
    tableRight.ajax.reload(null, false);
    tableLeft.ajax.reload(null, false);
});
YT.subscribe('translations_add_saved', function(args){
    tableRight.ajax.reload(null, false);
    tableLeft.ajax.reload(null, false);
});

