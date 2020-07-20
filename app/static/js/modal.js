$(document).ready(function(){

	$('#drivers #add a').on('mouseup', function(e){
		$('#add-driver').show()
		$('#add-driver').addClass('active')
		console.log($('#add-driver'))
	})

	$('#equipment #add a').on('mouseup', function(e){
		$('#add-equipment').show()
		$('#add-equipment').addClass('active')
		console.log($('#add-equipment'))
	})

	$('body').on('mousedown', function(e) {
		if ($('.form-modal').hasClass('active') && e.target.id != 'form-modal' && !$(e.target).parents('.form-modal').length) {
			$('.form-modal').hide()
			$('#add-driver').removeClass('active')
			$('#add-equipment').removeClass('active')
			console.log('hidden')
		}
	})
})