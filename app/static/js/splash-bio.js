
function showBio(a, p) {
	if($(p).hasClass('active')){
		$(p).slideUp();
		$(p).removeClass('active');
		$(a).text("Read my bio.");
	} else {
		closeActive(p);
		$(p).slideDown();
		$(p).addClass('active');
		$(a).text("Close");
	}
	getVisibleCont(500);
}

function closeActive(p) {
	var array = $('.bio div').toArray();
	for(var i = 0; i < array.length; i++){
		$(array[i]).slideUp();
		$(array[i]).removeClass('active');
	}
	$('#team .bottomLink a').text("Read my bio.");
}