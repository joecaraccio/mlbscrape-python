// Variables
var clicktagArea = document.getElementById("clicktag"),
	shiner	= document.getElementById("shiner");

clicktagArea.addEventListener( 'mouseenter', moveShine, false);

// Functions

function startAd() {

	fnExitHandler = function(t) {
		// Enabler.exit('clickTag1');
		window.open(clickTag,'_blank');
	};

	initAnimations();
}

function initAnimations(){
	var timelineAnimation = new TimelineMax();
	timelineAnimation
	.to("#initial-blue", 0.2, {left:161, ease:Power2.easeOut, delay:1.5})
	.to("#second-blue", 0.3, {left:0, ease:Power4.easeOut})
	.to("#second-text", 0.8, {top:161, opacity: 1, ease:Power4.easeOut})
	.to("#card", 0.8, {top:525, ease:Power4.easeOut}, "-=0.8")
	.to("#second-text", 0.5, {opacity:0, ease:Power4.easeOut, delay:1.5})

	.to("#third-text", 0.8, {opacity: 1, ease:Power4.easeOut})
	.to("#third-text", 0.8, {opacity: 0, ease:Power4.easeOut, delay:3})

	.to("#earn-title", 0.5, {top:160, left:23, ease:Power4.easeOut, onComplete: function(){
		changeNumbersToSix();
	}})
	.to("#numbers", 0.5, {top:250, ease:Power4.easeOut}, "-=0.4")
	.to("#category1", 0.5, {left:26, ease:Power4.easeOut}, "-=0.4")
	.to("#terms", 0.8, {opacity:1, ease:Power4.easeOut})
	.to("#numbers", 0.5, {top:600, ease:Power4.easeOut, delay:1.5})
	.to("#category1", 0.4, {opacity:0, ease:Power4.easeOut, onComplete: function(){
		resetNumber();
		setTimeout(function(){
			changeNumbersToThree();
		}, 500);
	}}, "-=0.8")
	.to("#numbers", 0.5, {top:250, ease:Power4.easeOut})
	.to("#category2", 0.8, {left:26, ease:Power4.easeOut}, "-=0.4")
	.to("#numbers", 0.5, {top:600, ease:Power4.easeOut, delay:1.8})
	.to("#category2", 0.5, {opacity:0, ease:Power4.easeOut, onComplete: function(){
		resetNumber();
		setTimeout(function(){
			changeNumberOne();
		}, 150);
	}}, "-=0.4")
	.to("#numbers", 0.5, {top:250, ease:Power4.easeOut})
	.to("#category3", 0.5, {left:21, ease:Power4.easeOut}, "-=0.4")
	.to("#terms", 0.8, {opacity:0, ease:Power4.easeOut, delay:1.5})
	.to("#earn-title", 0.5, {opacity:0, ease:Power4.easeOut}, "-=0.6")
	.to("#numbers", 0.5, {left:302, opacity:0, ease:Power4.easeOut})
	.to("#category3", 0.5, {left:302, opacity:0, ease:Power4.easeOut}, "-=0.4")
	// .to("#second-blue", 0.5, {width:33, ease:Power4.easeOut}, "-=0.4")
	.to("#card", 0.5, {scale:0.75, top:65, left: -11, ease:Power4.easeOut}, "-=0.2")
	.to("#logo", 0.5, {opacity: 1, ease:Power4.easeOut}, "-=0.5")
	.to("#cta", 0.5, {display: "block"}, "-=0.5")
	.to("#button", 0.5, {opacity: 1, ease:Power4.easeOut}, "-=0.5")
	.to("#ff-terms", 0.5, {opacity: 1, ease:Power4.easeOut}, "-=0.5")
	.to("#ff-title", 0.5, {left: 23, ease:Power4.easeOut}, "-=0.5")
	.to("#ff-cashback", 0.5, {left: 23, ease:Power4.easeOut, onComplete: function(){
		moveShine();
	}}, "-=0.5");
}

function moveShine(){
	TweenLite.set(shiner, { x:-50 });
	TweenLite.to(shiner, 0.6, { x:160, ease:Linear.easeNone });
}

function changeNumbersToSix(){
	var number = 0;
	var six = setInterval(function(){
		if(number<7){
			document.getElementById("number").innerHTML = number++;
		}else{
			clearInterval(six);
		}
	},200);
}

function changeNumbersToThree(){
	var number = 0;
	var three = setInterval(function(){
		if(number<4){
			document.getElementById("number").innerHTML = number++;
		}else{
			clearInterval(three);
		}
	},200);
}

function changeNumberOne(){
	var number = 0;
	var one = setInterval(function(){
		if(number<2){
			document.getElementById("number").innerHTML = number++;
		}else{
			clearInterval(one);
		}
	},200);
}

function resetNumber(){
	document.getElementById("number").innerHTML = "0";
}