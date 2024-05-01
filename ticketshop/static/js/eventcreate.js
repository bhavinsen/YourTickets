var historyVar = [];
var token = "EAACEdEose0cBALGbBJZCEY0HM8fq7EbecIM0ocvuoQLbUSvBJUNJdEg9arvVZB5ZBD6CtRONkwlk1eOxeZB9eUn6g0flCoFt9DCj9F4ZAs9CaIu0UGOkyctVx3MLN2Dlea57viZCekNRwTXaslaXDaLC8ZBgARelwjRIfq49BIAewZDZD";
var d = new Date();
var month = d.getMonth()+1;
var day = d.getDate();
var date = d.getFullYear() + '-' +
    ((''+month).length<2 ? '0' : '') + month + '-' +
    ((''+day).length<2 ? '0' : '') + day;

$(function(){

    $('#start-date').datepicker({
        format: 'yyyy-mm-dd'
    });
    $('#end-date').datepicker({
        format: 'yyyy-mm-dd'
    });

});

$.ajaxSetup({
  cache: true
});
$.getScript('//connect.facebook.net/en_US/sdk.js', function() {
  FB.init({
    appId: '200973763316497',
    version: 'v2.5'
  });
});
var typed = 1;
$(document).on('focusout','#Title', function() {
  if (typed == 1){
  var newString = $('#Title').val().replace(/[ ]+/ig, "_").replace(/[/]+/ig, "");
    $('#eventurl').val(newString);
  }
});
$(document).on('focusout','#eventurl', function() {
  typed = 0;
  var newString = $('#eventurl').val().replace(/[ ]+/ig, "_").replace(/[/]+/ig, "");
    $('#eventurl').val(newString);
});
$('#eventurl').each(function() {
  var elem = $(this);
  elem.data('oldVal', elem.val());
  elem.bind("propertychange change click keyup input paste", function(event) {
    if (elem.data('oldVal') != elem.val()) {
      elem.data('oldVal', elem.val());
      var eventulr_ = '/' + $(this).val();
      FB.api(
        eventulr_,
        'GET', {},
        function(response) {
          if (response["error"] != null) {
            console.log(response["error"]["message"]);
          }
          var eventName = response["name"];
          if (response["description"] != null) {
            showEvent();
          } else if (response) {
            $("#js-event").html("<img class='logo' src='" + loading_gif + "'>");
            $("#js-skipbutton").text("overslaan");

            function backup() {
              addEvent();
            }
            setTimeout(backup, 1000)

          } else {
            $("#js-event").html("<img class='logo' src='" + loading_gif + "'>");
            $("#js-skipbutton").text("overslaan");
          }

          function addEvent() {
            if (response["description"] != null) {
              showEvent();
            } else if (response["name"] != null) {
              $("#js-event").html("<p>Geen beschrijving gevonden bij dit evenement</p>");
            } else {
              $("#js-event").html("<p>Dit is geen geldig openbaar evenement</p>");
            }
          };

          function showEvent() {
            $("#js-event").html("Gevonden evenement: " + eventName);
            $("#js-skipbutton").text("verder");
          };
        }, {
          access_token: token
        });
    }
  });
});
$(document).bind("ajaxSend", function() {
  $(".popup-loading").show();
}).bind("ajaxComplete", function() {
  $(".popup-loading").hide();
});
$('#js-loadingbutton').click(function() {
  $(".popup-loading").show();
});

function getEventData() {
    eventurl = historyVar['eventId'];
    $.ajaxSetup({
        cache: true
    });
    $.getScript('//connect.facebook.net/en_US/sdk.js', function() {
          FB.init({
            appId: '200973763316497',
            version: 'v2.5'
          });
          FB.api(
          eventurl,
          'GET',
          {},
          function(response) {

              $('#Title').val(response["name"]);
              $('#Locatie').val(response["place"]["name"]);
              $('#description').val(response["description"]);

          },{
                  access_token: token
        });
    });
}

var start_date;
var start_time;
var end_date;
var end_time;

