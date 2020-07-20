var secs = 10;
var countdown = function(){
	setInterval(function(){
		$('#top').text("You will be redirected back to the main page in " + (--secs) + " seconds.");
	}, 1000);
	setTimeout(function (){
		window.location.href= './'
	},	10000);
};