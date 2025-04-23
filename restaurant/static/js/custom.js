// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

$(document).ready(function () {
  var $grid = $(".grid").isotope({
    itemSelector: ".all",
    layoutMode: 'fitRows'
  });

  let currentCategoryFilter = '*';

  $('.filters_menu li').click(function () {
    $('.filters_menu li').removeClass('active');
    $(this).addClass('active');
    currentCategoryFilter = $(this).attr('data-filter') || '*';
    updateCombinedFilter();
  });

  $('.dietary-checkbox').on('change', updateCombinedFilter);

  function updateCombinedFilter() {
    const selectedDietaries = Array.from($('.dietary-checkbox:checked'))
      .map(cb => '.' + cb.value.trim().toLowerCase().replace(/\s+/g, '-'));

    const dietaryFilter = selectedDietaries.join('');
    const combinedFilter = currentCategoryFilter + dietaryFilter || '*';

    console.log("combined filter:", combinedFilter);
    $grid.isotope({ filter: combinedFilter });
  }
});

// nice select
$(document).ready(function() {
    $('select').niceSelect();
  });

/** google_map js **/
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

// client section owl carousel
$(".client_owl-carousel").owlCarousel({
    loop: true,
    margin: 0,
    dots: false,
    nav: true,
    navText: [],
    autoplay: true,
    autoplayHoverPause: true,
    navText: [
        '<i class="fa fa-angle-left" aria-hidden="true"></i>',
        '<i class="fa fa-angle-right" aria-hidden="true"></i>'
    ],
    responsive: {
        0: {
            items: 1
        },
        768: {
            items: 2
        },
        1000: {
            items: 2
        }
    }
});