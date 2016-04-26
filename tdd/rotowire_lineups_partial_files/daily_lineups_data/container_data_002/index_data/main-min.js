var Banner = {

  init: function() {

    'use strict';

    // Set banner dimensions
    var adContent = document.getElementById("ad_content"),
			img1 = document.getElementById("img1"),
      adWidth = 728,
      adHeight = 90;

    function preIE10Check() {
      if (window.attachEvent && !window.navigator.msPointerEnabled) {
        console.log('IE 9 or below detected.');
        return true;
      } else {
        console.log('This browsers is not IE 9 or below. 001');
        return false;
      }
    }


    ////////////////////////////////////////////////////// ANIMATION //////////////////////////////////////////////////////

    function frameStart() {
      frame0();
    }

    // this is the first frame on your animation
    function frame0(){
      //
    }


    ////////////////////////////////////////////////////// EVENT HANDLERS //////////////////////////////////////////////////////

    function onAdClick(e) {
      window.open(window.clickTag);
    }

   function onAdHover(e) {
      // hover state
    }

    function onAdOut(e) {
      // normal state
    }

    function adClickThru() {
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

    adClickThru();
    frameStart();
  }
};

window.onload = function(){
  Banner.init();
};
