
/* ================   using in invoice for add information about works  ============= */
/* ================   using in invoice for add information about works  ============= */

function show_type_work(form) {
            $(form.nextElementSibling).fadeIn("slow", function(){
         });
}


$(document.body).on( "click", ".type_work", function(e) {
    e.preventDefault();
    let $this=$(this);
    $.ajax({
        url: $this.attr("href"),
        type: "GET",
        dataType: "json",
        success: function(b){
                    let type=JSON.parse(b);
                    let idname=$this.closest('div').find('select');
                    let nametype='#'+idname.attr('name')+'_type_work';

                    $(idname).empty();
                    for (i = 0; i < type.length; i++) {
                        $(idname).append('<option value='+type[i].id+'>'+type[i].name+'</option>');
                    }

                    idh=$(nametype);
                    idh.fadeOut("slow", function(){   });

        }
    });
});


/* ================   using in invoice  ============= */

function delete_field(id){
const element = document.getElementById(id);
element.parentNode.remove();
}

/* ================   using in invoice  ============= */

const addMoreBtn=document.getElementById('add-more');
const totalNewForms = document.getElementById('id_form-TOTAL_FORMS');
addMoreBtn.addEventListener('click', add_new_form);

const delete_empty=document.getElementsByClassName('delete-empty-form');

delete_empty[0].addEventListener('click', delete_field) ;


function add_new_form(event){
    if (event) {
    event.preventDefault();
    }
    const currentForms = document.getElementsByClassName('form');
    const currentFormCount = currentForms.length ;
    const formCopyTarget = document.getElementById('form-list');
    const copyEmptyFromEl=document.getElementById('empty-form').cloneNode(true);
    copyEmptyFromEl.setAttribute('class', 'form');
    copyEmptyFromEl.setAttribute('id',`form-${currentFormCount}`);
    copyEmptyFromEl.setAttribute('new',`new`);
    copyEmptyFromEl.getElementsByClassName('type_work')[0].setAttribute('id',`form-${currentFormCount}-service_id_type_work`);
    const regex = new RegExp('__prefix__', 'g');
    copyEmptyFromEl.innerHTML=copyEmptyFromEl.innerHTML.replace(regex,
    currentFormCount);
    totalNewForms.setAttribute('value', currentFormCount+1);
    const delete_empty=copyEmptyFromEl.getElementsByClassName('delete-empty-form')[0];
    delete_empty.setAttribute('id',`del_empty_field-${currentFormCount}`);
    delete_empty.addEventListener('click', function() { delete_field(id=`del_empty_field-${currentFormCount}`); } );
    formCopyTarget.append(copyEmptyFromEl);

}


/* ================   using in invoice  ============= */

$('#id_form').submit(function(e) {
    e.preventDefault();
    $.ajax({
        url: '',
        type: 'POST',
        data: $(this).serialize(),
        dataType: 'html',
        success: function (r) {
            let b=JSON.parse(r);
            if (b!=='error') {
                let c = $('div[new="new"]');
                for (i = 0; i < c.length; i++) {
                    let form_name = c[i]['id'];
                    let tr = $('tr.hidden').clone();
                    tr.find('td[name="service_id"]').html(b[i].service_id_name);
                    tr.find('td[name="quantity"]').html(b[i].quantity);
                    tr.find('td[name="price"]').html(b[i].price);
                    tr.find('td[name="amount"]').html(b[i].price*b[i].quantity);
                    tr.find('td[name="delete"]').html('<a href="../deleteinvoice/'+b[i].pk+'" class="link-delete" ><i class="fas fa-trash text-secondary"></i></a>');
                    tr.attr('class','form_text');
                    $('#total_').before(tr);
                    sum_total();
                }
                c.remove();
                $('#id_form-TOTAL_FORMS').attr("value", 0);
            }
            else {$('#error').html('<h4>Fill in all the fields</h4>');}
        },
    });

});


/* ================   END using in invoice  ============= */