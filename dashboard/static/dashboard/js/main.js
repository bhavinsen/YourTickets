var link;

$(document).on('click','#ticket-delete-confirm', function(){
  document.location = link

});

$(function(){
    // this is actually not remove event, but remove ticket
    $('.remove-event').click(function(){
        var inst = $('[data-remodal-id=remove-event]').remodal();
        link = $(this).data('href');
        inst.open();
    });


    $('#amount_switcher').toggles({
        text: {
            on: '%',
            off: '#'
        },
        on: true,
        type:'select'
    });

    $('#amount_switcher').on('toggle', function(e, active) {

        $('.tickets_sold_percentage').toggleClass('hidden');
        $('.tickets_sold_amount').toggleClass('hidden');

    });


    $('#remove_event').click(function(){
        var inst = $('[data-remodal-id=remove_event]').remodal();
        inst.open();
    });
    $('[data-remodal-id=remove_event]').find('#event-delete-confirm').click(function(){
        var $el = $(this);
        $.ajax({
                url: $el.data('url'),
                success: function (data) {
                    if(data.success === true){
                        document.location = $el.data('redirect');
                        var inst = $('[data-remodal-id=remove_event]').remodal();
                        inst.close();

                    }
                }});

    });


});
