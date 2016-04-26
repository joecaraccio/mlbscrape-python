try {
/*****************
 * Setup Module
 ****************/
if(window.QSI === undefined) window.QSI = {};
if (!QSI.dbg)
QSI.dbg = {
	log:function() {},
	c:function(m) {QSI.dbg.log(m);},
	d:function(m) {QSI.dbg.log(m);},
	t:function(m) {QSI.dbg.log(m);},
	e:function(m) {QSI.dbg.log(m);}
};
if (QSI.reg === undefined) QSI.reg = {};
if (QSI.ed === undefined) QSI.ed = {};
if (QSI.reqID === undefined) QSI.reqID = {};
if (QSI.global === undefined) {
	QSI.global = {
		currentZIndex:2000000000,
		imagePath:"http://zncvfm2dltswdzell-farris.siteintercept.qualtrics.com/WRSiteInterceptEngine/../WRQualtricsShared/Graphics/",
		graphicPath:"http://zncvfm2dltswdzell-farris.siteintercept.qualtrics.com/WRSiteInterceptEngine/../WRQualtricsSiteIntercept/Graphic.php?IM=",
		intercepts:{},
		maxCookieSize:null,
		eventTrackers:[],
		startTime:1461437321350
	};
}
QSI.baseURL = 'http://siteintercept.qualtrics.com/WRSiteInterceptEngine/';


QSI.adobeVar = 's';


//This is used by IE to get the stored user data off the storage element
QSI.id = 'SI_3CWPKrI10k7ANBX';

QSI.reqID.SI_3CWPKrI10k7ANBX = true;

QSI.Browser = {
	name:'Firefox',
	version:44,
	isMobile:false,
	isBrowserSupported:true
};
QSI.CookieDomain = '';
QSI.currentURL = window.location.href.split('?')[0];
(function(){
	// Create the measurement node
	var scrollDiv = document.createElement("div");
	scrollDiv.className = "scrollbar-measure";
	scrollDiv.style.width = '100px';
	scrollDiv.style.height = '100px';
	scrollDiv.style.overflow = 'scroll';
	scrollDiv.style.position = 'absolute';
	scrollDiv.style.top = '-99999px';
	document.body.appendChild(scrollDiv);

	// Get the scrollbar width
	var scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth;
	QSI.scrollbarWidth = scrollbarWidth; // Mac:  15

	// Delete the DIV
	document.body.removeChild(scrollDiv);

})();
/****************
* Global Includes
****************/
QSI.util={creativeTypes:{EMPTY:"Empty",FEEDBACK_LINK:"FeedbackLink",HTTP_REDIRECT:"HTTPRedirect",IFRAME:"IFrame",INFO_BAR:"InfoBar",LINK:"Link",NO_CREATIVE:"NoCreative",POP_OVER:"PopOver",POP_UNDER:"PopUnder",POP_UP:"PopUp",RELAY:"Relay",SLIDER:"Slider",SOCIAL_MEDIA:"SocialMedia",USER_DEFINED_HTML:"UserDefinedHTML"},originalDocumentOverflow:"auto",$:function(a){return"string"==typeof a&&(a=document.getElementById(a)),a},setStyle:function(a,b){QSI.util.forOwn(b,function(c,d){try{a.style[d]=b[d]}catch(e){QSI.dbg.e(e)}})},getStyle:function(a,b){var c,d=this.getStyles(a);try{c=d?d[b]||d.getPropertyValue(b):void 0}catch(e){c=void 0}return void 0===c?c:c+""},getStyles:function(a){return window.getComputedStyle?a.ownerDocument.defaultView.opener?a.ownerDocument.defaultView.getComputedStyle(a,null):window.getComputedStyle(a,null):document.documentElement.currentStyle?a.currentStyle:void 0},prependElement:function(a,b){b.firstChild?b.insertBefore(a,b.firstChild):b.appendChild(a)},getTempID:function(){return"QSI_"+Math.floor(1e5*Math.random()+1)},getDateNow:function(){return Date.now?Date.now():(new Date).valueOf()},getElementHTML:function(a){var b=document.createElement("div");return b.appendChild(a.cloneNode(!0)),b.innerHTML},buildQueryString:function(a){var b=[];return QSI.util.forOwn(a,function(c,d){b.push(encodeURIComponent(d)+"="+encodeURIComponent(a[d]))}),b.join("&")},waitForFocus:function(){var a=QSI.util.Deferred();return document.hasFocus()?a.resolve():QSI.util.observe(window,"focus",function(){a.resolve()}),a.promise()},truncateString:function(a,b){var c="...";return null===a||void 0===a?null:a.length<=b?a:a.slice(0,b)+c},ScriptLoader:function(a){var b={},c=document.getElementsByTagName("script")[0];this.getScriptURL=function(b){return a+b},this.load=function(a,e){if(void 0!==a&&null!==a){var f="";e&&(f=d(e));var g,h,i=QSI.util.Deferred();return h=this.getScriptURL(a)+f,b[h]=!0,g=QSI.util.build("script",{src:h,"data-qsimodule":"script"}),QSI.util.observe(g,"load",function(){i.resolve()}),QSI.util.observe(g,"readystatechange",function(){("loaded"===g.readyState||"complete"===g.readyState)&&i.resolve()}),c.parentNode.insertBefore(g,c),i.promise()}};var d=function(a){var b=[];return QSI.util.forOwn(a,function(c,d){b.push(d+"="+a[d])}),"?"+b.join("&")}},generateRandomID:function(a){return a+"_"+Math.round(1e8*Math.random())},build:function(a,b,c){var d=document.createElement(a);if(b){var e=this;QSI.util.forOwn(b,function(a,c){switch(c){case"style":e.setStyle(d,b[c]);break;case"className":d.className=b[c];break;case"id":d.id=b[c];break;default:d.setAttribute(c,b[c])}})}if(c)if(QSI.util.isString(c))"style"==a&&d.styleSheet?d.styleSheet.cssText=c:d.appendChild(document.createTextNode(String(c)));else if(QSI.util.isArray(c))for(var f=0,g=c.length;g>f;f++){var h=c[f];"string"==typeof h||"number"==typeof h?d.appendChild(document.createTextNode(String(h))):h&&h.nodeType&&d.appendChild(h)}return d},showTrialIcon:function(){if(!this.trialIcon){var a=this.build("div",{},[this.build("img",{src:QSI.global.imagePath+"/siteintercept/logo.png"})]);this.trialIcon=a,QSI.util.setStyle(a,{opacity:.5,padding:"20px",bottom:"0",right:"0",position:"fixed"}),document.body.appendChild(a)}},createArrayFromArguments:function(a){return a?Array.prototype.slice.call(a):[]},createArrayFromIterable:function(a){for(var b=a.length||0,c=new Array(b);b--;)c[b]=a[b];return c},sendHttpRequest:function(a){var b=new XMLHttpRequest;b.open(a.type,a.url),a.timeout&&(b.timeout=a.timeout,a.timeoutCallback&&(b.ontimeout=a.timeoutCallback));for(var c in a.header)b.setRequestHeader(c,a.header[c]);a.includeCookies&&(b.withCredentials=!0,b.setRequestHeader("Access-Control-Allow-Credentials","true")),b.onreadystatechange=function(){4==b.readyState&&(200==b.status&&a.successCallback?a.successCallback(b):a.errorCallback&&a.errorCallback(b))},b.send(a.data)},Class:function(){function a(){try{this.initialize&&this.initialize.apply(this,arguments)}catch(a){QSI.dbg.e(a)}}function b(b){QSI.util.forOwn(b,function(c,d){a.prototype[d]=b[d]})}for(var c=QSI.util.createArrayFromArguments(arguments),d=0,e=c.length;e>d;d++)b(c[d]);return a},Creative:function(){var creative=this.Class.apply(this,arguments);return creative.prototype.globalInitialize=function(a){this.displayed=QSI.util.Deferred(),this.willShow=QSI.util.Deferred(),this.cookiesEnabled=QSI.util.Deferred(),this.preventRepeatedDisplay=QSI.util.Deferred(),this.localStorageEnabled=QSI.util.Deferred(),this.options=a||{},this.id=this.options.id,this.type=this.options.type,this.displayOptions=this.options.displayOptions||{},this.displayOptions.displayed=this.displayed.promise(),this.interceptDisplayOptions=this.options.interceptDisplayOptions||{},this.actionOptions=this.options.actionOptions||{};var b;if(this.actionOptions.actionSetJavaScriptBeforeDisplay&&this.shouldShow()&&(b=this.actionOptions.actionSetJavaScriptBeforeDisplay,this.evalJS(b)),this.actionOptions.actionSetJavaScript){var c=this;b=this.actionOptions.actionSetJavaScript,this.displayed.done(function(){c.evalJS(b)})}this.actionOptions.actionSetEvents&&QSI.util.processElementEvents(this.actionOptions.actionSetEvents,null,this),this.getType()!=QSI.util.creativeTypes.POP_UNDER&&this.killPopUnder(),QSI.util.addStatsImage()},creative.prototype.evalJS=function(js){try{eval(js)}catch(e){QSI.dbg.c("Error During Eval JavaScript "+e)}},creative.prototype.getType=function(){return this.type},creative.prototype.getTarget=function(a){var b=this.options.targetURL,c=QSI.EmbeddedData.getEmbeddedData(this.id,a);return c&&(c=encodeURIComponent(c),"Internet Explorer"==QSI.Browser.name&&QSI.Browser.version<9&&(c=c.substring(0,2050-b.length)),b+="&Q_ED="+c),b},creative.prototype.getTargetHelper=function(a){var b=this;return function(){return b.getTarget(a)}},creative.prototype.resetStyles=function(){if(this.options.resetStyle){var a=QSI.util.build("style",{type:"text/css"});if(a.styleSheet){var b=document.getElementsByTagName("head")[0];b.appendChild(a),a.styleSheet.cssText=this.options.resetStyle}else{document.body.appendChild(a);var c=document.createTextNode(this.options.resetStyle);a.appendChild(c)}}},creative.prototype.killPopUnder=function(){try{var a="QSIPopUnder_"+this.id;if(QSI.cookie.get(a)){var b=QSI.util.openWin("",a);b&&b.w&&(b.w.popunderDead=!0),b.close(),QSI.cookie.erase(a)}}catch(c){}},creative.prototype.shouldShow=function(){var a=!0;return this.interceptDisplayOptions.hideOnCookiesDisabled&&(QSI.cookie.areCookiesEnabled()?this.cookiesEnabled.resolve():(this.cookiesEnabled.reject(),a=!1)),this.interceptDisplayOptions.hideOnLocalStorageDisabled&&(QSI.localStorage.isLocalStorageEnabled()?this.localStorageEnabled.resolve():(this.localStorageEnabled.reject(),a=!1)),this.shouldPreventRepeatedDisplay()?(this.preventRepeatedDisplay.resolve(),a=!1):this.preventRepeatedDisplay.reject(),a?(this.willShow.resolve(),!0):(this.willShow.reject(),!1)},creative.prototype.shouldPreventRepeatedDisplay=function(){var a=!1;if(0!=this.interceptDisplayOptions.noshow)try{null!==QSI.cookie.get(this.id+"_intercept")?(a=!0,QSI.cookie.erase(this.id+"_intercept")):null!==QSI.cookie.get("QSI_"+this.id+"_intercept")&&(a=!0)}catch(b){QSI.dbg.e(b)}else QSI.cookie.erase("QSI_"+this.id+"_intercept");return a},creative.prototype.setPreventRepeatedDisplayCookie=function(){if(this.interceptDisplayOptions&&this.interceptDisplayOptions.noshow&&0!=this.interceptDisplayOptions.noshow&&null===QSI.cookie.get("QSI_"+this.id+"_intercept"))try{QSI.cookie.set("QSI_"+this.id+"_intercept",!0,this.interceptDisplayOptions.noshow,this.interceptDisplayOptions.cookieDomain,{force:!0})}catch(a){QSI.dbg.e(a)}},creative.prototype.impress=function(){QSI.util.impress(this.options.impressionURL),this.setPreventRepeatedDisplayCookie()},creative.prototype.close||(creative.prototype.close=function(){}),creative.prototype.remove||(creative.prototype.remove=creative.prototype.close),creative},evalJSON:function(json){try{return eval("("+json+")")}catch(e){QSI.dbg.e(e)}},isString:function(a){return"string"==typeof a},isArray:function(a){return"object"==typeof a&&a instanceof Array},isFunction:function(a){return"function"==typeof a||!1},isIE8:function(){return this.isIE(8)},isIE:function(a){return"Internet Explorer"!=QSI.Browser.name?!1:a?a==QSI.Browser.version:!0},isChrome:function(){return"Chrome"===QSI.Browser.name},isOpera:function(){return"Opera"===QSI.Browser.name},isFF:function(){return"Firefox"===QSI.Browser.name},removePx:function(a){a=a||"";var b=a.indexOf("px");return b>0&&(a=a.substr(0,b)),a},getDimensions:function(a){var b=!0;a.parentNode&&a.parentNode.tagName||(document.body.appendChild(a),b=!1);var c=a.style.display||this.getComputedStyle(a).display;if("none"!=c&&null!==c){var d={width:a.offsetWidth,height:a.offsetHeight};return b||a.parentNode.removeChild(a),d}var e=a.style,f=e.visibility,g=e.position,h=e.display;e.visibility="hidden",e.position="absolute",e.display="block";var i=a.clientWidth,j=a.clientHeight;return e.display=h,e.position=g,e.visibility=f,b||a.parentNode.removeChild(a),{width:i,height:j}},convertPercentToPixel:function(a,b){return Math.round(a/100*b)},convertPixelToPercent:function(a,b){return Math.round(a/b*100)},cumulativeOffset:function(a){var b,c={top:0,left:0},d=a&&a.ownerDocument;if(d)return b=d.documentElement,"undefined"!=typeof a.getBoundingClientRect&&(c=a.getBoundingClientRect()),{top:c.top+(window.pageYOffset||b.scrollTop)-(b.clientTop||0),left:c.left+(window.pageXOffset||b.scrollLeft)-(b.clientLeft||0)}},getTimeout:function(a){var b=QSI.util.Deferred();return a=1e3*parseFloat(a),window.setTimeout(function(){b.resolve()},a),b.promise()},getComputedStyle:function(a){return a.currentStyle||window.getComputedStyle(a,null)},getWindowSize:function(a){var b=a||window,c=this.getPageSize(a);return{width:b.outerWidth||c.width,height:b.outerHeight||c.height}},getPageSize:function(a){a=a||window;var b=a.document.documentElement||{};return{width:a.innerWidth||b.clientWidth,height:a.innerHeight||b.clientHeight}},getScrollOffsets:function(){var a=window,b=a.document.documentElement,c="pageYOffset",d="pageXOffset",e=d in a?a[d]:b.scrollLeft,f=c in a?a[c]:b.scrollTop;return{left:e,top:f}},startScrolling:function(){if("Internet Explorer"==QSI.Browser.name&&QSI.Browser.version<8){var a=document.getElementsByTagName("html")[0];QSI.util.setStyle(a,{overflow:this.originalDocumentOverflow})}else QSI.util.setStyle(document.body,{overflow:this.originalDocumentOverflow});document.ontouchmove=QSI.touchScrollEvent,QSI.touchScrollEvent=null},stopScrolling:function(){if("Internet Explorer"==QSI.Browser.name&&QSI.Browser.version<8){var a=document.getElementsByTagName("html")[0];this.originalDocumentOverflow=this.originalDocumentOverflow||this.getStyle(a,"overflow"),QSI.util.setStyle(a,{overflow:"hidden"})}else this.originalDocumentOverflow=this.originalDocumentOverflow||this.getStyle(document.body,"overflow"),QSI.util.setStyle(document.body,{overflow:"hidden"});document.ontouchmove&&(QSI.touchScrollEvent=document.ontouchmove),document.ontouchmove=function(a){a.preventDefault()}},hasScrollbars:function(){var a=document.documentElement;if("Internet Explorer"===QSI.Browser.name&&QSI.Browser.version<8)return!0;if("Internet Explorer"===QSI.Browser.name&&QSI.Browser.version<9){var b=a.offsetWidth-a.scrollWidth;return b>6}return a.scrollWidth<window.innerWidth},pageMode:function(){return"CSS1Compat"==document.compatMode?"Standards":"Quirks"},isFixed:function(){return!("Internet Explorer"==QSI.Browser.name&&"Standards"!=this.pageMode())},openWin:function(a,b,c){var d=[];return c=c||{},QSI.util.forOwn(c,function(a,b){d.push(b+"="+c[b])}),d=d.join(","),window.open(a,b,d)},impress:function(a){if(a){var b=QSI.util.build("img",{src:a+"&r="+(new Date).getTime(),style:{display:"none"}});document.body.appendChild(b)}},getQueryParam:function(a,b){b=b.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]");var c="[\\?&]"+b+"=([^&#]*)",d=new RegExp(c),e=d.exec(a);return null===e?"":e[1]},capFirst:function(a){return a.charAt(0).toUpperCase()+a.slice(1)},observe:function(a,b,c){this.obs=this.obs||[],a&&(this.obs.push({el:a,e:b,f:c}),a.addEventListener?a.addEventListener(b,c,!1):a.attachEvent?a.attachEvent("on"+b,c):a["on"+this.capFirst(b)]&&(a["on"+this.capFirst(b)]=c))},stopObserving:function(a,b,c){a.removeEventListener?a.removeEventListener(b,c,!1):a.detachEvent?a.detachEvent("on"+b,c):a["on"+this.capFirst(b)]&&(a["on"+this.capFirst(b)]=null)},removeObservers:function(){var a=this;this.each(this.obs||[],function(b){a.stopObserving(b.el,b.e,b.f)})},hasReachedScrollPosition:function(a){var b=this.getScrollOffsets().top,c=this.getPageSize().height,d=document.body.scrollHeight,e=d*(a/100);return b+c>=e?!0:!1},remove:function(a){a&&a.parentNode&&a.parentNode.removeChild(a)},removeAllByQuery:function(a,b){var c=a.querySelectorAll(b);Array.prototype.forEach.call(c,function(a){QSI.util.remove(a)})},buildWidget:function(a,b){var c="build"+a+"Widget";return this[c]?this[c](b):""},buildCCDWidget:function(a){if(a=a||{},a.close&&parseInt(a.close,10)>0){var b=a.close,c=this.getTempID(),d=this.build("span",{id:c},b+""),e=this.build("span",{},[d]),f=this,g=function(){var d=function(){if(!(0>=b)){var a=f.$(c);a&&(a.innerHTML=--b+""),setTimeout(d,1e3)}};a.delay&&a.delay>0?setTimeout(function(){setTimeout(d,1e3)},1e3*a.delay):setTimeout(d,1e3)};return a.displayed?a.displayed.done(function(){g()}):g(),this.getElementHTML(e)}return""},positionFixed:function(a,b,c){a.style.position="absolute";var d,e=0,f=this.getPageSize().height,g=document.body.scrollHeight,h=QSI.util.getScrollOffsets().top;h>0&&("auto"==c?(a.style.top=h+parseInt(b,10)+"px",a.style.bottom=c):"auto"==b&&(a.style.bottom=h+f-parseInt(b,10)+"px",a.style.top=b)),"string"==typeof b&&b.indexOf("px")>-1&&(b=parseInt(b,10)),"string"==typeof c&&c.indexOf("px")>-1&&(c=parseInt(c,10));var i=function(){clearTimeout(d),d=setTimeout(function(){var d=QSI.util.getScrollOffsets().top;if(!(0>d||d+f>g)){var h=d+b,j=h-e,k=j>=0?20:-20;Math.abs(j)<10&&(k=j);var l;e=h,"auto"==c?l=setInterval(function(){var b=parseInt(a.style.top,10)+k;a.style.top=b+"px",a.style.bottom=c,k>0?b>=h&&(clearInterval(l),QSI.util.observe(window,"scroll",i)):h>=b&&(clearInterval(l),QSI.util.observe(window,"scroll",i)),QSI.util.observe(window,"scroll",i)},15):"auto"==b&&(l=setInterval(function(){var e=parseInt(a.style.bottom,10)+k;a.style.bottom=d+f-c+"px",a.style.top=b,a.style.bottom=e+"px",k>0?e>=h&&(clearInterval(l),QSI.util.observe(window,"scroll",i)):h>=e&&(clearInterval(l),QSI.util.observe(window,"scroll",i)),QSI.util.observe(window,"scroll",i)},15))}},60)};QSI.util.observe(window,"scroll",i)},each:function(a,b){var c=a.length;if(c)for(var d=0;c>d;d++)b(a[d],d)},forOwn:function(a,b){if(a&&a instanceof Object&&this.isFunction(b))for(var c in a)a.hasOwnProperty(c)&&b(a[c],c,a)},filter:function(a,b){try{if(a.filter&&this.isFunction(a.filter))return a.filter(b)}catch(c){}var d=a.length,e=[];if(d)for(var f=0;d>f;f++)b(a[f])&&e.push(a[f]);return e},Deferred:function(){var a={},b="pending",c=[],d=[],e=[],f=[],g={state:function(){return b},then:function(a,b){return this.done(a).fail(b),this},done:function(a){return"pending"==b?e.push(a):"resolved"==b&&a.apply(this,c),this},fail:function(a){return"pending"==b?f.push(a):"rejected"==b&&a.apply(this,d),this},promise:function(){return g}};return QSI.util.forOwn(g,function(b,c){a[c]=g[c]}),a.resolve=function(){if("pending"==b){b="resolved";var a=QSI.util.createArrayFromArguments(arguments);c=a;var d=this;QSI.util.each(e,function(b){b.apply(d,a)})}},a.reject=function(){if("pending"==b){b="rejected";var a=QSI.util.createArrayFromArguments(arguments);d=a;var c=this;QSI.util.each(f,function(b){b.apply(c,a)})}},a},when:function(a){var b=QSI.util.createArrayFromArguments(arguments),c=b.length,d=c,e=1===d?a:QSI.util.Deferred(),f=function(a,b){return function(c){b[a]=arguments.length>1?c:QSI.util.createArrayFromArguments(arguments),--d||e.resolve(b)}};if(c>1)for(var g=0;c>g;g++)b[g]&&b[g].promise?b[g].promise().done(f(g,b)).fail(e.reject):d--;return 1>d&&e.resolve(b),e.promise()},moveToBackground:function(){("Firefox"===QSI.Browser.name||"Internet Explorer"===QSI.Browser.name&&QSI.Browser.version>=11)&&window.open("javascript:window.focus();","_self","")},handleMailTo:function(a,b,c,d){this.addClickImg(b,c,d,function(){window.location.href=a})},addClickImg:function(a,b,c,d){var e=new Date,f=QSI.baseURL+"?Q_Click=1&Q_CID="+c+"&Q_SIID="+a+"&Q_ASID="+b+"&T="+e.getTime()+"&Q_LOC="+encodeURIComponent(window.location.href);this.addImage(f,d)},addStatsImage:function(){try{if(!QSI.loggedStats&&Math.floor(100*Math.random())<1&&(window.performance||QSI.global.startTime)){QSI.loggedStats=!0;var a=(new Date).getTime(),b=a-(QSI.global.startTime||window.performance.timing.loadEventStart),c=QSI.baseURL+"?Q_Stats=1&Q_T="+b+"&T="+a;this.addImage(c)}}catch(d){QSI.dbg.e(d)}},addImage:function(a,b){var c=QSI.util.build("img",{src:a});QSI.util.isIE()&&QSI.util.setStyle(c,{display:"none"}),b&&QSI.util.observe(c,"load",b),document.body.appendChild(c)},processLocators:function(a,b){for(var c=0,d=a.length;d>c;c++){var e=a[c];e.locators&&(QSI.PipedText.setLocators(e.locators),e.content=QSI.PipedText.evaluateLocators(e.content,b))}},getDocDimension:function(a){var b=document,c=b.documentElement;return Math.max(b.body["scroll"+a],c["scroll"+a],b.body["offset"+a],c["offset"+a],c["client"+a])},getDocWidth:function(){return this.getDocDimension("Width")},getDocHeight:function(){return this.getDocDimension("Height")},getScroll:function(){var a=this.getScrollOffsets();return{width:this.getDocWidth(),height:this.getDocHeight(),left:a.left,top:a.top}},fireGoogleEventBeacon:function(a,b,c){return a.search(/^UA-\d+-\d{1,2}$/)<0?void QSI.dbg.c("Google Anylytics Account number is incorrect "+a):void(window.GoogleAnalyticsObject?this.googleEventAnyalytics(window.GoogleAnalyticsObject,a,b,c):this.googleEventGA(a,b,c))},googleEventGA:function(a,b,c){var d="SITracker"+this.getTempID(),e=window._gaq||[];e.push([d+"._setAccount",a]),e.push([d+"._trackEvent",b,c])},googleEventAnyalytics:function(a,b,c,d){var e="SITracker"+this.getTempID();window[a]("create",b,{name:e}),window[a](e+".send","event",c,d)},evalJS:function(stringToEval){return function(){try{eval(stringToEval)}catch(e){QSI.dbg.c("Error During Eval JavaScript "+e)}}},processElementEvents:function(a,b,c){if(!(!a||a.length<=0||a[0].length<=0)){for(var d=new QSI.ActionModule(c),e=a[0],f=0,g=e.length;g>f;f++)d.add(e[f]);d.addToElement(b)}}},QSI.Target=QSI.util.Class({initialize:function(a,b,c,d){this.el=a,this.options=c,this.urlCallback=b,this.deferred=QSI.util.Deferred(),this.parent=d,this.init()},init:function(){var a=this;QSI.util.observe(this.el,"click",function(){a.urlCallback&&(a.openTarget(),a.deferred.resolve())})},openTarget:function(){var a=this.urlCallback(),b=this.options;if(a&&0!==a.indexOf("&"))if(b.targetReplaceContents&&this.parent.getType()!==QSI.util.creativeTypes.USER_DEFINED_HTML&&(b.targetNewWindow=!0,b.targetReplaceContents=!1),b.targetNewWindow)try{var c=QSI.util.getPageSize(),d=b.targetFullScreen?screen.availWidth||screen.width||c.width:b.targetWidth,e=b.targetFullScreen?screen.availHeight||screen.height||c.height:b.targetHeight,f=QSI.util.openWin(a,"targetwindow",{location:"yes",status:"yes",scrollbars:"yes",resizable:"yes",width:d,height:e});setTimeout(function(){try{f.moveTo(0,0)}catch(a){QSI.dbg.e(a)}},500)}catch(g){QSI.dbg.e(g)}else b.targetEmbedded?new QSI.EmbeddedTarget(a,b):b.targetPopUnder?new QSI.PopUnderTarget(a,b,this.parent):b.targetReplaceContents?this.handleReplaceCreative():window.location=a},handleReplaceCreative:function(){var a,b,c=this.parent.node;this.options.sameSizeAsCreative?(a=this.parent.options.size.width,b=this.parent.options.size.height):(a=this.options.targetWidth,b=this.options.targetHeight);var d={width:a+"px",height:b+"px",display:"block",border:"none",outline:"none",zIndex:2e9},e=QSI.util.build("iframe",{src:this.urlCallback()});QSI.util.setStyle(e,d),this.parent.node=e,this.parent.options.size={width:a,height:b},c.parentNode.replaceChild(e,c),this.parent.displayOptions.customPosition&&this.parent.position()},complete:function(){return this.deferred.promise()}}),QSI.ActionModule=QSI.util.Class({initialize:function(a){this.creative=a,this.actions={click:[],mouseout:[],mouseover:[],displayed:[]}},add:function(a){this.actions[a.triggeringEvent]&&this.actions[a.triggeringEvent].push(this.buildAction(a))},buildAction:function(a){var b=this;return{run:function(){b["run"+a.actionType+"Action"]&&b["run"+a.actionType+"Action"](a)}}},runAddCookieAction:function(a){QSI.cookie.set(a.cookieName,a.cookieValue,this.creative.interceptDisplayOptions.cookieDomain)},runRemoveCookieAction:function(a){QSI.cookie.erase(a.cookieName,this.creative.interceptDisplayOptions.cookieDomain)},runGoogleEventAction:function(a){QSI.util.fireGoogleEventBeacon(a.accountNumber,a.actionCategory,a.actionName)},runJavaScriptAction:function(a){QSI.util.evalJS(a.javaScriptString)()},addToElement:function(a){var b=this,c=function(a){var c=!1;return function(){c||(c=!0,b.runAction(a))}};QSI.util.forOwn(this.actions,function(d,e){b.actions[e].length&&("displayed"===e?b.creative.displayed.done(c(b.actions[e])):QSI.util.observe(a,e,c(b.actions[e])))})},runAction:function(a){for(var b=0;b<a.length;b++)a[b].run()}});(!QSI.EmbeddedData||window.QTest)&&(QSI.EmbeddedData={getHTMLFromDOM:function(a){var b=QSI.util.$(a),c="";if(b)switch(b.tagName){case"TEXTAREA":case"INPUT":c=b.value;break;default:c=b.innerHTML}return c},getCookieVal:function(a){var b="",c=QSI.cookie.get(a);return c&&(b=c),b},getURLParameter:function(a){return QSI.util.getQueryParam(window.location.href,a)},getURLRegexMatch:function(a){var b=/^\/(.*)\/([gim]*)/,c=a.match(b);return c=window.location.href.match(c&&c[1]?new RegExp(c[1],c[2]):new RegExp(a)),c&&c[1]?c[1]:""},getJavaScriptValue:function(varName){var qsi_val="";try{qsi_val=eval(varName)}catch(e){QSI.dbg.e(e)}return qsi_val},getHistory:function(){return QSI.history.get()},getTimeOnSite:function(){return QSI.history.getTimeOnSite()},getCurrentPage:function(){return window.location},getReferer:function(){return QSI.history.getPageReferrer()},getSiteReferer:function(){return QSI.history.getSiteReferrer()},getSearchTerm:function(){return QSI.history.getSearch()},getPageCount:function(){var a=QSI.history.getPageCount();return a.unique},getTotalPageCount:function(){var a=QSI.history.getPageCount();return a.total},getPercentagePageViewed:function(){var a=QSI.history.getPageCount();return a.unique},getSiteInterceptID:function(){return this.siid},getCreativeID:function(){return QSI.global.intercepts[this.siid]&&QSI.global.intercepts[this.siid].CreativeID?QSI.global.intercepts[this.siid].CreativeID:void 0},getEventTrackingData:function(a){return QSI.EventTracker.get(a)},getSiteCatalystValue:function(a){for(var b=a.split("."),c=function(a){return a.charAt(0).toLowerCase()+a.slice(1)},d=window[QSI.adobeVar],e=0,f=b.length;f>e;e++)d&&(d=d[c(b[e])]);return d?d:null},getEmbeddedData:function(a,b){b=b||[];var c="";return QSI.ed[a]&&(b=b.concat(QSI.ed[a])),this.siid=a,c=this.generateDynamicEmbeddedData(b)},generateDynamicEmbeddedData:function(a){var b="";"string"==typeof a&&(a=a.split(""));for(var c=0,d=a.length;d>c;c++)try{var e=a[c];if(e.type&&e.name){var f="";switch(e.type){case"StaticVal":f=e.value;break;case"HTML":f=this.getHTMLFromDOM(e.value);break;case"Cookie":f=this.getCookieVal(e.value);break;case"QueryParam":f=this.getURLParameter(e.value);break;case"URLRegex":f=this.getURLRegexMatch(e.value);break;case"JavaScriptVal":f=this.getJavaScriptValue(e.value);break;case"SiteCatalyst":f=this.getSiteCatalystValue(e.value);break;case"EventTracking":f=this.getEventTrackingData(e.value);break;default:f=this["get"+e.type]?this["get"+e.type](e.value):e.value}f=String(f),f=encodeURIComponent(f),b+="&"+e.name+"="+f}}catch(g){QSI.dbg.e(g)}return b}});(!QSI.history||window.QTest)&&(QSI.history={limit:2e3,logVisit:function(){this.logCurrentURL(),this.logSearch(),this.startFocusTracking(),this.logReferrer()},startFocusTracking:function(){if(!this.started)try{this.started=!0,this.focusTime=this.getFocusTime(),this.blurTime=this.getBlurTime();var a=1,b=this;setInterval(function(){b.focused?b.focusTime+=a:b.blurTime+=a},1e3*a);var c=function(){b.focused=!0},d=function(){b.focused=!1};c(),QSI.util.observe(window,"focus",c),QSI.util.observe(window,"blur",d),QSI.util.observe(window,"unload",function(){QSI.profile.set("History","BlurTime",b.blurTime),QSI.profile.set("History","FocusTime",b.focusTime)})}catch(e){QSI.dbg.e(e)}},logSite:function(a,b){var c,d=QSI.cookie.get("QSI_HistorySession");if(d){d=decodeURIComponent(d);var e=d.split("|"),f=e[e.length-1];c=f.split("~")[0],d+="|"}else d="",c="";if(a!=c){var g=a+"~"+b;d+=g,this.writeHistory(d)}},writeHistory:function(a,b){if(null!==b&&void 0!==b&&0>=b)return void QSI.cookie.erase("QSI_HistorySession",encodeURIComponent(a),0);b=b||QSI.global.maxCookieSize||this.limit,a=this.limitSize(a,b);try{QSI.cookie.set("QSI_HistorySession",encodeURIComponent(a),0)}catch(c){this.writeHistory(a,b-500)}},limitSize:function(a,b){if(!a.length)return a;for(b=b||this.limit;a.length>b;){var c=a.split("|");c.splice(0,1),a=c.join("|")}return a},get:function(){var a=QSI.cookie.get("QSI_HistorySession"),b=a?decodeURIComponent(a):[];return b=this.limitSize(b)},logCurrentURL:function(){var a=window.location.href,b=1*new Date;this.logSite(a,b)},getReferrer:function(){return document.referrer},logSearch:function(){var a,b,c=this.getReferrer();if(c.search(/(google.com)|(bing.com)|(yahoo.com)/)>=0){var d="";c.search(/(google.com)|(bing.com)/)>=0?(a=/q=(.*?)\&/,b=c.match(a),b&&b.length&&b[1]&&(d=b[1])):c.search(/yahoo.com/)>=0&&(a=/p=(.*?)\&/,b=c.match(a),b&&b.length&&b[1]&&(d=b[1])),d=unescape(d),QSI.profile.set("History","SearchTerm",d)}},logReferrer:function(){var a=this.getReferrer();if(a){var b=QSI.util.build("a",{href:a});b.hostname!=document.location.host&&QSI.profile.set("History","SiteReferrer",a),QSI.profile.set("History","PageReferrer",a)}},logIntercept:function(a,b){b&&this.logActionSet(b)},logActionSet:function(a){if(a.search("AS_")>=0){var b=a,c=1*new Date;QSI.profile.set("ActionSetHistory",b,c),QSI.profile.set("ActionSetHistory",b,c,1)}},logSurvey:function(a,b){QSI.profile.set("QualtricsSurveyHistory",a,b,1)},getSiteReferrer:function(){return QSI.profile.get("History","SiteReferrer")},getPageReferrer:function(){return QSI.profile.get("History","PageReferrer")},getSearch:function(){var a=QSI.profile.get("History","SearchTerm");return a||(a=""),a},getTimeOnSite:function(){var a=this.getFocusTime(),b=this.getBlurTime();return a+b+"|"+a},getFocusTime:function(){var a=QSI.profile.get("History","FocusTime");return a||(a=0),a},getBlurTime:function(){var a=QSI.profile.get("History","BlurTime");return a||(a=0),a},getActionSetHistory:function(a,b){var c=QSI.profile.get("ActionSetHistory",a,b);return c||(c=0),c},getPageCount:function(){var a,b=QSI.cookie.get("QSI_HistorySession"),c=0,d=[];if(b){b=decodeURIComponent(b);var e=b.split("|");for(a=0,ilen=e.length;a<ilen;a++)d.push(e[a].split("~")[0]);var f={};for(a=0,ilen=d.length;a<ilen;a++)f[d[a]]||(c++,f[d[a]]=!0)}return{unique:c,total:d.length}}});QSI.profile={namespace:"QSI_",set:function(a,b,c,d){if(void 0===a||void 0===b||void 0===c)throw new Error("To few arguments");try{var e=this.getStorage(d),f=this.namespace+a,g=e.getItem(f);g=g?JSON.parse(g):{},g[b]=c,g=JSON.stringify(g),e.setItem(f,g)}catch(h){QSI.dbg.e("error setting profile item"),QSI.dbg.e(h)}},get:function(a,b,c){var d=this.getStorage(c),e=this.namespace+a,f=d.getItem(e);return f?(f=JSON.parse(f),b?f[b]?f[b]:null:f):null},erase:function(a,b,c){var d=this.getStorage(c),e=this.namespace+a;if(b){var f=JSON.parse(d.getItem(e));delete f[b],f=JSON.stringify(f),d.setItem(e,f)}else d.removeItem(e)},getStorage:function(a){if(this.hasSessionStorage())return a?localStorage:sessionStorage;if(QSI.UserDataStorage){var b=QSI.UserDataStorage;return b.isPermanent(a?!0:!1),b}return QSI.CookieStorage},hasSessionStorage:function(){var a="qualtricssessionstoragetestkey",b=window.sessionStorage;try{return b.setItem(a,a),b.removeItem(a),!0}catch(c){return!1}}};(!QSI.EventTracker||window.QTest)&&(QSI.EventTracker={counts:{},cookieName:"QSI_CT",clicked:!1,loaded:!1,trackElements:function(){this.loaded===!1&&(this.loadCounts(),this.loaded=!0);var a=QSI.global.eventTrackers,b=this;QSI.util.forOwn(a,function(c,d){var e=a[d];b.trackElement(e,d)}),QSI.util.observe(window,"beforeunload",function(){b.storeCounts()})},trackElement:function(a,b){var c=QSI.util.$(a);if(c){var d=this;QSI.util.observe(c,"click",function(){d.track(b)})}},track:function(a){this.clicked=!0,this.counts[a]?this.counts[a]++:this.counts[a]=1},storeCounts:function(){if(this.clicked===!0){var a=JSON.stringify(this.counts);QSI.cookie.set(this.cookieName,a)}},loadCounts:function(){var a=QSI.cookie.get(this.cookieName);a&&(this.counts=JSON.parse(a))},get:function(a){return this.counts[a]?this.counts[a]:0},incrementEventList:function(){if("_qsie"in window&&QSI.util.isArray(window._qsie))for(var a=0,b=window._qsie.length;b>a;a++){var c=window._qsie[a];QSI.util.isString(c)&&this.track(c)}}});QSI.localStorage={isLocalStorageEnabled:function(){try{var a="qsi_test_local_storage";return localStorage.setItem(a,"local_storage_test_value"),localStorage.removeItem(a),!0}catch(b){return!1}}};QSI.cookie={set:function(a,b,c,d,e){e=e||{};var f=this.getCookieSize(),g=this.get(a),h=QSI.global.maxCookieSize;g&&(f-=(a+"="+g).length);var i="";if(c){var j=new Date;j.setTime(j.getTime()+864e5*c),i="; expires="+j.toGMTString()}var k="";d?k="domain="+d:QSI.CookieDomain&&(k="domain="+QSI.CookieDomain);var l=a+"="+b,m=f+l.length;if(!(e.force||null!==h&&h>=m||null===h))throw new Error("Cannot exceed the specified maximum cookie size");this.cookieSize=e.erase?f:m,document.cookie=l+i+"; path=/; "+k},get:function(a){for(var b=a+"=",c=document.cookie.split(";"),d=0,e=c.length;e>d;d++){for(var f=c[d];" "==f.charAt(0);)f=f.substring(1,f.length);if(0===f.indexOf(b))return f.substring(b.length,f.length)}return null},erase:function(a,b){this.set(a,"",-1,b,{force:!0,erase:!0})},getCookieSize:function(){if(!this.cookieSize){this.cookieSize=0;for(var a=document.cookie.split(";"),b=0,c=a.length;c>b;b++){for(var d=a[b];" "==d.charAt(0);)d=d.substring(1,d.length);d.indexOf("QSI")>=0&&(this.cookieSize+=d.length)}}return this.cookieSize},areCookiesEnabled:function(){try{document.cookie="cookietest=1";var a=-1!=document.cookie.indexOf("cookietest=");return document.cookie="cookietest=1; expires=Thu, 01-Jan-1970 00:00:01 GMT",a}catch(b){return!1}}};QSI.CookieStorage=function(){function a(){try{var a=QSI.cookie.get(d);a&&(c=JSON.parse(a))}catch(b){c={}}}function b(){try{QSI.cookie.set(d,JSON.stringify(c))}catch(a){}}var c={},d="QSI_DATA";return a(),{setItem:function(a,d){c[a]=d,b()},getItem:function(a){return c[a]||null},removeItem:function(a){delete c[a],b()},reload:a,clear:function(){c={},b()}}}();void 0===window.QSI.DependencyResolver&&(QSI.DependencyResolver=QSI.util.Creative({initialize:function(a){this.options=a||{},this.resolve()},resolve:function(){var a=this.options.baseURL;if(this.options.dependencyValues){var b=this;QSI.util.forOwn(this.options.dependencyValues,function(c,d){"SiteCatalyst"===d&&(QSI["Resolve"+d].rootName=b.options.adobeSCVariable),a+=QSI["Resolve"+d].prepare(b.options.dependencyValues[d])})}a+="&Q_DPR=true",a+="&t="+(new Date).getTime(),this.options.debug&&(a+="&Q_DEBUG"),a+="&Q_VSI="+encodeURIComponent(this.options.validIntercepts);var c=QSI.util.build("script",{type:"text/javascript",src:a});document.body.appendChild(c)}}));QSI.ResolvePageCount={prepare:function(){var a="&Q_RPC=",b=QSI.history.getPageCount();return a+=b.total+"|"+b.unique}};(!QSI.API||window.QTest)&&(QSI.API={load:function(){if(!QSI.reg&&!this.unloading){var a=new QSI.util.ScriptLoader(QSI.baseURL),b={Q_LOC:encodeURIComponent(window.location.href)};"Editing"===QSI.version&&(b.Q_VERSION="0"),QSI.util.forOwn(QSI.reqID,function(c,d){0===d.search(/ZN/)?(b.Q_ZID=d,delete b.Q_SIID):(b.Q_SIID=d,delete b.Q_ZID),a.load("",b)})}},unload:function(){this.unloading=!0,QSI.reg&&(QSI.util.forOwn(QSI.reg,function(a,b){var c=QSI.reg[b];c.remove()}),QSI.util.removeObservers()),QSI.debug&&QSI.util.remove(QSI.util.$("QSI_Debug")),QSI.reg=void 0,this.unloading=!1},run:function(){QSI.InterceptsRan||void 0===QSI.reg||QSI.RunIntercepts()},Events:{increment:function(a){QSI.EventTracker.track(a)},count:function(a){return QSI.EventTracker.get(a)},push:function(a){QSI.EventTracker.track(a)}}});QSI.version = "Published";
QSI.InterceptsRan = false;
QSI.RunIntercepts = function(){
QSI.util.observe(window, 'message', function(e){
	if (e.data && typeof e.data === 'string')
	{
		var parts = e.data.split('|');
		if (parts[0] == 'QualtricsEOS')
		{
			var sid = parts[1];
			var ssid = parts[2];
			QSI.history.logSurvey(sid,ssid);
		}
	}

});

QSI.history.logVisit();


QSI.EventTracker.trackElements();
QSI.EventTracker.incrementEventList();
window._qsie = QSI.API.Events;

    (function(){
	var QSIDependencyResolver = new QSI.DependencyResolver({
		id:'SI_3CWPKrI10k7ANBX',
		baseURL:'http://siteintercept.qualtrics.com/WRSiteInterceptEngine/?Q_SIID=SI_3CWPKrI10k7ANBX&Q_LOC=http%3A%2F%2Fwww.baseball-reference.com%2Fplayers%2Fsplit.cgi%3Fid%3Dsabatc.01%26year%3DCareer%26t%3Dp',
		debug:false,
		dependencyValues:{"PageCount":true},
		validIntercepts:'[]',
        adobeSCVariable:'s'
	});
	QSI.reg['SI_3CWPKrI10k7ANBX'] = QSIDependencyResolver;
})();




QSI.InterceptsRan = true;

};
if(typeof JSON === 'undefined')
{
		var loader = new QSI.util.ScriptLoader('http://a248.e.akamai.net/img.qualtrics.com/WRQualtricsShared/JavaScript/SiteInterceptEngine/');
		loader.load('JSONParseModule.js').done(function() {
						QSI.RunIntercepts();
					});
}
else
{
				QSI.RunIntercepts();
		}
}catch(e){QSI.dbg.e(e);}