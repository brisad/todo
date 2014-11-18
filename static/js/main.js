
$('#login').on("click", function () {
  $('#login-form').submit();
});

$('#add').on("click" ,function () {
  $('#add-form').submit();
});

$('#loginModal').on('shown.bs.modal', function () {
  $('#username').focus();
})

$('#addModal').on('shown.bs.modal', function () {
  $('#name').focus();
})

$('#loginModal form').keypress(function (e) {
  if (e.which == 13) {
    $('#login-form').submit();
  }
});

$('#addModal form').keypress(function (e) {
  if (e.which == 13) {
    $('#add-form').submit();
  }
});

$('.move-up').on('click', function () {
  var row = $(this).closest('tr');
  var name_id = $(this).closest('div.buttons').prev('a').attr('href');
  var section = $(name_id);

  section.insertBefore(section.prev('.task'));
  row.insertBefore(row.prev());

  $.post("move_up", { item: name_id.substr(1) });
});

$('.move-down').on('click', function () {
  var row = $(this).closest('tr');
  var name_id = $(this).closest('div.buttons').prev('a').attr('href');
  var section = $(name_id);

  section.insertAfter(section.next('.task'));
  row.insertAfter(row.next())

  $.post("move_down", { item: name_id.substr(1) });
});

$('.remove-item').on('click', function () {
  var row = $(this).closest('tr');
  var name_id = $(this).closest('div.buttons').prev('a').attr('href');
  var section = $(name_id);

  if (confirm("This will remove the item!")) {
    section.remove();
    row.remove();

    $.post("remove", { item: name_id.substr(1) });
  }
});
