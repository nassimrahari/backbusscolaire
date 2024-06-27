$(window).on('load', function() {

  console.log("loader");
  $('form').submit(function() {
    $('#loader').css('display','flex');
  });
});