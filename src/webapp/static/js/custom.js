function safeConfirm(message) {
  if (confirm(message))
      return true;
  else
    return false;
}
$(document).ready(function () {
    var text = $('ul.sidebar-nav').find('li.active>a').text();
    if (text != 'Home'){
        $('#base-body').prepend('<h2 style="margin-top:-1px">'+text+'</h2><hr>');
    }

    $('#display_flash').fadeIn().delay(1500).fadeOut();
    $("select").addClass("form-control");
    $('td:last-child').addClass("list-buttons-column");
    if ($('.filters tr').length){
        $('.pull-right > .btn-primary').removeAttr('style');
    }
});
$("#wrapper").css('padding-left',localStorage['wrapper']);
$("#sidebar-wrapper").css('width',localStorage['wrapper']);
$("#menu-toggle").click(function () {
    if (localStorage['wrapper'] === '0px'){
        localStorage['wrapper'] = '250px';
    }else{
        localStorage['wrapper'] = '0px';
    }
    $("#wrapper").css('padding-left',localStorage['wrapper']);
    $("#sidebar-wrapper").css('width',localStorage['wrapper']);

});

