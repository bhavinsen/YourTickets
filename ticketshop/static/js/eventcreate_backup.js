var historyVar = [];
var token = "EAACEdEose0cBALGbBJZCEY0HM8fq7EbecIM0ocvuoQLbUSvBJUNJdEg9arvVZB5ZBD6CtRONkwlk1eOxeZB9eUn6g0flCoFt9DCj9F4ZAs9CaIu0UGOkyctVx3MLN2Dlea57viZCekNRwTXaslaXDaLC8ZBgARelwjRIfq49BIAewZDZD";
$.ajaxSetup({
  cache: true
});
$.getScript('//connect.facebook.net/en_US/sdk.js', function() {
  FB.init({
    appId: '200973763316497',
    version: 'v2.5'
  });
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
$('#form1').on('submit', function(e) { //use on if jQuery 1.7+
    e.preventDefault();
    form1();
});
$('#js-next-1').click(function() {
  form1();
  $(document).scrollTop(0);
});
if (window.location.hash.substr(1)) {
  $('article').load(createtwo_url);
  historyVar['eventId'] = window.location.hash.substr(1);
  getEventData();
}
function form1() {
  $('article').load(createtwo_url);
   var element = $('#eventurl'),
       event;
   if (element.val() != "") {
      id = $(element).val();

      window.location.hash = id;
      historyVar['eventId'] = id;
    }
    getEventData();
};
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
};

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
        if (flag == 1){
          $(document).scrollTop(0);
          $('article').load(createthree_url);
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
          eArtist = 1;
      $(document).on('click','#js-addArtist', function() {
        var artist = $('#js-artist');
        var liData = '<div class="artist js-artist u-desktop-placeholder u-flex-row p-top-12 u-border-top"><input name="artiest_naam[]" class="small m-right-24 form-input w-100 cell-10 u-flex u-break" type="text" id="artiestNaam_' + i +'" placeholder="Artiest naam"><input name="artiest_url[]" class="form-input small m-right-24 w-100 cell-10 u-flex u-break" type="text" id="artiestURL_' + i +'" placeholder="Artiestenpagina of website"><span class="artist-line js-removeArtist cell-w40 large u-pointer secondary_color-fixed"><i class="fa fa-trash-o" aria-hidden="true"></i></span></div>';
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
          tickets.push(ticket);
        });
                  historyVar['tickets'] = tickets;
      });
      var i = 1;
          itickets = 1;
      $(document).on('click','#js-addTickets', function() {
        var tickets = $('#js-tickets');
        var liData = '<div class="m-top-12 js-ticket a-left u-border-bottom"> <div class="p-side-12"> <span class="small bold uppercase">Ticket Naam</span> <input name="ticket_naam[]" class="js-required m-top-6 form-input w-100 u-break" type="text" id="ticketNaam_' + i +'" placeholder="Bijv. Regular Ticket"> </div><div class="u-flex-row p-side-12 cell-H74"> <div class="m-right-24 u-flex"> <span class="small bold uppercase">Aantal</span> <input name="ticket_aantal[]" class="js-required m-top-6 form-input w-100 u-break" type="number" id="ticketAantal_' + i +'" placeholder="0"> </div><div class="m-right-24 u-flex"> <span class="small bold uppercase">Prijs</span> <span class="base small currency">€</span> <input name="ticket_prijs[]" class="js-required m-top-6 euro form-input w-100 u-break" type="text" id="ticketPrijs_' + i +'" placeholder="12,50"> </div><div class="u-flex cell-w80"> <span class="large u-pointer cell-lineheigt secondary_color-fixed "><i class="js-gear m-right-12 Gear fa fa-cog" aria-hidden="true"></i><i class="fa fa-trash-o js-removeTicket" aria-hidden="true"></i></span> </div></div><div class="bg-gray p-around-12 js-more"> <div class="u-flex-column-to-row"> <div class="m-right-24 u-flex a-center p-top-12 m-bottom-6"> <span class="base">Startdatum verkoop</span> </div><div class="m-right-24 u-flex"> <input name="ticket_begin_datum[]" class="form-input m-right-6 w-100" type="date" id="ticketBeginDatum_' + i +'" placeholder="Begin datum"> </div><div class="m-right-24 u-flex"> <input name="ticket_begin_tijd[]" class="form-input w-100" type="time" id="ticketBeginTijd_' + i +'" placeholder="Begin tijd"> </div></div><div class="u-flex-column-to-row "> <div class="m-right-24 u-flex a-center p-top-12 m-bottom-6"> <span class="base">Einddatum verkoop</span> </div><div class="m-right-24 u-flex"> <input name="ticket_eind_datum[]" class="form-input m-right-6 w-100" type="date" id="ticketEindDatum_' + i +'" placeholder="Einddatum"> </div><div class="m-right-24 u-flex"> <input name="ticket_eind_tijd[]" class="form-input w-100" type="time" id="ticketEindTijd_' + i +'" placeholder="Eindtijd"> </div></div><div class="base m-top-12 m-bottom-12">Aantal tickets per bestelling</div><div class="u-flex-column-to-row"> <div class="m-right-24 u-flex"> <span class="base m-right-12">Min:</span> <input name="ticket_aanal_min[]" class="form-input" type="number" id="ticketAantalMin_' + i +'" placeholder="1"> </div><div class="u-flex"> <span class="base m-right-12">Max:</span> <input name="ticket_aanal_max[]" class="form-input" type="number" id="ticketAantalMax_' + i +'" placeholder="10"> </div></div></div></div>';
          $(liData).appendTo(tickets);
        i++;
        itickets++;
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
