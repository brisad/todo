
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

$('.move-up').on('click', function () {
    var row = $(this).closest('tr');
    var name_id = $(this).closest('div.buttons').prev('a').attr('href');
    var section = $(name_id);

    section.insertBefore(section.prev('section'));
    row.insertBefore(row.prev());
});

$('.move-down').on('click', function () {
    var row = $(this).closest('tr');
    var name_id = $(this).closest('div.buttons').prev('a').attr('href');
    var section = $(name_id);

    section.insertAfter(section.next('section'));
    row.insertAfter(row.next());
});
