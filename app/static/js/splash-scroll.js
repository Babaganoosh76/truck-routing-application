$(document).ready(function(){
  $(".nav a, #services a, #rentals a").on('click', function(e) {
    e.preventDefault();
    scrollTo(this.hash);
  });
  
  // $(window).scroll(function() {
  //   $(".addSlide").each(function(){
  //     var pos = $(this).offset().top;
  //     var winTop = $(window).scrollTop();
  //     if (pos < winTop + $(window).height()) {
  //       $(this).addClass("slide");
  //     }
  //   });
  // });
});

function scrollTo(hash) {
  $('html, body').animate({
    scrollTop: $(hash).offset().top
  }, 700, function(){
    // window.location.hash = hash;
  });
}
