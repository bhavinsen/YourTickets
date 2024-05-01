(function ( $ ) {
    $.fn.filterList = function( options ) {
        // This is the easiest way to have default options.
        var opts = $.extend( {}, $.fn.filterList.defaults, options );
        // Greenify the collection based on the settings variable.
        return this.each(function() {
            var elem = $( this );
            var listElements = elem.find('li');
            listElements.each(function(key, listElement){
                var $listElement = $(listElement);
                var matchFound = false;
                for(var searchKey in opts) {
                    var searchString = opts[searchKey];
                    var filterElements = $listElement.find('[data-name="' + searchKey + '"]');
                    /**
                     * loop over the elements with the found data attribute value
                     */
                    for (var i = 0; i < filterElements.length; i++) {
                        var txt = $(filterElements[i]);
                        var b = (new RegExp(searchString, "i")).test(txt.text());
                        //var a = txt.text().toLowerCase().indexOf(searchString);
                        if (b === true) {
                            matchFound = true;
                            break;
                        }
                    }
                }
                if (matchFound === false) {
                    $listElement.hide();
                } else {
                    $listElement.show();
                }
            });
        });
    };
    $.fn.filterList.defaults = {
    };
}( jQuery ));