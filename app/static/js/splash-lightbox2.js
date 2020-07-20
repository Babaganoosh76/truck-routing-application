var $currentDiv;

$(document).on('click','.image',function() {
    $currentDiv = this;
    showImg();
});

function closeModal() {
	$('#myModal').hide();
}

function showImg(){
	var source = $($currentDiv).children('img').attr('src');
	$('#myModal').find('.mySlides').children().attr('src', source);
	$('#myModal').show();
}