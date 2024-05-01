
$(function(){

    $('#direct-marker').click(function(){
        var url = YT.urls.mark_event;

        YT.showLoader($(this).closest('.panel-body'));

        var btn = $(this);

        var new_value = $(this).data('current') == 'False'? true: false

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'mark': new_value
            }
        })
        .done(function (msg) {
            if (msg.success === true) {

                btn.data('current', new_value);
                if(new_value == true){
                    $('.glyphicon[data-marker="true"]').removeClass('hidden');
                    $('.glyphicon[data-marker="false"]').addClass('hidden');
                }else{
                    $('.glyphicon[data-marker="true"]').addClass('hidden');
                    $('.glyphicon[data-marker="false"]').removeClass('hidden');
                }


            } else {

            }
            YT.hideLoader(btn.closest('.panel-body'));

        });
    });

})




YT.subscribe('user_delete_confirm_success', function(args){

});