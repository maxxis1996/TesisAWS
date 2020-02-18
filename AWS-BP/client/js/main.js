$(document).ready(function(){
  var altura = $('.men').offset().top;

  $(window).on('scroll', function(){
    if ($(window).scrollTop()>altura){
      $('.men').addClass('men-fixed')
    }else{
      $('.men').removeClass('men-fixed')
    }
  });
});