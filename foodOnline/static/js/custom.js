// let autocomplete;

// function initAutoComplete(){
//   autocomplete = new google.maps.places.Autocomplete(
//     document.getElementById('id_address'),
//     {
//       types:['geocode', 'establishment'],
//       componentRestrictions:{'country':['uzb']},
//     }
//   )
//   autocomplete.addListener('place_changed',onPlaceChanged);
// }

// function onPlaceChanged(){
//   var place =autocomplete.getPlace();

//   if (!place.geometry){
//     document.getElementById('id_address').placeholder="start typing...";

//   }else{
//     console.log('place name=>',place.name);
//   }

//   var geocoder =new google.maps.Geocoder()
//   var address =document.getElementById('id_address').value

//   geocoder.geocode({'address':addresss}, function(results, status){
//     // console.log('results=>',results);
//     // console.log('status=>',status);

//     if (status == google.maps.GeocoderStatus.OK){
//       var latitude = results[0].geometry.location.lat();
//       var longitude = results[0].geometry.location.lng();
//       $('#id_latitude').val(latitude);
//       $('#id_longitude').val(longitude);
      
//       $('#id_address').val(address);


//     }
//   });

//   for(var i=0; i<place.address_components.length; i++){
//     for(var j=0; j<place.address_components[i].types.length; j++){
//       // get country
//       if (place.address_components[i].types[j] == 'country'){
//         $('#id_country').val(place.address_components[i].long_name);
//       }
//       // get state
//       if (place.address_components[i].types[j] == 'adminstrative_area_level_1'){
//         $('#id_state').val(place.address_components[i].long_name);
//       }
//       // get city
//       if (place.address_components[i].types[j] == 'locality'){
//         $('#id_city').val(place.address_components[i].long_name);
//       }
//       //get pincode
//       if (place.address_components[i].types[j] == 'postal_code'){
//         $('#id_pin_code').val(place.address_components[i].long_name);
//       }else{
//         $('#id_pin_code').val("");
//       }
//     }
//   }
// }


$(document).ready(function(){
 

//     // $('#add_to_cart').on('click',function (e) {
//     //   e.preventDefault();
//     //   food_id = $(this).attr('data-id');
//     //   url=$(this).attr('data-url');
//     //   // console.log(url);
//     //   data ={
//     //     food_id:food_id,
        
//     //     }
        
//   //   $.ajax({
//   //     type:'GET',
//   //     url:url,
//   //     data:data,
//   //     success:function(response){
//   //     alert(response);        
//   //     }
//   //     })
//   // });


//    function my_function(elem){
//     food_id = $(this).attr('data-id');
//       url=$(this).attr('data-url');
//       alert(food_id)
// // console.log(food_id);
//    }
  
$('.item_qty').each(function(){
  var the_id =$(this).attr('id');
  var qty =$(this).attr('data-qty');
  $('#'+the_id).html(qty);
  // console.log(the_id);
});
$('#myOrder').DataTable();
});

function add_to_cart(elem){
    food_id = $(elem).attr('data-id');
    url=$(elem).attr('data-url');
      $.ajax({
      type:'GET',
      url:url,
      success:function(response){
        // console.log(response);
        if(response.status =='login_required'){
          swal(response.message,'','info').then(function(){
            window.location ='/accounts/login';
          });
        }else if(response.status =='Failed'){
          swal(response.message,'','error');
        }
        else{
          console.log(response);
          $('#cart_counter').html(response.cart_counter['cart_count']);
          $('#qty-'+food_id).html(response.qty);

          applyCartAmounts(
            response.cart_amount['subtotal'],
            response.cart_amount['tax_dict'],
            response.cart_amount['grand_total']
            );

        }
      // alert(response);        
      }
      })
    
 }
function decrease_from_cart(elem){
    food_id = $(elem).attr('data-id');
    url=$(elem).attr('data-url');
    cart_id = $(elem).attr('id');
      $.ajax({
      type:'GET',
      url:url,
      success:function(response){
        // console.log(response);
        if(response.status =='login_required'){
          swal(response.message,'','info').then(function(){
            window.location ='/accounts/login';
          });
          }else if(response.status =='Failed'){
            swal(response.message,'','error');
          }else{
          
          $('#cart_counter').html(response.cart_counter['cart_count']);
          $('#qty-'+food_id).html(response.qty);

          applyCartAmounts(
            response.cart_amount['subtotal'],
            response.cart_amount['tax_dict'],
            response.cart_amount['grand_total']
            );

          if(window.location.pathname == '/cart/'){
            removeCartItem(response.qty,cart_id);
            checkEmptyCart();
          }

        }
      // alert(response);        
      }
      })
    
 }

function delete_cart(elem){
    cart_id = $(elem).attr('data-id');
    url=$(elem).attr('data-url');
      $.ajax({
      type:'GET',
      url:url,
      success:function(response){
          if(response.status =='Failed'){
            swal(response.message,'','error');
          }else{
          $('#cart_counter').html(response.cart_counter['cart_count']);
          swal(response.status,response.message,'success');

          applyCartAmounts(
            response.cart_amount['subtotal'],
            response.cart_amount['tax_dict'],
            response.cart_amount['grand_total']
            );
          removeCartItem(0,cart_id);
          checkEmptyCart();
        }        
      }
      })
    
 }
function removeCartItem(cartItemQty,cart_id){

    if( cartItemQty <= 0){
      document.getElementById("cart-item-"+cart_id).remove();
    }
  
}

function checkEmptyCart(){
  var cart_counter =document.getElementById('cart_counter').innerHTML;
  if (cart_counter == 0){
    document.getElementById('empty-cart').style.display='block';
  }
}

function applyCartAmounts(subtotal,tax_dict,grant_total){
  if( window.location.pathname == '/cart/'){
    $('#subtotal').html(subtotal);
    $('#total').html(grant_total);

    for(key1 in tax_dict){
      for(key2 in tax_dict[key1]){
        $('#tax-'+key1).html(tax_dict[key1][key2])
      }
    }
  }

}





$('.add_hour').on('click',function(e){
  e.preventDefault();
  var day =document.getElementById('id_day').value;
  var from_hour =document.getElementById('id_from_hour').value;
  var to_hour =document.getElementById('id_to_hour').value;
  var is_closed =document.getElementById('id_is_closed').checked;
  // var csrftoken =document.getElementsByName('csrfmiddlewaretoken').value;
  var csrftoken =$('input[name=csrfmiddlewaretoken]').val();
  var url =document.getElementById('add_hour_url').value;

  if(is_closed){
    is_closed='True'
    condition ='day !=""'
  }else{
    is_closed='False'
    condition="day != '' && from_hour != '' && to_hour != '' "
  }
  // console.log(csrftoken);
  if(eval(condition)){
    $.ajax({
      type:"POST",
      url:url,
      data:{
        'day':day,
        'from_hour':from_hour,
        'to_hour':to_hour,
        'is_closed':is_closed,
        'csrfmiddlewaretoken':csrftoken
      },
      success:function(response){
        console.log(response);
        if (response.status == 'success'){
            if(response.is_closed =='Closed'){
              html ='<tr><td >Closed</td><td><a href="#">Remove</a></td></tr>'
            }else{
              html ='<tr><td >'+response.day+'</td><td>'+response.from_hour+'-'+response.to_hour+'</td><td><a href="#">Remove</a></td></tr>'
            }
            $('.opening_hours').append(html);
            document.getElementById("opening_hours").reset();
        }else{
          swal(response.message,'','error');
        }
      }
    });
  }else{
    swal('Please fill all fields!','','info')
  }

});