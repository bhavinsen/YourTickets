$(function(){

    $("#birth_date").inputmask('dd-mm-yyyy', {placeholder: 'dd-mm-jjjj', clearMaskOnLostFocus:true});

    $('.ticket-panel-button').click(function(){

        $(this).closest('.ticket-panel').find('.ticket-panel-body').toggleClass('hidden');
    });

    $('#hide_alternative').click(function(){
        $('.ticket-panel-group').addClass('hidden');
    });

    $('#show_alternative').click(function(){
        $('.ticket-panel-group').removeClass('hidden');
    });

    if($('#show_alternative').is(':checked')){
        console.log('ok')
        $('.ticket-panel-group').removeClass('hidden');
    }

});