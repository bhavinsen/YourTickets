var YT = function () {
    //initialize stuff here

    /**
     * global error shown when something went wrong with the ajax call
     */
    $(document).ajaxError(function (event, jqXHR, settings, thrownError) {
        YT.showError(thrownError || 'Error','Something wrong.')
        //console.log(jqXHR.responseText)
        /**
         * hide all loaders
         */

        $('.loader').remove()
    });

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });

    $(function(){
        /**
         * left menu
         */
        //$('.leftmenu').find('.main-item').click(function(){
        //    $(this).closest('.list-group-item').toggleClass('active');
        //});

    });

};





YT.prototype = {
    _events:{},
    publish: function(eventName, args){
        if(this._events.hasOwnProperty(eventName) === false){
            this._events[eventName] = {
                subscribers:[],
                args:args,
                published:true
            }
        }
        var event = this._events[eventName];
        for(var i=0;i<event.subscribers.length;i++){
            subscriber = event.subscribers[i];
            subscriber.fn(args);
            if(subscriber.hasOwnProperty('once')){
                this._events[eventName].subscribers.splice(i,1);
            }
        }
        event.args = args;
    },
    subscribe: function(eventName, fn){
        if(this._events.hasOwnProperty(eventName) === false){
            this._events[eventName] = {
                subscribers:[],
                published:false
            }
        }
        var event = this._events[eventName];
        event.subscribers.push({fn:fn});
        if(event.published == true){
            fn(event.args);
        }
    },
    subscribeOnce: function(eventName, fn){
        if(this._events.hasOwnProperty(eventName) === false){
            this._events[eventName] = {
                subscribers:[],
                published:false
            }
        }
        var event = this._events[eventName];
        var key = event.subscribers.push({fn:fn, once:true});
        if(event.published == true){
            fn(event.args);
            this._events[eventName].subscribers.splice(key,1);
        }
    },
    /**
     * this is for server errors
     * @param title
     * @param message
     * @param container
     */
    showError: function (title, message, container) {

        container = typeof container !== 'undefined' ? container : '#error';
        $(container).find('.error_message').html(message);
        $(container).find('.error_title').html(title);
        $(container).removeClass('hidden');
    },

    /**
     * this is to hide error shown before
     * @param container
     */
    hideError: function (container) {
        container = typeof container !== 'undefined' ? container : '#error';

        $(container).find('.error_message').html('');
        $(container).find('.error_title').html('');
        $(container).addClass('hidden');
    },
    /**
     * this is for error like for not correctly filled in and stuff
     * @param title
     * @param message
     * @param container
     */
    showWarning: function (title, message, container) {
        container = typeof container !== 'undefined' ? container : '#warning';

        // mycontainer = container;
        $(container).find('.warning_message').html(message);
        $(container).find('.warning_title').html(title);
        $(container).removeClass('hidden');
    },
    /**
     * this is to hide warning shown before
     * @param container
     */
    hideWarning: function (container) {
        container = typeof container !== 'undefined' ? container : '#warning';

        // mycontainer = container;
        $(container).find('.warning_message').html('');
        $(container).find('.warning_title').html('');
        $(container).addClass('hidden');
    },
    /**
     * this is when something went ok
     * @param title
     * @param message
     */
    showSuccess: function (title, message, container) {
        container = typeof container !== 'undefined' ? container : '#success';

        $(container).find('.success_message').html(message);
        $(container).find('.success_title').html(title);
        $(container).removeClass('hidden');
    },

    /**
     * this is to hide success shown before
     * @param container
     */
    hideSuccess: function (container) {
        container = typeof container !== 'undefined' ? container : '#success';

        $(container).find('.success_message').html('');
        $(container).find('.success_title').html('');
        $(container).addClass('hidden');
    },
    /**
     * hide all the alerts
     */
    hideAllNotifications: function(){
        $('.usernotifications').find('.alert').addClass('hidden');
    },
    showFormErrors: function(formDomElement, errors){
        for(var field in errors){

            var fieldErrors = errors[field];

            //input field
            var domField = formDomElement.find('[name="'+field+'"]').first();


            //form group field
            var domFormContainer = domField.closest('div.form-group');

            //error message container for displaying error messages
            //example: <ul class="errorlist"><li>This field is required.</li></ul
            var errorMessageContainer = domFormContainer.find('.errormessage_container');

            /**
             * if the error message container doesnt have a list yet create it
             */
            if(errorMessageContainer.find('.errorlist').length === 0){
                errorMessageContainer.html('<ul class="errorlist"></ul>')
            }

            var errorList = errorMessageContainer.find('.errorlist').first();

            /**
             * empty the errorlist
             */
            errorList.html('');

            for(var i=0;i<fieldErrors.length;i++){
                var error = fieldErrors[i]
                var message = error.message;
                errorList.append('<li>'+message+'</li>')
            }

            if(domFormContainer.hasClass('has-error')){
                continue;
            }

            domFormContainer.addClass('has-error has-feedback');
            domField.parent().append('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>');
        }
    },
    showFormGroupErrors: function(formDomElement, errors){
        for(var field in errors){

            var fieldErrors = errors[field];

            //input field
            var domField = formDomElement.find('[name="'+field+'"]').first();

            //form group field
            var domFormContainer = domField.closest('div.form-group');

            // get error container
            var errorMessageContainer = domField.closest('div.input-element').find('.errormessage_container');

            /**
             * if the error message container doesnt have a list yet create it
             */
            if(errorMessageContainer.find('.errorlist').length === 0){
                errorMessageContainer.html('<ul class="errorlist"></ul>')
            }

            var errorList = errorMessageContainer.find('.errorlist').first();

            /**
             * empty the errorlist
             */
            errorList.html('');

            for(var i=0;i<fieldErrors.length;i++){
                var error = fieldErrors[i]
                var message = error.message;
                errorList.append('<li>'+message+'</li>')
            }

            if(domFormContainer.hasClass('has-error')){
                continue;
            }

            domFormContainer.addClass('has-error has-feedback');
            domField.parent().append('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>');

        }
    },
    cleanFormErrors: function(formDomElement){
        formDomElement.find('.errorlist').remove();
        formDomElement.find('div.form-group').removeClass('has-error');
        formDomElement.find('.form-control-feedback').remove();
    },
    showLoader: function(element, css, loader){
        // var image = '/static/youradmin/img/loader.gif';
        // if(loader != undefined){
        //     image = loader
        // }



        $(element).addClass('loader-parent').append('<div class="loader"></div>');
        $(element).find('.loader').show();
    },
    hideLoader: function(element){
        $(element).removeClass('loader-parent').find('.loader').remove();
    },
    serializeObject: function(serializedFormArray){
        var o = {};
        var a = serializedFormArray;
        $.each(a, function() {
           if (o[this.name]) {
               if (!o[this.name].push) {
                   o[this.name] = [o[this.name]];
               }
               o[this.name].push(this.value || '');
           } else {
               o[this.name] = this.value || '';
           }
        });
        return o;
    },
    createCookie: function(name, value, days) {
        var expires;
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toGMTString();
        }
        else {
            expires = "";
        }
        document.cookie = name + "=" + value + expires + "; path=/";
    },
    getCookie: function (c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) {
                    c_end = document.cookie.length;
                }
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return "";
    },
    getUrlParameter: function(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }
};

YT = new YT();

function truefalse_field_renderer(data, type, row, meta){
    var color = data==true ? 'green' : '#e6e6e6';
    var html = '<span style="color:'+color+'" class="glyphicon glyphicon-ok"></span>';
    return html;
}