$(document).on('click','#js-next-2', function() {
    var flag = 1;
    $(".js-required").each(function(i){
        if ($(this).val() == ""){
            $(this).addClass("form-error");
            if (flag == 1) {
                $('html, body').animate({
                    scrollTop: $(this).offset().top -100
                }, 200);
            }
            flag++;
        }
    });

    var startDate = new Date($('#start-date').val() + ' '+$('#start-time').val());
    var endDate = new Date($('#end-date').val() + ' '+$('#end-time').val());

    $('#startdate_errors').addClass('hidden');
    $('#error-startdate_after_enddate').addClass('hidden');


    if(startDate > endDate){
        $('#start-date').addClass('form-error');
        $('#start-time').addClass('form-error');
        $('#end-date').addClass('form-error');
        $('#end-time').addClass('form-error');

        $('#startdate_errors').removeClass('hidden');
        $('#error-startdate_after_enddate').removeClass('hidden');
        flag++;
    }

    if (flag == 1){
        $(document).scrollTop(0);

        start_date = $('#start-date').val();
        start_time = $('#start-time').val();
        end_date = $('#end-date').val();
        end_time = $('#end-time').val();

        /**
         * load the next page
         */
        $('article').load(createthree_url, function(){
            $('.ticket_start_date').val(date);
            //$('.ticket_start_time').val(start_time);
            /**
             * set the end date at the start date of the event
             */
            $('.ticket_end_date').val(start_date);
            $('.ticket_end_time').val(start_time);
             $('#ticketStartDatum_0').datepicker({
                format: 'yyyy-mm-dd'
            });
            $('#ticketEindDatum_0').datepicker({
                format: 'yyyy-mm-dd'
            });
        });
    }
    historyVar['title'] = $('#Title').val();
    historyVar['locatie'] = $('#Locatie').val();
    historyVar['description'] = $('textarea#description').val();
    historyVar['eventurl'] = $('#eventurl').val();
    historyVar['start-date'] = $('#start-date').val();
    historyVar['start-time'] = $('#start-time').val();
    historyVar['end-date'] = $('#end-date').val();
    historyVar['end-time'] = $('#end-time').val();
    var artiesten = [];
    $('.js-artist').each(function(){
        var artiest = [];
        artiest.push($("input[name='artiest_naam\\[\\]']").map(function(){return $(this).val();}).get());
        artiest.push($("input[name='artiest_url\\[\\]']").map(function(){return $(this).val();}).get());
        artiesten.push(artiest);
    });
    historyVar['artiesten'] = artiesten;
});

var iArtist = 1;
var eArtist = 1;
$(document).on('click','#js-addArtist', function() {
    var artist = $('#js-artist');
    var liData = '<div class="artist js-artist u-desktop-placeholder u-flex-row p-top-12 u-border-top"><input class="small m-right-24 form-input w-100 u-flex u-break" type="text" id="artiestNaam_' + i +'" name="artiest_naam[]" placeholder="Artiest naam"><span class="artist-line js-removeArtist cell-w40 large u-pointer secondary_color-fixed"><i class="fa fa-trash-o" aria-hidden="true"></i></span></div>';
    $(liData).appendTo(artist);
    iArtist++;
    eArtist++;
});


$(document).on('click','.js-removeArtist', function() {
    if(eArtist > 1){
        $(this).parents('.js-artist').slideUp("normal", function() { $(this).remove(); } );
        eArtist--;
    }
});

$(document).on('click','#js-next-3', function() {
    var flag = 1;
    $(".js-required").each(function(i){
        if ($(this).val() == ""){
            $(this).addClass("form-error");
            if (flag == 1) {
                $('html, body').animate({
                    scrollTop: $(this).offset().top -100
                }, 200);
            }
            flag++;
        }
    });


    /**
     * date checks
     */
    $('.js-ticket').each(function(){

        var startDateEl = $(this).find('input[name="ticket_begin_datum[]"]');
        var startTimeEl = $(this).find('input[name="ticket_begin_tijd[]"]');
        var endDateEl = $(this).find('input[name="ticket_eind_datum[]"]');
        var endTimeEl = $(this).find('input[name="ticket_eind_tijd[]"]');

        var startDate = new Date(startDateEl.val() + ' ' + startTimeEl.val());

        var endDate = new Date(endDateEl.val() + ' ' + endTimeEl.val());

        var error_container = $(this).find('.ticket-panel-error-container');
        var error_message = $(this).find('.startdate-error');

        error_container.addClass('hidden');
        error_message.addClass('hidden');
        startDateEl.removeClass('form-error');
        startTimeEl.removeClass('form-error');
        endDateEl.removeClass('form-error');
        endTimeEl.removeClass('form-error');

        if(startDate > endDate){
            error_container.removeClass('hidden');
            error_message.removeClass('hidden');
            startDateEl.addClass('form-error');
            endDateEl.addClass('form-error');
            startTimeEl.addClass('form-error');
            endTimeEl.addClass('form-error');
           flag ++;
        }


    });


    if (flag == 1){
        $('article').load(createfour_url);
        $(document).scrollTop(0);
    }
    var tickets = [];
    $('.js-ticket').each(function(){
        var ticket = [];
        ticket.push($("input[name='ticket_naam\\[\\]']").map(function(){return $(this).val();}).get());
        ticket.push($("input[name='ticket_aantal\\[\\]']").map(function(){return $(this).val();}).get());
        ticket.push($("input[name='ticket_prijs\\[\\]']").map(function(){return $(this).val();}).get());
        ticket.push($("input[name='ticket_begin_datum\\[\\]']").map(function(){return $(this).val();}).get());
        ticket.push($("input[name='ticket_begin_tijd\\[\\]']").map(function(){return $(this).val();}).get());
        ticket.push($("input[name='ticket_eind_datum\\[\\]']").map(function(){return $(this).val();}).get());
        ticket.push($("input[name='ticket_eind_tijd\\[\\]']").map(function(){return $(this).val();}).get());
        ticket.push($("input[name='ticket_aanal_max\\[\\]']").map(function(){return $(this).val();}).get());
        ticket.push($("input[name='ticket_aanal_min\\[\\]']").map(function(){return $(this).val();}).get());
        ticket.push($("input[name='person_amount\\[\\]']").map(function(){return $(this).val();}).get());
        tickets.push(ticket);
    });
    historyVar['tickets'] = tickets;
});
var i = 1;
var itickets = 1;

