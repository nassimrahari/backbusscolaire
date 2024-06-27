


jQuery(document).ready(function(){
    // Mettez ici votre code jQuery

    $('section.dashboard').css('display', 'block');
    $('.menu-item').click(function() {
    // Supprimer la classe active de tous les éléments de menu
        $('.menu-item').removeClass('active');

        // Ajouter la classe active à l'élément de menu cliqué

      /*  let sectionClass = $(this).attr('class').split(' ')[1];
        console.log(sectionClass);
        $('section').css('display', 'none');
        let sectionVisible='section'+'.'+sectionClass;
        console.log(sectionVisible);
        $(sectionVisible).css('display', 'block');*/
        $(this).addClass('active');
    });
});

$(window).on('load', function() {

  console.log("hhhhhhhh");
  $('form').submit(function() {
     $('#loader').css('display','hidden');
  });
});
