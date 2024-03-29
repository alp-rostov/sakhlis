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

/* ================ showing form ===  using in templates orderlist, ordersearchform ================ */

function show_create_order_form(form) {
    if (form.style.display == "none") {
        $('#form').fadeIn("slow", function() {
                            form.style.display = "block";
                            $('#link_create_order_form').html('X');
                   });
    }
    else {
        $('#form').fadeOut("slow", function(){
                       form.style.display = "none";
                       $('#link_create_order_form').html('Create the order');
                   });
    }
}

/* ================ using in templates orderlist for paginator ================ */

function add_order_in_html_object(r) {
    g=$("#row_order").clone();
    g.attr("class", "row p-1 mb-1");
    g.attr("id", "row_order"+r.pk);

    g.find("#order_").attr("href", "list_order/"+r.pk);
    g.find("#order_").html("Заявка №"+r.pk);
    let date_order=r.time_in.substr(0, 10).split("-").reverse().join(".");
    g.find("#time_in").html(date_order);

    g.find("#delete_").attr("href", "invoice/delete-order/"+r.pk);
    g.find("#delete_").attr("id", "delete_"+r.pk);

    g.find(".copy").attr("id", r.pk);

    g.find("#edit_").attr("href", "../list_order/update/"+r.pk);
    g.find("#edit_").attr("id", "edit_"+r.pk);

    g.find("#text_order_").html(r.text_order);
    g.find("#text_order_").attr("id", "text_order_"+r.pk);

    g.find("#customer_name_").html(" "+r.customer_name);
    g.find("#customer_name_").attr("id", "customer_name_"+r.pk);

    g.find("#customer_phone_").attr("href", "tel:"+r.customer_phone);
    g.find("#customer_phone_").html(" "+ r.customer_phone);
    g.find("#customer_phone_").attr("id", "customer_phone_"+r.pk);

    g.find("#customer_telegram_").attr("href", "https://t.me/"+r.customer_telegram);
    g.find("#customer_telegram_").html(" @"+r.customer_telegram);
    g.find("#customer_telegram_").attr("id", "customer_telegram_"+r.pk);

    g.find("#city_").html('Тбилиси');
    g.find("#city_").attr("id", "city_"+r.pk);

    g.find("#street_app_").html(r.address_street_app);
    g.find("#street_app_").attr("id", "street_app_"+r.pk);

    g.find("#num_").html(r.address_num);
    g.find("#num_").attr("id", "num_"+r.pk);

    if (r.location_longitude) {
        g.find("#map_").attr("href", 'https://yandex.ru/maps/?pt='+r.location_longitude+','+r.location_latitude+'&z=18&l=map');
        g.find("#map_").attr("id", "map_"+r.pk);
        g.find("#map_icon").attr("class", "fas fa-map-marker prefix text-secondary mt-3");
    }
    else {
        g.find("#map_").attr("onclick", "copyToClipboard($(this))");
        g.find("#map_").attr("title", "Copy address");
        g.find("#map_").attr("id", "map_"+r.pk);
    }
    return g;
 }

/* ================ copy address name to clipboard ======  using in card_for_order ============= */

function copyToClipboard(element) {
    let address = $(element).html().replace(/(<([^>]+)>)/gi, '');
    address=address.replaceAll('  ','' ).trim();
    window.navigator.clipboard.writeText(address);
}

/* ================ copying order`s information in form  ======  using in card_for_order ============= */

$(document.body).on( "click", ".copy", function(e) {
    let customer_name_pk="customer_name_"+$(this).attr('id');
    let name=$('#'+customer_name_pk).html();


    let customer_phone_pk="customer_phone_"+$(this).attr('id');
    let phone=$('#'+customer_phone_pk).html().trim();


    let customer_telegram_pk="customer_telegram_"+$(this).attr('id');
    let telegram=$('#'+customer_telegram_pk).html().trim();

    let customer_street_pk="street_app_"+$(this).attr('id');
    let street=$('#'+customer_street_pk).html();

    let num_house_pk="num_"+$(this).attr('id');
    let num_house=$('#'+num_house_pk).html();

    $('#form').fadeIn("slow", function(){
        form.style.display = "block";
        form.reset();
        $('#link_create_order_form').html('X');
        $('[name="customer_name"]').attr("value", name);
        $('[name="customer_phone"]').attr("value", phone);
        $('[name="customer_telegram"]').attr("value", telegram);
        $('[name="address_street_app"]').attr("value", street);
        $('[name="address_num"]').attr("value", num_house);

    });
});

/* ================ loading information when pressing a button "NEXT"  ======  using in order_list ============= */

$(document.body).on( "click", "#paginator_next", function(e) {
    e.preventDefault();
    let $this=$(this);
    $.ajax({
        url: $this.attr('href'),
        type: "GET",
        dataType: "json",
        beforeSend: function () {},
        success: function(e){
            let type=JSON.parse(e);
            for (i = 0; i < type.length; i++) {
                $('#head').append(add_order_in_html_object(type[i]));
                $('#head').append('<div class="row"><div class="col-md-12"><hr></div></div>');
            }
            if (type.length==14) {
                $('#paginator_next').attr('href', '../listorderjson?last_pk='+type[13].pk+'&work_status=end');
                }
            else {
                $('#paginator_next').remove();
                }
        },
    });
});




