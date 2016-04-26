
function shimmerIn(){
	TweenMax.to(ctaBtnOver, 0, {opacity:0, x:0, delay: 0});	
	TweenMax.to(ctaBtnOver, .3, {opacity:1, x:61, ease:Sine.easeIn, delay: 0});
	TweenMax.to(ctaBtnOver, .3, {opacity:0, x:122, ease:Sine.easeOut, delay: .3});
}

/////////////Animation

function startAd() {
    
    /*========================  CLICKTAG  =============================*/
    
    // var clickTag = "http://www.Goodyear.com/";
    // var adBtn = document.getElementById("ad");

    // function OPENW(){
    //     window.open(clickTag);
    // }

    // adBtn.addEventListener("click", OPENW, false);

    fnExitHandler = function(t) {
        if(t===1) {
            // Enabler.exit('clickTag1');
            window.open(clickTag,'_blank');
        } else if(t===2) {
            // Enabler.exit('clickTag2');
            window.open(clickTag1,'_blank');
        }
    };
    
    /*================================================================*/
    
    var adContainer = document.getElementById("container");

    TweenMax.defaultOverwrite = "false";
    document.getElementById("banner").style.visibility = "visible";

    animation1();
    // animation4();
	addOver();
}

function animation1(){
    setTimeout (function(){animation2()}, 3);
};

function animation2(){
    TweenMax.to(txt6Cont, 0, {left:-300});
    TweenMax.to(txt5, 0, {left:-300});
    TweenMax.to(txt7, 0, {left:-300});
	TweenMax.to(invisibleOver, 0, {opacity:0, ease:Quad.easeInOut, delay: 0});
    TweenMax.to(background, 0, {opacity:1,delay: 0});
    TweenMax.from(txt1, .5, {opacity:0, left:360, ease:Quad.easeOut, delay: .4});
    setTimeout (function(){animation3()}, 0);
};

function animation3(){
	TweenMax.to(terms, 1, {opacity:1, ease:Expo.easeInOut, delay: 3.1});
	TweenMax.to(background2, 1.2, {top:0, ease:Expo.easeInOut, delay: 2.1});
	TweenMax.to(cardContainer, 1.5, {top:414, ease:Expo.easeInOut, delay: 2.1});    
	TweenMax.to(txt2, 1, {opacity:0.9,left:11, ease:Expo.easeInOut, delay: 3.1});
    TweenMax.to(txt3, 1, {top:0, ease:Expo.easeInOut, delay: 4.1, onComplete: animation4});
};

function animation4(){
    TweenMax.to(terms, 0.4, {opacity:0, ease:Expo.easeInOut, delay: 2});
    
    TweenMax.to(terms, 0, {top:436, ease:Expo.easeInOut, delay: 2.3});

    TweenMax.to(rates, 1.0, {opacity:1, ease:Expo.easeInOut, delay: 2.1, onComplete: switchZIndex});
    TweenMax.to(ctaContainer, 1.1, {opacity:1, ease:Expo.easeOut, delay: 0.6});
    TweenMax.to(terms, 1.1, {opacity:1, ease:Expo.easeOut, delay: 2.9});

    TweenMax.to(logo, 0.6, {opacity:1, ease:Expo.easeOut, delay: 2.9});

    TweenMax.to(cardContainer, 1.5, {top:310, ease:Expo.easeInOut, delay: 2.1});
    TweenMax.to(cardShine, 0, {left:-100, delay: 1.2});
    TweenMax.to(cardShine, 1.5, {left:125, ease:Expo.easeOut, delay: 3});

    TweenMax.to(txt2Comma, 1.5, {opacity:0, ease:Expo.easeInOut, delay: 1.2});
    TweenMax.to(txt3, 1.5, {opacity:0, ease:Expo.easeInOut, delay: 1.2});
    TweenMax.to(txt6Cont, 1, {left:18, ease:Expo.easeInOut, delay: 2.7});
    TweenMax.to(txt5, 1, {left:0, ease:Expo.easeInOut, delay: 2.7});
    TweenMax.to(txt7, 1, {left:7, ease:Expo.easeInOut, delay: 2.7});
    TweenMax.from(txt5, 1, {top:120, ease:Expo.easeInOut, delay: 3.2});
    TweenMax.from(txt7, 1, {top:-50, ease:Expo.easeInOut, delay: 3.2, onComplete: bgOnOver});
};

function addOver(){
    invisibleOver.addEventListener('mouseenter', bgOnOver, false);
};

bgOnOver = function(e)
{
    TweenMax.to(ctaBtnOver, 0, {css: {left:-130}, ease:Expo.easeOut, delay: 0});
    TweenMax.to(ctaBtnOver, 1.7, {css: {left:130}, ease:Expo.easeOut, delay: .1});
};

function switchZIndex(){
    TweenMax.to(rates, .1, {zIndex:6});
}