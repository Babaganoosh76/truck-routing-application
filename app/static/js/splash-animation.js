$(document).ready(function(){
	var position = $('#glyphicon-truck').offset().left;
	var width = $(window).width();
	

	var offscreenTruck = width - $('#glyphicon-truck').offset().left,
		offscreenTrailer = width - $('#glyphicon-trailer').offset().left,
		offscreenForklift = width - $('#glyphicon-forklift').offset().left;

	var widthForklift = $('#glyphicon-forklift').children().width();
		heightForklift = $('#glyphicon-forklift').children().height();

	var smol = 0.75;
	console.log(widthForklift, heightForklift);

	// Remove from screen
	$('#glyphicon-truck').animate({
		left: (offscreenTruck-52)
	}, 1, function(){
	});
	$('#glyphicon-trailer').animate({
		left: offscreenTrailer
	}, 1, function(){
	});
	$('#glyphicon-forklift').animate({
		top: "5px",
		left: (offscreenForklift+108)
	}, 1, function(){
	});
	$('#glyphicon-forklift').children().animate({
		width: (smol*widthForklift),
		height: (smol*heightForklift)
	}, 1, function(){
	});

	// $('.bubble').addClass('trailerScale');
	// Reposition
	// $('#glyphicon-truck').animate({
	// 	left: offscreenTruck-50,
	// }, 1000, function(){
	// });
	// $('#glyphicon-trailer').animate({
	// 	left: 0,
	// }, 1000, function(){
	// });
	// $('#glyphicon-forklift').animate({
	// 	left: offscreenForklift+50,
	// }, 1000, function(){
	// });

	// Drive onscreen
	$('#glyphicon-truck').animate({
		left: "-=500"
	}, 1000, function(){
	});
	$('#glyphicon-trailer').animate({
		left: "-=500"
	}, 1000, function(){
	});
	$('#glyphicon-forklift').animate({
		top: "5px",
		left: "-=500",
	}, 1000, function(){
	});
	$('#glyphicon-forklift').children().animate({
		width: (smol*widthForklift),
		height: (smol*heightForklift)
	}, 1000, function(){
	});



	// Put back into default positions
	$('#glyphicon-truck').animate({
		left: 0
	}, 1000, function(){
	});
	$('#glyphicon-trailer').animate({
		left: 0
	}, 1000, function(){
	});
	$('#glyphicon-forklift').animate({
		top: 0,
		left: 0,
	}, 1000, function(){
	});
	$('#glyphicon-forklift').children().animate({
		width: (widthForklift),
		height: (heightForklift)
	}, 1000, function(){
	});

	// $('#glyphicon-forklift').children().animate({
	// 	width: "100"
	// }, 1000, function(){
	// });

	console.log(widthForklift);
	console.log()
});
