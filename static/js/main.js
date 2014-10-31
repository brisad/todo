
$('#login').on("click", function () {
    $('#login-form').submit();
});

$('#loginModal').on('shown.bs.modal', function () {
    $('#username').focus();
})
