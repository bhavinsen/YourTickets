$(function(){

    $('.navbar-toggle').click(function(){
        $(this).toggleClass('change');
    });

    $('.navbar-collapse a').click(function(){
        $(".navbar-collapse").collapse('hide');
        $('.navbar-toggle').addClass('collapsed');
        $('.navbar-toggle').toggleClass('change');
    });

    $('body').scrollspy({ target: '.navbar-collapse', offset:100 });

    $('.process .cardlink').click(function(){
        $el = $(this);
        $('.process .cardlink').removeClass('active');
        $el.toggleClass('active');

        $('.process.subframe').hide();
        $($el.data('frame')).show();
    });

    $('.whyyourtickets .navlink').click(function(){
        $el = $(this);
        $('.navlink').removeClass('active');
        $el.toggleClass('active');

        $('.whyyourtickets .subframe .row').hide();
        $('.whyyourtickets '+$el.data('frame')).show();
        checkArrows($el.data('frame'));
    });

    var currentNavItem = '#why-1';

    $('.whyyourtickets .arrows img').click(function(){

        $el = $(this);

        if(!$el.hasClass('enabled')){
            return;
        }

        $curActive = $($('.whyyourtickets .navlink.active').first().parent('div'));

        if($el.hasClass('left')){
            $curActive.prev('div').find('.navlink').first().click();
        }else if($el.hasClass('right')){
            $curActive.next('div').find('.navlink').first().click();
        }

    });

    function checkArrows(newSelectedId){

        currentNavItem = newSelectedId;

        var $left = $('.whyyourtickets .left');
        var $right = $('.whyyourtickets .right');

        $left.removeClass('enabled');
        $right.removeClass('enabled');

        if(currentNavItem == '#why-1'){
            $right.addClass('enabled');
        }else if(currentNavItem == '#why-2' || currentNavItem == '#why-3'){
            $left.addClass('enabled');
            $right.addClass('enabled');
        }else if(currentNavItem == '#why-4'){
            $left.addClass('enabled');
        }

    }

    $('.special-input').click(function(){
        $('.input_ticket_price').show();
        $('.input_ticket_price').focus();
    });
    $('.input_ticket_price').focusout(function(){
        if($(this).val() == ""){
            $('.input_ticket_price').hide();
        }
    }).keyup(function(){
        //(1.45*tickets_amount) + (order_price*0.025)
        if($(this).val() === "" || !$(this).val() || $(this).val() === '0'){
            $('.ticketprice-calculated').html('0.00');
            return;
        }

        var value = (1.45*1)+(parseFloat($(this).val())*0.025);

        $('.ticketprice-calculated').html(value.toFixed(2));
    });


});