var slideIndex = 1;
var $currentDiv;
var cur, tot;

$(document).on('click','.image',function() {
    $currentDiv = this;
    showImg();
});

function openModal(d) {
	var divs = d.children;
	for (var i = 0; i < divs.length; i++) {
		if(divs[i].className == 'item active') {
			$currentDiv = divs[i];
			cur = i+1;
			tot = divs.length;
		}
	}
	showImg();
}

function closeModal() {
	$('#myModal').hide();
}

function plusSlides(n){
	if(n<0){
		if($($currentDiv).prev().length == 0){
			$currentDiv = $($currentDiv).parent().find('.item').last();
			cur = tot;
		}
		else{
			$currentDiv = $($currentDiv).prev();
			cur--;
		}
	} else {
		if($($currentDiv).next().length == 0){
			$currentDiv = $($currentDiv).parent().find('.item').first();
			cur = 1;
		}
		else{
			$currentDiv = $($currentDiv).next();
			cur++;
		}
	}
	showImg();
}

function showImg(){
	var source = $($currentDiv).children('img').attr('src');
	$('#myModal').find('.mySlides').children().attr('src', source);
	$('#myModal').find('.numberText').text(cur + ' / ' + tot);
	$('#myModal').show();
}