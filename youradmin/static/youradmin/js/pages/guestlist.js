YT.subscribe('send_mail_confirm_success', function(args){
    $('#maintable').DataTable().ajax.reload(null, false);
});

var service_running = false;

$('#maintable').DataTable().on('draw', function(){
    if(service_running === true){
        call()
    }
});


function start_service(){
        service_running = true;
        $('#info_total_send').html('0');
        $('#info_total_errors').html('0')


        call();
    }

function stop_service(){
    service_running = false;
}

var error_skip_index = 0;

function call() {

    var pk = $('#maintable').DataTable().data()[error_skip_index].pk;

    var url = YT.urls.guestlist_send.replace('_placeholder_id', pk);

    var $cell = $('#maintable').find('#'+pk).find('td').last();

    YT.showLoader($cell, 'width:20px;height:20px;');

    $.ajax({
        url: url,
        type: 'GET'
    }).done(function (data) {

        YT.hideLoader($cell);

        if (data.success === true) {
            $('#info_total_send').html(parseInt($('#info_total_send').html())+1);

            $('#maintable').DataTable().ajax.reload(null, false);

        }else{
            error_skip_index += 1;
            $('#info_total_errors').html(error_skip_index);
            $cell.html('error sending');
        }

    });

}

$(function(){





//    onclick button

    $('#stop_sending').click(function(){

        stop_service();


    });

//    get first record from
    $('#start_sending').click(function(){

        start_service();


    });

});