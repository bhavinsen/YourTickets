

$(function(){

    $('#create_ticketshop').click(function(){
        var modal = $('[data-remodal-id=create-multi_ticketshop]').remodal();
        modal.open();

    });

    var remove_multishop_url = '';
    $('.remove-multishop').click(function(){
        var inst = $('[data-remodal-id=remove-shop]').remodal();
        remove_multishop_url = $(this).data('href');
        inst.open();
    });

    $('[data-remodal-id=remove-shop]').find('#delete-confirm').click(function(){
        document.location = remove_multishop_url;
    });

    var request_url = '';
    var td = '';
    $('.request_short_url').click(function(){


        var inst = $('[data-remodal-id=request-short-url]').remodal();

        inst.open();
        td = $(this).closest('td');
        request_url = $(this).data('url');
    });

    $('[data-remodal-id=request-short-url]').find('#request-confirm').click(function(){

        var $modal = $(this).closest('.remodal');
        var url_name = $('[name="urlname"]').val();

        if(url_name == ''){
            return;
        }

        $.ajax({
        url: request_url,
        method: "post",
        data: {
            'csrfmiddlewaretoken': $modal.find('input[name="csrfmiddlewaretoken"]').val(),
            'url_name': url_name
        },
        success: function (data) {
            if(data.success === true){


                // document.location = data.url;
                td.find('.message_send').removeClass('hidden');
                td.find('.request_short_url').hide();

                var modal = $('[data-remodal-id=request-short-url]').remodal();
                modal.close();

            }
        }});

    });


    $('#create-shop-button').click(function(){

       if($(this).closest('.remodal').find('input[name="name"]').val() == ''){
           return;
       }

       $.ajax({
        url: $(this).data('url'),
        method: "post",
        data: {
            'csrfmiddlewaretoken': $(this).closest('.remodal').find('input[name="csrfmiddlewaretoken"]').val(),
            'name':$(this).closest('.remodal').find('input[name="name"]').val()
        },
        success: function (data) {
            if(data.success === true){
                var modal = $('[data-remodal-id=create-multi_ticketshop]').remodal();
                modal.close();

                document.location = data.url;


            }
        }});

   });

});