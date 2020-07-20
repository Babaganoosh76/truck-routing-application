function getVisible() {
    if (mobile)
        return;
    var $el = $('#contact'),
        scrollTop = $(window).scrollTop(),
        scrollBot = scrollTop + $(window).height(),
        elTop = $el.offset().top,
        elBottom = elTop + $el.outerHeight(),
        visibleTop = elTop < scrollTop ? scrollTop : elTop,
        visibleBottom = elBottom > scrollBot ? scrollBot : elBottom,
        visible = (visibleTop - visibleBottom)*(-1);
        visDif = window.innerHeight - $('#notSubhaul').height() - visible; //Distane between visible and contact
        visSub = window.innerHeight - $('#desktopNav').height() - visible; //Distane between subhaul and contact
    if (visDif<0)
        $("#notSubhaul").css({"top": + visDif + "px"});
    else
        $("#notSubhaul").css({"top": "0px"});

    if (visSub<0)
        $("#desktopNav #subhaul").css({"top": + visSub + "px"});
    else
        $("#desktopNav #subhaul").css({"top": "0px"});
}

function getVisibleCont(dur) {
    var bioTransition = setInterval(getVisible, 10);
    setTimeout(function(){
        clearInterval(bioTransition);
    }, dur);
}

var collapsed = true;
var mobile;

$(document).ready(function(){
    $(window).on('scroll', getVisible);

    $(window).on('load', function() {
        if ($(window).width() <= 767)
            mobile = true;
        else
            mobile = false;
    });

    $(window).on('resize', function() {
        // NOTE: 752 in JS = 767px in CSS and I don't know why!
        if (mobile && $(window).width() > 752)
            document.dispatchEvent(resizeToDesktop);
        if (!mobile && $(window).width() <= 752)
            document.dispatchEvent(resizeToMobile);
    });

    $(".navbarToggle").on('click', toggleNav);
});

function toggleNav () {
    if(collapsed)
        expandNav();
    else
        collapseNav();
}

function collapseNav () {
    $(".navbar").css({"height": "0px"});
    collapsed = true;
}

function expandNav () {
    $(".navbar").css({"height": "auto"});
    collapsed = false;
}

var resizeToMobile = new Event('resizeToMobile');
var resizeToDesktop = new Event('resizeToDesktop');

document.addEventListener('resizeToMobile', function(e) {
    collapseNav();
    mobile = true;
});

document.addEventListener('resizeToDesktop', function(e) {
    expandNav();
    mobile = false;
});


