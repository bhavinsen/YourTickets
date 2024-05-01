$(function(){

    $("#orderform").submit(function(e) {

        setErrorMessageText($('#message_noticketselected').html());

        if ($("#Terms").is(':checked')){

        }else{
            setErrorMessageText($('#message_akkoordvoorwaarden').html());
            $(".errormessage").addClass('active');
            e.preventDefault();
        }
        //if covid info is shown
        if($('[name="show_covid19_info"]').length > 0){
            if ($("#show_covid19_info").is(':checked')){

            }else{
                setErrorMessageText($('#message_covid').html());
                $(".errormessage").addClass('active');
                e.preventDefault();
            }
        }

    });


    $(document).on('click','.button-bottom-right', function() {
      boxes();
    });
    function boxes() {
      var anyFilled = false;

      var boxes = $('input:visible');

      for(var i = 0; i < boxes.length; i++) {
          if(boxes[i].value > 0) {
              anyFilled = true;
              break;
          }
      }

      if(!anyFilled){
        event.preventDefault();
        $(".errormessage").addClass('active')
      }
    }
    function setErrorMessageText(text){
        $(".errormessage").html(text);
    }
    $(document).on('click','.errormessage', function() {
      $(".errormessage").removeClass('active');
        setErrorMessageText($('#message_noticketselected').html());
    });
    $(document).on('click','.js-addNumber', function() {
      $(".errormessage").removeClass('active');
        setErrorMessageText($('#message_noticketselected').html());
    });
});