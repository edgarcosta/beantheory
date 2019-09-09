
function getCookie(name) {
    var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
}

$(document).ready(function () {
    console.log("ready");
    $('.button-toggle').click(
    function (evt) {
    evt.preventDefault();
    var label = $(this).attr('id');
    console.log("label = " + label);
    var talks = $('ul.talks').find('li.' + label);
    if( $(this).text() == 'Show' ) {
      talks.show("fast");
      document.cookie = label + '=True;path=/';
      $(this).text('Hide');
    } else {
      talks.hide("fast");
      document.cookie = label + '=False;path=/';
      $(this).text('Show');
    }
    console.log(document.cookie);
    return false;
    });

  $('.ical-toggle').click(
    function (evt) {
      evt.preventDefault();
      icons = $('.ical-detail').toggle("fast");
      return false;
    });

  var buttons = $('.button-toggle');
  for(let i = 0; i < buttons.length; i++){
    let label = buttons[i].getAttribute('id');
    if( getCookie(label) == 'False' ) {
      $('ul.talks').find('li.' + label).hide();
      buttons[i].click();
    }
  }
});
