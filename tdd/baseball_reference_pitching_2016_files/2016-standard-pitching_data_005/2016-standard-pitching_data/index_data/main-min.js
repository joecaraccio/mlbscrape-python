var Banner = {

  init: function() {

    'use strict';

    function getEl(elem) {
      return document.getElementById(elem);
    }

    // Set banner vars
    var adContent = getEl("ad_content"),
    f1_txt_1 = getEl('f1_txt_1'),
    f2_txt_2 = getEl('f2_txt_2'),
    f3_txt_1 = getEl('f3_txt_1'),
    f4_txt_2 = getEl('f4_txt_2'),
    ribbon_left = getEl('ribbon_left'),
    ribbon_right = getEl('ribbon_right'),
    cta = getEl('cta'),
    cta_up = getEl('cta_up'),
    cta_over = getEl('cta_over'),
    logo = getEl('logo'),
    ie_backup = getEl('ie_backup');

    ////////////////////////////////////////////////////// HELPERS //////////////////////////////////////////////////////

    // Check for IE 9 or earlier
    function preIE10Check() {
      if (window.attachEvent && !window.navigator.msPointerEnabled) {
        console.log('IE 9 or below detected.');
        ie_backup.style.display = "block";
        return true;
      } else {
        console.log('This browsers is not IE 9 or below. 001');
        return false;
      }
    }

    ////////////////////////////////////////////////////// ANIMATION //////////////////////////////////////////////////////

    function frameStart() {
      frame0();
      console.log("test");
    }

    // this is the first frame of your animation
    function frame0(){

      var tDelay=0;

      ribbon_left.style.visibility = "visible";
      ribbon_right.style.visibility = "visible";

      var tl = new TimelineMax();
       // Frame 1
       tl.from(f1_txt_1, .5, {autoAlpha:0}, tDelay+= 1)
       .from([ribbon_left, ribbon_right], 1, {y:"+=250", ease:Strong.easeOut}, tDelay+= .25)
       .from([scissor_light, scissor_dark], 1, {autoAlpha:0, x:"+=20", y:"+=20", ease:Strong.easeOut}, tDelay+= .5)

       .to(scissor_light, .5, {rotation:"-=15", x:"-=1", y:"+=2", ease:Strong.easeInOut}, tDelay+= 1)
       .to(scissor_dark, .5, {rotation:"+=18", x:"+=5", ease:Strong.easeInOut}, tDelay)

       .to(ribbon_left, 2, {x:"-190", y:"-=20", backgroundPosition:'100px 0px', ease:Strong.easeOut}, tDelay+= .25)
       .to(ribbon_right, 2, {x:"+190", y:"+=20", backgroundPosition:'-80px 0px', ease:Strong.easeOut}, tDelay)
       .to([scissor_light, scissor_dark], 1, {autoAlpha:0}, tDelay+= .5)

       // Frame 2
       .from(f2_txt_2, .5, {autoAlpha:0}, tDelay+= 1)

       // Frame 3
       .from(f3_txt_1, .5, {autoAlpha:0}, tDelay+= 1.5)

       // Frame 4
       .from(f4_txt_2, .5, {autoAlpha:0}, tDelay+= 1.5)
       .from(cta, 1, {autoAlpha:0}, tDelay+= 1)
       .from(logo, 1, {autoAlpha:0}, tDelay+= .5)

      TweenMax.delayedCall(tDelay,frameStop);

    }

    function frameStop() {
      adInteractionListeners();
    }

    ////////////////////////////////////////////////////// EVENT HANDLERS //////////////////////////////////////////////////////

    function onAdClick(e) {
      window.open(window.clickTag);
    }

    function onAdHover(e) {
      TweenMax.set(cta_up, {visibility:"hidden"});
      TweenMax.set(cta_over, {visibility:"visible"});
    }

    function onAdOut(e) {
       TweenMax.set(cta_up, {visibility:"visible"});
       TweenMax.set(cta_over, {visibility:"hidden"});
    }

    function adInteractionListeners() {
    	if (adContent.addEventListener) {
			adContent.addEventListener('click', onAdClick, false);
			adContent.addEventListener('mouseover', onAdHover, false);
			adContent.addEventListener('mouseout', onAdOut, false);
		} else {
			adContent.attachEvent('onclick', onAdClick, false);
			adContent.attachEvent('onmouseover', onAdHover, false);
			adContent.attachEvent('onmouseout', onAdOut, false);
		}
    }


    ////////////////////////////////////////////////////// INIT //////////////////////////////////////////////////////

    if(!preIE10Check())
    {
      adInteractionListeners();
      frameStart();
    }
  }
};

window.onload = function(){
  Banner.init();
};
