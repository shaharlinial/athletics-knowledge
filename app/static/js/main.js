$(document).ready(function() {
    // Make an API request to Flask backend
    $.ajax({
        url: '/api/data',
        type: 'GET',
        success: function(data) {
            $('#message').text(data.message);
        },
        error: function(error) {
            console.error('Error fetching data:', error);
        }
    });
});