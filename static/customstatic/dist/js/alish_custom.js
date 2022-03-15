
// document.getElementById('su-password').addEventListener('keypress', function (e) {
//     if (e.which == 13){
//     	e.preventDefault()
//     } else {
//     	setTimeout(function() {
// 	    	var pword = document.getElementById('su-password').value
// 	    	var c_pword = document.getElementById('su-password-confirm').value
// 	    	console.log(pword)
// 	    	console.log(c_pword)
// 			var btn = document.getElementById('register_customer_button')
// 	    	if (pword != c_pword){
// 	    		btn.disabled = true;
// 	    	} else if (pword == c_pword){
// 	    		btn.disabled = false;	
// 	    	}
//     	}, 500)
//     }
//     var val = document.getElementById('su-password')
// }, false);


// Add to cart
// alert('hh')
$('body').on('click', '.add-to-cart', function(e) {
	e.preventDefault();
    var quantity = $('.quantity_input').val()
	if (quantity < 1){
		$('.quantity_input').val(1)
		$('.quantity_input').select()
		toastr.options.closeButton = true;
        toastr.options.positionClass = 'toast-top-right';
        toastr.options.timeOut = 2000;
        toastr.options.extendedTimeOut = 100;
        toastr['error'](`please enter quantity`, 'Error');
	} 
	else {
		$.ajax({
			url: $(this).data('url'),
			data: {
				quantity,
			},
			success: function(data) {
				// alert(data.message)
				if (data.message == "success"){
					$('#navbar_cart_container').load(' #navbar_cart_container')
					$('#mobile_screen_footermenu').load(' #mobile_screen_footermenu')
					toastr.options.closeButton = true;
			        toastr.options.positionClass = 'toast-top-right';
			        toastr.options.timeOut = 2000;
			        toastr.options.extendedTimeOut = 100;
			        toastr['success'](`${data.addedproduct} added to the cart`, 'Success');
			        $('#process').hide();
					// alert('success')

				}
				else if(data.message == "cart-full"){
					Swal.fire({
						icon: 'warning',
						title: 'Oops...',
						text: 'Your Cart is Full',
					  })				
					$('#process').hide();
				}
				else {
					toastr.options.closeButton = true;
			        toastr.options.positionClass = 'toast-top-right';
			        toastr.options.timeOut = 2000;
			        toastr.options.extendedTimeOut = 100;
			        toastr['error']('Failed to add products', 'Error');
			        $('#process').hide();
				}
			}
		})
	}
});

$('body').on('click', '.remove-cart-product', function(e){
	var id = $(this).data('id')
	$.ajax({
		url: $(this).data('href'),
		data:{
			id, 'action': 'rmv'
		},
		success: function(data) {
			if (data.message == "success"){
				$('#navbar_cart_container').load(' #navbar_cart_container')
				$('#cart_table_section').load(' #cart_table_section')
				$('#client_cart_sideaside').load(' #client_cart_sideaside')
				$('#checkout_sideaside').load(' #checkout_sideaside')
				$('#checkout_review_load_products').load(' #checkout_review_load_products')
				$('#mobile_screen_footermenu').load(' #mobile_screen_footermenu')
				
				toastr.options.closeButton = true;
				toastr.options.positionClass = 'toast-top-right';
				toastr.options.timeOut = 2000;
				toastr.options.extendedTimeOut = 100;
				toastr['success']('Cart Product Removed successfully', 'Success');
				$('#process').hide();
				// location.reload()
			} else {
				alert('error')
				$('#process').hide();
			}
		}
	})
})

// $('#quantity_input').on('keyup', function(e){
// 	if (e.which == 13){
// 		e.preventDefault()
// 	} else {
// 		var val = $('#quantity_input').val()
// 		if (val < 1){
// 			$('#quantity_input').val(1)
// 			$('#quantity_input').select()
// 		} else if (val > 10){
// 			$('#quantity_input').val(10)
// 		}
// 	}
// })

$('body').on('keyup', '.quantity_input', function(e){
	if (e.which == 13){
		e.preventDefault()
	} else {
		var $this = $(this)
		var val = $(this).val()
		quantityInputChange(val, $this)
	}
})

function quantityInputChange(val, $this) {
	if (val <= 1){
		$($this).val(1)
		$($this).select()
	} else if (val > 10){
		$($this).val(10)
	}
}

// $('body').on('click', '.quick_view', function(e){
// 	e.preventDefault();
// 	var href = $(this).data('href') 
// 	$.ajax({
// 		url: href,
// 		success: function(data){
// 			$('#quick-view').html(data)
// 			$('#quick-view').modal('show');
// 		}
// 	})
// })