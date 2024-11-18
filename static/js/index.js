var $grid = $('.collection-list').isotope({
    layoutMode: 'fitRows',
    originLeft: false,
    });
    
    // Rest of your code remains the same
    $('.filter-button-group').on('click', 'button', function() {
    var filterValue = $(this).attr('data-filter');
    resetFilterBtns();
    $(this).addClass('active-filter-btn');
    $grid.isotope({ filter: filterValue });
    });
    
    var filterBtns = $('.filter-button-group').find('button');
    function resetFilterBtns() {
    filterBtns.each(function() {
      $(this).removeClass('active-filter-btn');
    });
    }