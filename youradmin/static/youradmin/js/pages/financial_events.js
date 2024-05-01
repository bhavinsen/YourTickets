window.truefalse_field_renderer_marker = function(data, type, row, meta){
    var color = data==true ? 'green' : 'red';

    var html = '<span data-id="'+row.pk+'" data-toggle="'+!data+'" style="color:'+color+'" class="glyphicon glyphicon-ok marker-element"></span>';
    return html;
}

$(function(){
    var tablee = $('#maintable').on('draw.dt', function(type){

        $.ajax({
            url: YT.urls['get_total'],
            type: 'POST',
            data: {
                'start_date':$('#start_date').val(),
                'end_date': $('#end_date').val(),
                'title': $('#title').val(),
                'event_id': $('#event_id').val()

            }
        })
        .done(function (msg) {
            if (msg.success === true) {
                $('#info_total_order_amount').html(msg.data.total_orders_amount.toLocaleString());
                $('#info_total_service_costs').html(msg.data.total_service_costs.toLocaleString());
                $('#info_total_order_payout').html(msg.data.total_payd.toLocaleString());
                $('#info_total_still_to_pay').html(msg.data.total_still_to_pay.toLocaleString());
                $('#info_total_tickets_sold').html(msg.data.total_tickets_sold.toLocaleString())
            } else {
                // YT.showError('Error',msg.error,panel.find('.alert-danger'))
            }
            // YT.hideLoader(panel_body);
        });

        tablee.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
            var data = this.data();

            if(data.fields.saldo == '0' || data.fields.saldo == '0.00'){
                $(this.node()).addClass('row_payed');
            }else{
                $(this.node()).addClass('row_not_payed');
            }
            // ... do something with data(), or this.node(), etc
        } );

    }).DataTable();


    $(document.body).on('click', '.marker-element', function(){

        var url = YT.urls.mark_event.replace('_placeholder', $(this).data('id'));

        YT.showLoader($(this).parent(),'width:20px;');

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'mark':$(this).data('toggle')
            }
        })
        .done(function (msg) {
            if (msg.success === true) {
                tablee.draw()
            } else {

            }
            YT.hideLoader($(this).parent());

        });
    });

    $('#button_filter').click(function(){

        if($('#event_id').val() != ''){
            tablee.columns(0).search($('#event_id').val());
        }else{
            tablee.columns(0).search('');
        }

        if($('#title').val() != ''){
            tablee.columns(1).search($('#title').val());
        }else{
            tablee.columns(1).search('');
        }
        if($('#start_date').val() != ''){
            tablee.columns(2).search($('#start_date').val());
        }else{
            tablee.columns(2).search('');
        }
        if($('#end_date').val() != ''){
            tablee.columns(3).search($('#end_date').val());
        }else{
            tablee.columns(3).search('');
        }

        if($('#marked').prop('checked')){
            tablee.columns(7).search($('#marked').prop('checked'));
        }else{
            tablee.columns(7).search('');
        }
        tablee.draw();

    });

    $('#start_date_picker').datetimepicker({
        'format': 'YYYY-MM-DD'
    });
    $('#end_date_picker').datetimepicker({
        'format': 'YYYY-MM-DD'
    });

// $('#total_start_date_picker').datetimepicker({
//     'format': 'YYYY-MM-DD'
// });
// $('#total_end_date_picker').datetimepicker({
//     'format': 'YYYY-MM-DD'
// });
// $('#end_date_picker').on("dp.change", function (e) {
//     tablee.columns(3).search($('#end_date').val()).draw();
// });


});
