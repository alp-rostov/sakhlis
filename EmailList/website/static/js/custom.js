 
/* ================ Contact form ajax ================ */

   jQuery(document).ready(function(){

    $('#contactform').submit(function(){

        var action = $(this).attr('action');

        $("#message").slideUp(500, function(){
            $('#message').hide(1000);

            $.post(action, {
                    name: $('#name').val(),
                    home: $('#home').val(),
                    phone: $('#phone').val(),
                    comments: $('#comments').val(),
                },
                function(data){
                    document.getElementById('message').innerHTML = data;
                    $('#message').slideDown('slow');
                    $('#submit').removeAttr('disabled');
                    if(data.match('success') !== null) $('#contactform').slideUp('slow');

                }
            );

        });

        return false;
        
            });
			
	/* ================ Masked Input ================ */

	$('input[name="phone"]').mask("");
        
        });

/* ================ PageScroll2id ================ */

		(function($) {
					$(window).on("load", function() {

						/* Page Scroll to id fn call */
						$("#navigation-menu a,a[href='#top'],a[rel='m_PageScroll2id']").mPageScroll2id({
							highlightSelector: "#navigation-menu a"
						});

						/* demo functions */
						$("a[rel='next']").click(function(e) {
							e.preventDefault();
							var to = $(this).parent().parent("section").next().attr("id");
							$.mPageScroll2id("scrollTo", to);
						});

					});
		 })(jQuery);
 
 /* ================ Services ================ */
 
		 $('.owl-carousel').owlCarousel({
			loop:true,
			margin:20,
			responsiveClass:true,
			responsive:{
				0:{
					items:1,
					nav:true
				},
				600:{
					items:2,
					nav:false
				},
				1000:{
					items:3,
					nav:true,
					loop:false
				}
			}
		})

/* ================ Counter ================ */

        $('.counter-item').appear(function() {
            $('.counter-number').countTo();
        });

/* ================ Typed ================ */

		var typed2 = new Typed('#typed2', {
			strings: ['<span class="font-weight-bold"><strong class="browns">Со скидкой - 10%</span</strong></span>', '<span class="font-weight-bold"><strong class="browns">смета бесплатно!</strong></span>'],
			typeSpeed: 120,
			backSpeed: 120,
			fadeOut: true,
			loop: true
		});

/* ================ Back to top button ================ */

$(document).ready(function() {

  //Check to see if the window is top if not then display button
  $(window).scroll(function() {
    // Show button after 100px
    var showAfter = 200;
    if ($(this).scrollTop() > showAfter) {
      $('.back-to-top').fadeIn();
    } else {
      $('.back-to-top').fadeOut();
    }
  });

  //Click event to scroll to top
  $('.back-to-top').click(function() {
    $('html, body').animate({
      scrollTop: 0
    }, 800);
    return false;
  });

});