$(document).on('click','#js-addTickets', function() {
    var tickets = $('#js-tickets');
    var liData = '' +
        '<div class="m-top-12 js-ticket a-left u-border-bottom">' +
            '<div class="p-side-12"> ' +
                '<span class="small bold uppercase">Ticket Naam</span> ' +
                '<input name="ticket_naam[]" class="js-required m-top-6 form-input w-100 u-break" type="text" id="ticketNaam_' + i +'" placeholder="Bijv. Regular Ticket"> ' +
            '</div>' +
            '<div class="u-flex-row p-side-12 cell-H74"> ' +
                '<div class="m-right-24 u-flex"> ' +
                    '<span class="small bold uppercase">Aantal</span> ' +
                    '<input name="ticket_aantal[]" class="js-required m-top-6 form-input w-100 u-break" type="number" id="ticketAantal_' + i +'" placeholder="0"> ' +
                '</div>' +
                '<div class="m-right-24 u-flex"> ' +
                    '<span class="small bold uppercase">Prijs</span> ' +
                    '<span class="base small currency">&euro;</span> ' +
                    '<input name="ticket_prijs[]" class="js-price js-required m-top-6 euro form-input w-100 u-break" type="text" id="ticketPrijs_' + i +'" placeholder="12,50"> ' +
                '</div>' +
                '<div class="u-flex cell-w80"> ' +
                    '<span class="large u-pointer cell-lineheigt secondary_color-fixed ">' +
                        '<i class="js-gear m-right-12 Gear fa fa-cog" aria-hidden="true"></i>' +
                        '<i class="fa fa-trash-o js-removeTicket" aria-hidden="true"></i>' +
                    '</span> ' +
                '</div>' +
            '</div>' +
            '<div class="bg-gray p-around-12 js-more"> ' +
                '<div class="ticket-panel-error-container hidden">'+
                      '<div class="hidden startdate-error">Start datum kan niet voor na de eind datum zijn.</div>'+
                '</div>'+
                '<div class="u-flex-column-to-row"> ' +
                    '<div class="m-right-24 u-flex a-center p-top-12 m-bottom-6"> ' +
                        '<span class="base">Startdatum verkoop</span> ' +
                    '</div>' +
                    '<div class="m-right-24 u-flex"> ' +
                        '<input name="ticket_begin_datum[]" class="form-input m-right-6 w-100" readonly id="ticketStartDatum_' + i +'" placeholder="Begin datum" value="'+ date +'"> ' +
                    '</div>' +
                    '<div class="m-right-24 u-flex"> ' +
                        '<input value="00:00" name="ticket_begin_tijd[]" class="form-input w-100" type="time" id="ticketStartTijd_' + i +'" placeholder="Begin tijd"> ' +
                    '</div>' +
                '</div>' +
                '<div class="u-flex-column-to-row "> ' +
                    '<div class="m-right-24 u-flex a-center p-top-12 m-bottom-6"> ' +
                        '<span class="base">Einddatum verkoop</span> ' +
                    '</div>' +
                    '<div class="m-right-24 u-flex"> ' +
                        '<input name="ticket_eind_datum[]" class="form-input m-right-6 w-100" readonly id="ticketEindDatum_' + i +'" placeholder="Einddatum" value="'+start_date+'"> ' +
                    '</div>' +
                    '<div class="m-right-24 u-flex"> ' +
                        '<input name="ticket_eind_tijd[]" class="form-input w-100" type="time" id="ticketEindTijd_' + i +'" placeholder="Eindtijd" value="'+start_time+'"> ' +
                    '</div>' +
                '</div>' +
                '<div class="base m-top-12 m-bottom-12">Maximaal aantal tickets per bestelling</div>' +
                '<input name="ticket_aanal_max[]" class="form-input" type="number" id="ticketAantalMax_' + i +'" value="10">' +
                '<div class="base m-top-12 m-bottom-12">Personen per ticket</div>' +
                    '<input name="person_amount[]" class="form-input" type="number" id="ticketPerson_amount_' + i +'" value="1">' +
                '</div>' +
            '</div>' +

        '</div>';
    $(liData).appendTo(tickets);

    $('#ticketStartDatum_' + i).datepicker({
        format: 'yyyy-mm-dd'
    });
    $('#ticketEindDatum_' + i).datepicker({
        format: 'yyyy-mm-dd'
    });

    i++;
    itickets++;
    $('.js-price').priceFormat({
        prefix: '€ ',
        centsSeparator: ',',
        thousandsSeparator: '.',
        limit: 7,
        centsLimit: 2
    });
});


