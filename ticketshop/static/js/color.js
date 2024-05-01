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

