var rot;

// SPIN
$(window).scroll( function(){
	rot = $(window).scrollTop()/10;
	$('.sunburst').css({"transform": "rotate("+rot+"deg)"});
});

// LOAD
$(window).on("load", function(){
	$('.sunburst').attr("src", "static/img/sunburst.png");
});

// RESIZE
$(window).on("load resize", function(){
	if ($(window).width() >= 752)
		$('#desktopNav .spinner').css({"height": $('#desktopNav .spinner').width()/2 +"px"});
	else
		$('#desktopNav .spinner').css({"height": "50px"});
});