/**
 * Created by cameron on 3/24/18.
 */
$(function() {
    $('button').click(function() {
        var user = $('#txtUsername').val();
        var pass = $('#txtPassword').val();
        $.ajax({
            url: '/progress',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
