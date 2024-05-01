function delete_image(el){
    var li_clone = $(el).closest('li').clone();
    li_clone.appendTo('#sourceList');

    $(el).closest('li').remove();

}
function showDestinationLoader(){
     YT.showLoader('#dropContainer');
}
function showSourceLoader(){
     YT.showLoader('#dragContainer');
}
function hideSourceLoader(){
    YT.hideLoader('#dragContainer');
}
function hideDestinationLoader(){
    YT.hideLoader('#dropContainer');
}

    var listItemTemplate = doT.template([
        '{{~ it.events :event }}',
            '<li class="list-group-item" data-id="{{=event.pk}}" data-event_id="{{=event.event__pk}}">',
                '<span data-name="event">{{=event.event__title }}&nbsp;</span>',
                '<span class="pull-right glyphicon glyphicon-move"></span>',
                '<span><img src="'+YT.urls.move_image+'" class="pull-right drag-icon"/></span>',
                '<span><img src="'+YT.urls.delete_image+'" onclick="delete_image(this)" class="pull-right delete-icon"/></span>',
            '</li>',
        '{{~}}'
    ].join(''));

    var sourceListTemplate = doT.template([
        '{{~ it.events :event }}',
            '<li class="list-group-item" data-event_id="{{=event.event__pk}}">',
                '<span data-name="event">{{=event.event__title}}</span>',
                '<img src="'+YT.urls.move_image+'" class="pull-right drag-icon"/>',
                '<span><img src="'+YT.urls.delete_image+'" onclick="delete_image(this)" class="pull-right delete-icon"/></span>',
            '</li>',
        '{{~}}'
    ].join(''));

function refresh_list(list_type, success_cb){

        var url = YT.urls.game_more_apps_list.replace('_placeholder', list_type);

        if(list_type == 'source'){
            showSourceLoader();
        }

        showDestinationLoader();
        $.get(url, function(response){
            if(response.success === true){
                var events = response['data'];
                if(list_type == 'destination') {
                    $('#destinationList').html(listItemTemplate({events: events, url: YT.urls.more_apps_delete}));
                    if(success_cb){
                        success_cb();
                    }
                    hideDestinationLoader();
                }else if(list_type == 'source'){

                    $('#sourceList').html(sourceListTemplate({
                        events: events,
                        create_url: YT.urls.more_apps_add
                    }));
                    if(success_cb) {
                        success_cb();
                    }
                    hideSourceLoader();
                }
            }else{
                YT.showSuccess('Error', "Could not retrieve the gamelist.");
            }
        });
    }

$(function(){

    $('#sourceFilter').keyup(function(){
        $('#sourceList').filterList({
            'event': $(this).val()
        });
    });
    $('#destinationFilter').keyup(function(){
        $('#destinationList').filterList({
            'event': $(this).val()
        });
    });

    $('#save-shop').click(function(){

        var $list_items = $('#destinationList').find('li');

        var data = [];
        for(var i=0;i<$list_items.length;i++){
            data.push($($list_items[i]).data('event_id'))
        }

        showDestinationLoader();

        $.ajax({
            url: $(this).data('url'),
            method: "post",
            data: {'items': data, use_in_iframe: $('[name="use_in_iframe"]').is(':checked')},
            success: function (data) {
                if(data.success === true){

                    window.location = data.redirect_to;

                }
        }});

    });

    /**
     * drag code
     */
    Sortable.create(document.getElementById('sourceList'), {
			sort: false,
			group: {
                name: 'advanced',
                pull: true,
                put: false
            },
            handle: '.drag-icon',
			animation: 150,
            onStart: function (/**Event*/evt) {
                $('#dropContainer').addClass('dragliststart');
            },
            onEnd: function(evt){
                $('#dropContainer').removeClass('dragliststart');
            }

		});



    // $(document.body).on('click', '[data-dismiss="modal"]' , function () {
    //     hideDestinationLoader();
    //     refresh_list('destination');
    //     refresh_list('source')
    // });

    Sortable.create(document.getElementById('destinationList'), {
        sort: true,
        group: {
            name: 'advanced',
            pull: 'clone',
            put: true
        },
        handle: '.drag-icon',
        animation: 150,
        // Changed sorting within list
        onUpdate: function (/**Event*/evt) {
            // showDestinationLoader();
            //
            // var url = YT.urls.more_apps_position.replace('_placeholder_event_id', $(evt.item).data('id')).replace('_placeholder_position', evt.newIndex+1);
            // $.ajax({
            //     url: url,
            //     method: "get",
            //     success: function (data) {
            //         if(data.success === true){
            //             hideDestinationLoader();
            //             refresh_list('destination');
            //             refresh_list('source')
            //
            //         }
            // }});

        },
        onAdd: function (/**Event*/evt) {
            // disabled this in favor of the opslaan button
            // showDestinationLoader();
            //
            // var url = YT.urls.more_apps_add.replace('_placeholder', $(evt.item).data('id')).replace('_position', evt.newIndex+1);
            // $.ajax({
            //     url: url,
            //     method: "get",
            //     success: function (data) {
            //         if(data.success === true){
            //             hideDestinationLoader();
            //             refresh_list('destination');
            //             refresh_list('source')
            //
            //         }
            // }});
        }
    });



    // $0.click(function(){
    //     console.log('yeah')
    // })




    refresh_list('destination');
    refresh_list('source');
});