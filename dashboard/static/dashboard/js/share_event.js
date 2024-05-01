
$(function(){

    var remove_channel_url = '';
    $('.remove-channel').click(function(){
        var inst = $('[data-remodal-id=remove-channel]').remodal();
        remove_channel_url = $(this).data('href');
        inst.open();
    });
    $('[data-remodal-id=remove-channel]').find('#delete-confirm').click(function(){
        document.location = remove_channel_url;
    });

    $('.create-channel').click(function(){
        var inst = $('[data-remodal-id=create-channel]').remodal();
        remove_channel_url = $(this).data('href');
        inst.open();
    });

    $('#create-confirm').click(function(){

        var $modal = $(this).closest('.remodal');
        var value = $modal.find('[name="user_email"]').val();
        $.ajax({
        url: $modal.data('url'),
        method: "post",
        data: {
            'csrfmiddlewaretoken': $modal.find('input[name="csrfmiddlewaretoken"]').val(),
            'user_email': value
        },
        success: function (data) {
            if(data.success === true){
                document.location.reload();
            }
        }});
    });

});