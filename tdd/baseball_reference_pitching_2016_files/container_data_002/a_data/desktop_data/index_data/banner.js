window.onload = function() {
	
	var _settings = init({w: 728, h: 90});
	var _container = _settings.container;
	var _plays = 0;
	var _maxPlays = 3;

	createElement("img", {attr:{class:"background728", src:''}, css:{x:-182, y:-22, transformOrigin:'100% 100%', scale:.8}}, _container);

	var _footer = createElement("div", {attr:{class:"footer"}, css:{y:33, width:728, height:180}}, _container);
	createElement("img", {attr:{class:"angle", src:"assets/bg_angle.svg"}, css:{x:0, y:0}}, _footer);
	createElement("div", {attr:{class:"blueBg"}, css:{x:0, y:90, width:728, height:90}, bg:"#005983"}, _footer);

	var _line2Mask = createElement("div", {attr:{class:"line2Mask"}, css:{x:459, y:-2, width:33, height:44, overflow:'hidden'}}, _container);
	createElement("img", {attr:{class:"line2", src:"assets/line2.svg"}, css:{x:33, y:44}}, _line2Mask);

	var _lineMask = createElement("div", {attr:{class:"lineMask"}, css:{x:295, y:22, width:524, height:68, rotation:0, overflow:'hidden'}}, _container);
	createElement("img", {attr:{class:"line", src:"assets/lineDot.svg"}}, _lineMask);

	createElement("img", {attr:{class:"logo728", src:""}, css:{x:579, y:65}}, _container);
	var _cta = createElement("img", {attr:{class:"cta", src:'assets/cta.png'}, css:{x:971, y:25}}, _container);
	
	var _shineMask = createElement("div", {attr:{class:"shineMask"}, css:{x:269, y:25, width:110, height:33, overflow:'hidden'}}, _container);
	createElement("div", {attr:{class:"shine"}, css:{x:-50, y:-10, width:30, height:60, rotation:30, backgroundRepeat:'repeat-y'}, bg:'assets/shine.png'}, _shineMask);

	createElement("img", {attr:{class:"acela728", src:''}, css:{x:1231, y:58,}}, _container);

	createElement("div", {attr:{class:"lead1_1"}, css:{
		x:20, y:20, alpha:0, color:'#fff', fontFamily:'Hind Siliguri', fontSize:25, fontWeight:400, lineHeight:'25px'
	}, text:''}, _container);
	createElement("div", {attr:{class:"leadlegal_1"}, css:{
		x:20, y:70, alpha:0, color:'#fff', fontFamily:'Hind Siliguri', fontSize:8, fontWeight:400, lineHeight:'8px', letterSpacing:'-0.53px', autoRound:false
	}, text:''}, _container);
	
	createElement("div", {attr:{class:"lead2_1"}, css:{
		x:20, y:20, alpha:0, color:'#fff', fontFamily:'Hind Siliguri', fontSize:25, fontWeight:400, lineHeight:'25px'
	}, text:''}, _container);
	createElement("div", {attr:{class:"leadlegal_2"}, css:{
		x:20, y:70, alpha:0, color:'#fff', fontFamily:'Hind Siliguri', fontSize:8, fontWeight:400, lineHeight:'8px', letterSpacing:'-0.53px', autoRound:false
	}, text:''}, _container);

	createElement("div", {attr:{class:"lead3_1"}, css:{
		x:738, y:20, color:'#fff', fontFamily:'Hind Siliguri', fontSize:20, fontWeight:400, lineHeight:'26px'
	}, text:''}, _container);
	createElement("div", {attr:{class:"leadlegal_3"}, css:{
		x:738, y:70, color:'#fff', fontFamily:'Hind Siliguri', fontSize:8, fontWeight:400, lineHeight:'8px', letterSpacing:'-0.53px', autoRound:false
	}, text:''}, _container);

	createElement("div", {attr:{class:"seeWhere"}, css:{
		x:1242, y:35, color:'#fff', fontFamily:'Hind Siliguri', fontSize:12, fontWeight:400, fontStyle:'italic'
	}, text:{value:'SEE&nbsp;WHERE&nbsp;THE&nbsp;TRAIN&nbsp;CAN&nbsp;TAKE&nbsp;YOU.'}}, _container);
	
	spongeapi.init({type:'custom',isDynamic:true,onReady:frame1});

	function frame1() {
		spongeapi.parseDynamicClasses();


		TweenLite.from(".lineMask", 7.5, {width:0, ease:Power1.easeOut});
		TweenLite.to(".background728", 4, {scale:1, ease:Power0.easeNone});
		TweenLite.to(".footer", .5, {y:-90, delay:2.5, scale:1, ease:Power4.easeIn});

		TweenLite.delayedCall(2.5, frame2);
	} 
	
	function frame2() {
		TweenLite.to(".lead1_1, .leadlegal_1", .5, {alpha:1, ease:Power4.easeIn});

		TweenLite.delayedCall(1.5, frame3);
	} 
	
	function frame3() {
		TweenLite.to(".lead1_1, .leadlegal_1", .5, {alpha:0, ease:Power4.easeIn});

		TweenLite.to(".lead2_1, .leadlegal_2", .5, {delay:.25, alpha:1, ease:Power4.easeIn});
		
		TweenLite.delayedCall(2, frame4);
	} 

	function frame4() {
		TweenLite.to(".lead2_1, .leadlegal_2", .5, {x:'-=728', y:'+=90', ease:Power4.easeIn});

		TweenLite.to(".logo728", .5, {scale:1, x:'-=728', y:'+=90', ease:Power2.easeOut});
		TweenLite.to(".lead3_1, .leadlegal_3", .75, {delay:.6, x:20, ease:Power2.easeOut});
		TweenLite.to(".cta", .75, {delay:.65, x:269, ease:Power2.easeOut});
		//TweenLite.to(".logo", .5, {delay:0, alpha:0, ease:Power2.easeOut});
		TweenLite.to(".acela728", .5, {delay:.5, x:503, ease:Power2.easeOut});
		TweenLite.to(".lineMask", .75, {delay:.75, x:-20, y:54, rotation:-4, ease:Power2.easeOut});
		TweenLite.to(".seeWhere", .75, {delay:.8, x:503, ease:Power2.easeOut});
		
		TweenLite.to(".line2", 1.25, {delay:1.35, x:0, y:0, ease:Power2.easeOut});
		TweenLite.to(".shine", 1.25, {delay:2.5, x:160, ease:Power3.easeInOut});

		_plays++;
		if (_plays < _maxPlays) {
			TweenLite.delayedCall(7.25, fadeLoop);
		}
	}

	function fadeLoop() {
		TweenLite.set('.logo728', {x:"+=728", y:"-=90", alpha:0});
		TweenLite.to(".acela728", .25, {alpha:0, ease:Power2.easeOut});
		TweenLite.to(".logo728", .25, {delay:.25, alpha:1, ease:Power2.easeOut});
		TweenLite.to('.lead3_1, .leadlegal_3, .seeWhere, .cta, .line2, .lineMask, .shine',
			0.5, {alpha:0, ease:Power2.easeOut});
		
		
		TweenLite.set('.background728', {scale:.8});
		TweenLite.to('.footer', 0.5, {delay:.5, y:33, ease:Power2.easeOut, onComplete:reset});
	}

	function reset() {
		resetElements();
		frame1();
	}
}; 