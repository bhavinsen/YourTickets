var copyToClipboard = function(el) {
        var $this = $(el),
            aux   = document.createElement("input"),
            data  = $this.data('content');
        aux.setAttribute("value", data);
        document.body.appendChild(aux);
        aux.select();
        document.execCommand("copy");
        document.body.removeChild(aux);
    };

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

    $('.copyurl').click(function(){
        copyToClipboard(this);
    })

    $('#create-confirm').click(function(){

        var $modal = $(this).closest('.remodal');
        var value = $modal.find('[name="name"]').val();

        $.ajax({
        url: $modal.data('url'),
        method: "post",
        data: {
            'csrfmiddlewaretoken': $modal.find('input[name="csrfmiddlewaretoken"]').val(),
            'name': value
        },
        success: function (data) {
            if(data.success === true){
                document.location.reload();

                // document.location = data.url;
                // td.find('.message_send').removeClass('hidden');
                // td.find('.request_short_url').hide();
                //
                // var modal = $('[data-remodal-id=request-short-url]').remodal();
                // modal.close();

            }
        }});
    });

});