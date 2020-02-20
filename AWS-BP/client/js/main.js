$(document).ready(function(){
  var altura = $('.men').offset().top;
  
  $(window).on('scroll', function(){
    if ($(window).scrollTop()>altura&&$(window).width()>640){
      $('.men').addClass('men-fixed')
    }else{
      $('.men').removeClass('men-fixed')
    }
    if($(window).scrollTop()>altura&&$(window).width()<640){
      $('.icon').addClass('men-fixed')
    }else{
      $('.icon').removeClass('men-fixed')
    }

  });
});