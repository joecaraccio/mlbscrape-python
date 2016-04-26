
 /////////////Animation

function startAd() {
//

    var screen = document.getElementById('screen');

    //Set positions and attributes
        TweenLite.set(txt1, {opacity:0, left:320});
        TweenLite.set(txt2, {opacity:0,left:323});
        TweenLite.set([txt3,logo,txtBottom,arrow],{opacity:0});
        TweenLite.set([circle1,circle2,circle3],{opacity:0,scale:0});

		TweenLite.set([image01,image02,image03,image04,image05,image06], {opacity:0, scale:0});

  
        TweenLite.set(imag, {opacity:0, scale:0.34});
        
        
      //END Set positions and attributes

    var adContainer = document.getElementById("container");
    
   

    TweenMax.defaultOverwrite = "false";
    document.getElementById("banner").style.visibility = "visible";

    init();
   
  
}



function init(){
    setTimeout (function(){animation1()}, 100);
};

function animation1(){
	
	//Speed animation if you wants change to slow-fast.

	
	var count=.08;// starting
	var scales = 1.1;
	var easing = Power0.easeNone;
	
	TweenLite.to(image01, count, {opacity:1,scale:scales,ease:easing,delay:0});
	TweenLite.to(image01, count, {scale:1, ease:Power1.easeOut,delay:.1});
	
	TweenLite.to(image03, count, {opacity:1,scale:scales, ease:easing,delay:.2});
	TweenLite.to(image03, count, {scale:1, ease:Power1.easeOut,delay:.3});
	
	TweenLite.to(image05, count, {opacity:1,scale:scales, ease:easing,delay:.7});
	TweenLite.to(image05, count, {scale:1, ease:Power1.easeOut,delay:.8});
	
	TweenLite.to(image02, count, {opacity:1,scale:scales, ease:easing,delay:.8});
	TweenLite.to(image02, count, {scale:1, ease:Power1.easeOut,delay:.9});
	
	TweenLite.to(image04, count, {opacity:1,scale:scales, ease:easing,delay:1});
	TweenLite.to(image04, count, {scale:1, ease:Power1.easeOut,delay:1.1});
	
	TweenLite.to(image06, count, {opacity:1,scale:scales, ease:easing,delay:1});
	TweenLite.to(image06, count, {scale:1, ease:Power1.easeOut,delay:1.1});
	

	TweenLite.to(txt1, .2, {delay:1.3, opacity:1, left:-53, ease:easing});
	TweenLite.delayedCall(2.3, animation2);
};

function animation2(){
	
	var easing = Power1.easeOut;
	TweenLite.to(txt1, .2, {delay:2, opacity:0, left:22, ease:easing});
	TweenMax.to(imag, .5, {delay:2,left:0,top:0, opacity:1, scaleX:1, scaleY:1, ease:easing});
    TweenMax.to(txt2, .2, {delay:2.3, opacity:1, left:15, ease:easing});
	TweenMax.to([image01,image02,image03,image04,image05,image06], .2, {delay:2.6, opacity:0,ease:easing});
	TweenMax.to([bottom,logo,txtBottom,arrow], .2, {delay:2.5, opacity:1,ease:easing});
    TweenLite.delayedCall(3, animation3);
}

function animation3(){
	var easing = Power1.easeOut;
    TweenMax.to(txt2, .2, {delay:2, opacity:0, ease:easing});
	TweenMax.to(imag, .2, {delay:2, opacity:0,ease:easing});
    
	TweenMax.to(txt3, .2, {delay:2, opacity:1,left:14});
    TweenMax.to(tv, .2, {delay:2.3,left:6});
	TweenMax.to(phone, .2, {delay:2.6,left:129});
    TweenMax.to(circle1, .4, {delay:2.7, opacity:1, scale:1});
    TweenMax.to(circle2, .4, {delay:2.8, opacity:1,  scale:1,repeat: 3 , yoyo:true,repeatDelay:0.2});
    TweenMax.to(circle3, .4, {delay:2.9, opacity:1,  scale:1,repeat: 3 , yoyo:true,repeatDelay:0.2});
    TweenLite.delayedCall(3, animation4);
}

function animation4(){
	var easing = Power1.easeOut;
    TweenMax.to([txt3,tv,phone,circle1], .2, {delay:2, opacity:0,ease:easing});
	TweenMax.to(txt4, .2, {delay:2.3,left:9, ease:easing});
	TweenMax.to(icon, .2, {delay:2.6,left:36, ease:easing});
	
    TweenLite.delayedCall(3, animation5);   
    TweenMax.to(txt5, .2, {delay:2, opacity:1, x:0, ease:easing});
}
function animation5(){
	var easing = Power1.easeOut;
	TweenMax.to([txt4,icon], .2, {delay:2,opacity:0,ease:easing});
	TweenMax.to(txtBottom, .2, {delay:2,top:7,ease:easing});
    TweenMax.to(arrow, .2, {delay:2,top:10,ease:easing});
	TweenMax.to(bottom, .2, {delay:2,opacity:1,ease:easing});
	TweenMax.to(ctaText, .2, {delay:2.2,top:25,ease:easing,onComplete: hoverUnit});
	
	TweenMax.to(txt5, .2, {delay:2.2,left:9, ease:easing});
	TweenMax.to(txt6, .2, {delay:2.4,left:15, ease:easing});
	TweenMax.to([line1, line2], .25, {delay: 2.4,width: 120,ease:easing});
	TweenMax.to(txt7, .2, {delay:2.4,left:19, ease:easing});
	TweenMax.to(txt8, .2, {delay:2.8,opacity:1, ease:easing});
    // TweenMax.to(phoneNumber, .25, {opacity: 1, delay: 3, ease:easing});
	
	

    TweenMax.delayedCall(5, bindEvents);
}

var bindEvents = function() {
		var ad = document.getElementById('ad');

		ad.addEventListener('mouseenter', hoverUnit);
	}





var hoverUnit = function(event) {
		var mouseEffect = TweenMax.fromTo(bottom, 1, {backgroundPosition:"-350px 0"},{backgroundPosition:"450px 0",paused:true});
		mouseEffect.restart();
	}	
	
	