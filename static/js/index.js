window.HELP_IMPROVE_VIDEOJS = false;

$(document).ready(function () {
  var slidesToShow = window.innerWidth < 768 ? 1 : 2;
  var options = {
    slidesToScroll: slidesToShow,
    slidesToShow: slidesToShow,
    pagination: false,
    loop: true,
    infinite: true,
    autoplay: false,
    autoplaySpeed: 3000,
  };

  var demoEl = document.querySelector('#demo-carousel');
  if (demoEl && typeof bulmaCarousel !== 'undefined') {
    bulmaCarousel.attach('#demo-carousel', options);
  }
});
