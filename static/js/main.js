
$('#login').on("click", function () {
  $('#login-form').submit();
});

$('#loginModal').on('shown.bs.modal', function () {
  $('#username').focus();
})

$('#loginModal form').keypress(function (e) {
  if (e.which == 13) {
    $('#login-form').submit();
  }
});
