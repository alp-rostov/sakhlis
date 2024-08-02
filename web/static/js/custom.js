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
            let to = $(this).parent().parent("section").next().attr("id");
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
