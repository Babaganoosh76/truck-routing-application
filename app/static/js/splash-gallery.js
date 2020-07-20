$(document).ready(function() {
  var i = 0, delay = 50
  $.get('/get-gallery',function(data){
  	var populate = setInterval(function(){
  		var col = shortest()
  		addDiv(col, (i+1), data[i++])
  	}, delay)

  	setTimeout(function() {
  		clearInterval(populate)
  	}, (delay*data.length))
  })
  

  console.log(images)

  // var populate = setInterval(function(){
  // 	var col = shortest()
  // 	addDiv(col, (i+1), images[i++])
  // }, delay)

  // setTimeout(function() {
  // 	clearInterval(populate)
  // }, (delay*images.length))
})




function addDiv(col, id, img) {
	// $(col).append('<div id="div' + id + '" class="image"><img src="' + img + '"><div class="overlay"><div class="text">Text</div></div></div>');
	$(col).append('<div id="div' + id + '" class="image"><img src="' + img + '"></div>');
	$('#div'+id).css({'animation-delay':findDelay(id)+'ms'});
}

function findDelay(id){
	var speed = 80;
	return id*speed;
}

function shortest() {
	var short = $('#col1');
	if($('#col2').height() < short.height()){
		short = $('#col2');
	}
	if($('#col3').height() < short.height()){
		short = $('#col3');
	}
	return short;
}