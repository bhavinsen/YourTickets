(function () {
    "use strict";
    //add a readmore button when description is biger than 100
    $(".readmore").click(function () {
        $('.js-readmore').toggleClass('active');
        $('#description').toggleClass('active');
    });
    if ($('#description').height() > 100) {
        $('.js-readmore').toggleClass('active');
    }
    //counter for adding or removing an ticket in the shop
    $(document).on('click','.js-addNumber', function() {
        var $button = $(this),
            _input = $button.parent().find("input.u-addNumber-input"),
            maxValues = $( _input).map(function(){
                return this.max;
            }).get(),
            oldValue = $( _input).val(),
            newVal;

        if ($button.text() === "-" && oldValue != 0) {
             newVal = parseFloat(oldValue) - 1;
             removeshoptooltip();
        }
        else if ($button.text() === "+" && oldValue != maxValues) {
            newVal = parseFloat(oldValue) + 1;
            removeshoptooltip();
        }
        else if (oldValue >= maxValues){
            $(this).toggleClass('shop-tooltip');
            $(this).prop('title', 'Je kunt niet meer dan '+ maxValues +' tickets bestellen');
             newVal = maxValues;
        }
        else{
            newVal = 0;
        }
        $(_input).val(newVal);
    });
    $( "input[name='quantity[]']" ).focusout(function() {
        var maxValues = +$(this).map(function(){
                return this.max;
            }).get(),
            Value = $(this).val();
        if($.isNumeric($(this).val())){
            if (Value < 0) {
                $(this).val(0);
            }
        }
        else{
            $(this).val(0);
        }
        if (Value > maxValues) {
            $(this).val(maxValues);
        }
    });
    $(document).click(function() {
       if (!$(event.target).closest('.js-addNumber').length) {
            removeshoptooltip();
        }
    });
    function removeshoptooltip(){
        $('.js-addNumber').removeClass('shop-tooltip');
    }

    $(".js-popup-click").click(function () {

       var template = typeof $(this).data('template') == 'undefined' ? '' : $(this).data('template');
       showPopup($(this).data('lang'), template);
       $(".js-overlay").data('lang', $(this).data('lang'));
       $(".js-overlay").data('template', template);
    });
    $(".js-overlay").click(function () {
       hidePopup($(this).data('lang'), $(this).data('template'));
    });
    $(".js-autoselect").click(function () {
       $(this).select();
    });
    $(document).on('click','.js-login-add', function() {
        showLogin()
    });
    $(document).on('click','.js-register-add', function() {
        showRegister()
    });
    $(document).on('click','#js-login .popup-overlay', function() {
        hideLogin()
    });
    $(document).on('click','#js-register .popup-overlay', function() {
        hideRegister()
    });
    function showPopup(lang, template){
        if(template !== ''){
            $(template).addClass('active');
        }else{
            $(".js-popup[data-lang='"+lang+"']").addClass('active');
        }

      $(".js-popup-overlay").addClass('active');
      $("body").addClass('u-noscroll');
      $('.nav > .nav-leftwrapper').addClass('be-static');
    }
    function hidePopup(lang, template){
        if(template !== ''){
            $(template).removeClass('active');
        }else{
            $(".js-popup[data-lang='"+lang+"']").removeClass('active');
        }

      $(".js-popup-overlay").removeClass('active');
      $("body").removeClass('u-noscroll');
      $('.nav > .nav-leftwrapper').removeClass('be-static');
    }

    function showLogin(){
        hideRegister()
          if(document.getElementById("js-login") == null) {
            $.ajax({
                url: "popup_login.html",
                success: function (data) { $('body').append(data)},
                dataType: 'html'
            });
          } else {
            $('#js-login').show();
          }
      $("body").addClass('u-noscroll');
    }
    function hideLogin(){
      $('#js-login').hide();
      $("body").removeClass('u-noscroll');
    }
    function showRegister(){
         hideLogin()
          if(document.getElementById("js-register") == null) {
            $.ajax({
                url: "popup_aanmelden.html",
                success: function (data) { $('body').append(data)},
                dataType: 'html'
            });
          } else {
            $('#js-register').show();
          }
      $("body").addClass('u-noscroll');
    }
    function hideRegister(){
      $('#js-register').hide();
      $("body").removeClass('u-noscroll');
    }

}());
(function($) {
    $.fn.Color = function( options ) {
         var settings = $.extend({
            primary_color           : '#dc3547',
            secondary_color         : '#55c7e0'
        }, options);
        return this.each( function() {
            if ( settings.primary_color ) {
                $(".primary_color").css( 'color', settings.primary_color);
                $(".bg-primary_color").css( 'background', settings.primary_color);
            }
            if ( settings.secondary_color  ) {
                $(".secondary_color").css( 'color', settings. secondary_color);
                $(".bg-secondary_color").css( 'background', settings. secondary_color);
            }
        });
    };
}(jQuery));

