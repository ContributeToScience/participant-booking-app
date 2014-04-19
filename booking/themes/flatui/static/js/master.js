window.odometerOptions = {
	format: 'd'
};

$(function() {
	$(".navbar .nav > li > a").bind('click', function() {
		var $panelScrollTo = $($(this).attr('href'));
		$.scrollTo($panelScrollTo, 500)
	});
    $('#donate .row .col2 div .price').bind('inview', function(event, isInView, visiblePartX, visiblePartY) {
        if (isInView) { // element is now visible in the viewport
            if (visiblePartY == 'top') { // top part of element is visible

            } else if (visiblePartY == 'bottom') { // bottom part of element is visible

            } else { // whole part of element is visible
                $(this).find('.odometer').html('2000');
            }
        } else { // element has gone out of viewport
            $(this).find('.odometer').html('0');
        }
    });
    $("#top-wrap header .logo, #top-wrap header h1").fadeIn(1000);
})