$(document).on('click','.js-removeTicket', function() {
    if(itickets > 1){
        $(this).parents('.js-ticket').slideUp("normal", function() { $(this).remove(); } );
        itickets--;
    }
});


$(document).on('click','.js-gear', function() {
    $(this).toggleClass('activeGear');
    $(this).closest(".js-ticket").find('.js-more').slideToggle();
});

$(document).on('focus','.form-error', function() {
   $(this).removeClass('form-error');
});
(function(e){e.fn.priceFormat=function(t){var n={prefix:"US$ ",suffix:"",centsSeparator:".",thousandsSeparator:",",limit:false,centsLimit:2,clearPrefix:false,clearSufix:false,allowNegative:false,insertPlusSign:false,clearOnEmpty:false};var t=e.extend(n,t);return this.each(function(){function m(e){if(n.is("input"))n.val(e);else n.html(e)}function g(){if(n.is("input"))r=n.val();else r=n.html();return r}function y(e){var t="";for(var n=0;n<e.length;n++){char_=e.charAt(n);if(t.length==0&&char_==0)char_=false;if(char_&&char_.match(i)){if(f){if(t.length<f)t=t+char_}else{t=t+char_}}}return t}function b(e){while(e.length<l+1)e="0"+e;return e}function w(t,n){if(!n&&(t===""||t==w("0",true))&&v)return"";var r=b(y(t));var i="";var f=0;if(l==0){u="";c=""}var c=r.substr(r.length-l,l);var h=r.substr(0,r.length-l);r=l==0?h:h+u+c;if(a||e.trim(a)!=""){for(var m=h.length;m>0;m--){char_=h.substr(m-1,1);f++;if(f%3==0)char_=a+char_;i=char_+i}if(i.substr(0,1)==a)i=i.substring(1,i.length);r=l==0?i:i+u+c}if(p&&(h!=0||c!=0)){if(t.indexOf("-")!=-1&&t.indexOf("+")<t.indexOf("-")){r="-"+r}else{if(!d)r=""+r;else r="+"+r}}if(s)r=s+r;if(o)r=r+o;return r}function E(e){var t=e.keyCode?e.keyCode:e.which;var n=String.fromCharCode(t);var i=false;var s=r;var o=w(s+n);if(t>=48&&t<=57||t>=96&&t<=105)i=true;if(t==8)i=true;if(t==9)i=true;if(t==13)i=true;if(t==46)i=true;if(t==37)i=true;if(t==39)i=true;if(p&&(t==189||t==109||t==173))i=true;if(d&&(t==187||t==107||t==61))i=true;if(!i){e.preventDefault();e.stopPropagation();if(s!=o)m(o)}}function S(){var e=g();var t=w(e);if(e!=t)m(t);if(parseFloat(e)==0&&v)m("")}function x(){n.val(s+g())}function T(){n.val(g()+o)}function N(){if(e.trim(s)!=""&&c){var t=g().split(s);m(t[1])}}function C(){if(e.trim(o)!=""&&h){var t=g().split(o);m(t[0])}}var n=e(this);var r="";var i=/[0-9]/;if(n.is("input"))r=n.val();else r=n.html();var s=t.prefix;var o=t.suffix;var u=t.centsSeparator;var a=t.thousandsSeparator;var f=t.limit;var l=t.centsLimit;var c=t.clearPrefix;var h=t.clearSuffix;var p=t.allowNegative;var d=t.insertPlusSign;var v=t.clearOnEmpty;if(d)p=true;n.bind("keydown.price_format",E);n.bind("keyup.price_format",S);n.bind("focusout.price_format",S);if(c){n.bind("focusout.price_format",function(){N()});n.bind("focusin.price_format",function(){x()})}if(h){n.bind("focusout.price_format",function(){C()});n.bind("focusin.price_format",function(){T()})}if(g().length>0){S();N();C()}})};e.fn.unpriceFormat=function(){return e(this).unbind(".price_format")};e.fn.unmask=function(){var t;var n="";if(e(this).is("input"))t=e(this).val();else t=e(this).html();for(var r in t){if(!isNaN(t[r])||t[r]=="-")n+=t[r]}return n}})(jQuery)
