
    $(function(){
        var tablee = $('#maintable').on('draw.dt', function(type){
    
    
    
            tablee.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
                var data = this.data();
    
    
                // ... do something with data(), or this.node(), etc
            } );
    
        }).DataTable();
    
    
        
    
        $('#button_update_totals').click(function(){
    
            $.ajax({
                url: YT.urls['update_totals'],
                type: 'POST',
                data: {

                    'from_event_id': 0,
                    'to_event_id': 9999
    
                }
            })
            .done(function (msg) {
                if (msg.success === true) {
                    
                } else {
                    
                }
            });
            location.reload(); 
        });
    

    
    
    
    
   
});