$('#add-entry').submit(function(event) {
    event.preventDefault();

    $.ajax({
        url: '/add_json',
        type: 'POST',
        dataType: 'json',
        data: $('#add-entry').serialize(),
        success: function(response){
            console.log(response);
        }
    });
});


// $(document).on('submit', function(event) {
//     event.preventDefault();
//     var data = $('#add-form').serialize();
//     $.post('/add_ajax', data);
// });
