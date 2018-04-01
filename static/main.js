$('document').ready(function() {
    $('.dialog-box').hide();
    $('.close-icon').hide();
    $('.login-signup-modal').hide();
    $('.signup-fomr').hide();
});

$('.saksham-bot').click(function () {
    $('.dialog-box').toggle(500);
    $('.close-icon').toggle(500);
    $('.bot-icon').toggle(500);

});

$('.login-button').click(function () {
    $('.login-signup-modal').toggle(500);
});


