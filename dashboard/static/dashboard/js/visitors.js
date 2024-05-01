function ticket_delete(row, data){
    var image = $("#remove_template").html();

    return image.replace('placeholder', row.id);
}

$(function(){
    var table = $('#maintable').DataTable();
    var orriginal_url = table.ajax.url();

    $(document).on('click', '.btn-remove-ticket', function(){

        var el = $(this);

        $('#message-ticket-deleted').addClass('hidden');


        $.ajax({
                url: el.data('url'),
                type: 'POST',
                //data: postData,
                contentType: false,
                processData: false
            }).done(function(msg){
                if (msg.success === true) {
                    $('#message-ticket-deleted').removeClass('hidden');
                    table.ajax.reload(null, false);
                } else {
                    console.log('iet ok')

                }
            });


    });

    $('.visitors-list').click(function(){

        var ticket_id= $(this).data('ticket_id');
        $('#message-ticket-deleted').addClass('hidden');

        if(ticket_id == 'guest_ticket'){
            $('#remove_template').find('.btn-remove-ticket').removeClass('hidden');
            //$('#maintable').
        }else if(ticket_id == 'special_guest_ticket'){
            $('#remove_template').find('.btn-remove-ticket').removeClass('hidden');
            $('#maintable').find('.btn-remove-ticket').removeClass('hidden');
        }else{
            $('#remove_template').find('.btn-remove-ticket').addClass('hidden');
            //$('#maintable').find('.btn-remove-ticket').addClass('hidden');
        }

        var url = orriginal_url.replace('placeholder', ticket_id);
        table.ajax.url(url).load();

        /**
         * set the url for the download button
         */
        $('#download_csv').attr('href', $('#download_csv').data('url').replace('placeholder', ticket_id) );

        var inst = $('[data-remodal-id=visitors_per_ticket]').remodal();
        inst.open();
    });

    var import_type = '';

    $('.import-file').click(function(){
        var inst = $('[data-remodal-id=import-file]').remodal();

        $('#mass-tickets-send-with').hide();
        $('#mass-tickets-send-without').hide();

        // link = $(this).data('href');
        import_type = $(this).data('ticket_type');
        inst.open();
        $('#import-file-step1').show();
        $('#import-file-step2').hide();
    });

    var sheetData = {};

    var container = $('#import-file-step2-container');

    container.find('select').change(function(){

        var cur_object = $(event.target);

        //nothing new selected
        if(cur_object.val() == cur_object.data('last_value')){
            return;
        }

        container.find('select[name="select_as"]').each(function (index, obj) {
            obj = $(obj);
            if ($(obj).attr('id') == cur_object.attr('id')) {
                return true;
            }

            //if "-" selected
            //and the last value was different then empty
            //add last value to all other dropdowns

            //from email to '-'
            if(cur_object.val() == '-' && cur_object.data('last_value') !== undefined){
                add_option(obj, cur_object.data('last_value'))

            }else{
                if(cur_object.data('last_value') !== undefined && cur_object.data('last_value') != '-'){
                    add_option(obj, cur_object.data('last_value'))
                }
            }

            //only remove if value selected is different then "-"
            if(cur_object.val() != '-') {
                remove_option(obj, cur_object.val());
            }


        });
        //store the last value
        cur_object.data('last_value', cur_object.val());

    });

    function add_option(targetSelect, value){
        targetSelect.append('<option value="'+value+'">'+value+'</option>');
    }

    function remove_option(targetSelect, value){
        targetSelect.find('option[value="' + value + '"]').remove();
    }


    $('#import-file-sendbutton').click(function(){

        var container = $('#import-file-step2-container');

        var sub_containers = container.find('div.m-right-36-desk');

        var counter = 0;
        var max = 3;

        //validate
        var container = $('#import-file-step2-container');

        var name = false;
        var email = false;

        container.find('select[name="select_as"]').each(function (index, obj) {
            obj = $(obj);

            if(obj.val() == 'email'){
                email = true;
            }else if(obj.val() == 'name'){
                name = true;
            }

        });

        if(name == true && email == true){
            $('#import-file-errors-selection').hide();

            var counter = 0;

            var selects = container.find('select[name="select_as"]');

            for(var colname in sheetData){
                sheetData[colname] = $(selects[counter]).val();

                counter++;
            }

            var reversed_sheetData = {};

            for(var xlsname in sheetData){
                reversed_sheetData[sheetData[xlsname]] = xlsname;
            }

            reversed_sheetData.csrfmiddlewaretoken = $("#import-file-step2").find('input[name="csrfmiddlewaretoken"]').val();

            reversed_sheetData['ticket_type'] = import_type;

            $.ajax({
                url: $("#import-file-step2").data('url'),
                method: "post",
                //processData: false,
                //contentType: false,
                data: reversed_sheetData,
                success: function (data) {
                    if(data.success === true){
                        $('#mass-tickets-send-'+import_type).show();
                        var inst = $('[data-remodal-id=import-file]').remodal();
                        inst.close();

                    }
                }});


        }else{
            $('#import-file-errors-selection').show();
        }

    });

    $('#import-file-button').click(function(){

        var data = new FormData();

        //Form data
        var form_data = $('#import-file-form').serializeArray();
        $.each(form_data, function (key, input) {
            data.append(input.name, input.value);
        });

        //File data
        var file_data = $('input[name="importfile"]')[0].files;
        data.append("importfile", file_data[0]);

        $('#import-file-errors').hide();

        $.ajax({
            url: $("#import-file-form").data('url'),
            method: "post",
            processData: false,
            contentType: false,
            data: data,
            success: function (data) {
                if(data.success == false){
                    $('#import-file-errors').show();
                }else{
                    $('#import-file-step1').hide();
                    $('#import-file-step2').show();
                    var sheet = data.sheet;
                    //external save sheet for later use
                    //sheetData = sheet;

                    var container = $('#import-file-step2-container');

                    var sub_containers = container.find('div.m-right-36-desk');

                    var counter = 0;
                    var max = 3;
                    for(var colname in sheet){
                        var rows = sheet[colname];
                        sheetData[colname] = '';
                        //add column name
                        var sub_container = $(sub_containers[counter]);
                        var record_container = sub_container.find('.records');
                        record_container.html('');

                        sub_container.find('.import-file-colname').html(colname);

                        for(var i=0;i<rows.length;i++){
                            record_container.append('<div style="width:100%;padding:10px;text-align:left;border-bottom:2px solid #f5f4f4;">'+rows[i]+'</div>')

                            if(i === max){
                                break;
                            }
                        }
                        sub_container.show();
                        //break
                        if(counter === max){
                            break;
                        }
                        counter ++
                    }
                }
            },
            error: function (e) {
                //error
            }
        });
    });
});