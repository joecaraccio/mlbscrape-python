var amzncsm=amzncsm||{};amzncsm.errorCodes={SLOT_INSIDE_UNFRIENDLY_FRAME:1,UNSUPPORTED_BROWSER:2,ERROR_SENDING_PIXEL:3,INVALID_API:4,MALFORMED_URL:5},amzncsm.errors=[],amzncsm.reportErrors=function(a){/^https?:\/\//.test(a)===!1&&(a=document.location.protocol+"//"+a),"/"!=a.substr(a.length-1)&&(a+="/");for(var b=0;b<amzncsm.errors.length;b++)payload='{"adViewability":[{"error": {"m": "'+amzncsm.errors[b]+'"}}], "c": "viewability", "api": "RTB", "error": 1}',"https:"===document.location.protocol&&/^http:\/\//.test(a)===!0&&(a=a.replace("http://","https://")),(new Image).src=a+payload+"&cb="+Math.round(1e7*Math.random());amzncsm.errors=[]},function(a,b){function c(a){return a?a.replace(/^\s+|\s+$/g,""):void 0}function d(a,b){if(b=b||{},!a)return{};a.m&&a.m.message&&(a=a.m);var d,i,j,k,l,m={m:e(a,b),c:a.c?""+a.c:a.c,s:[],name:a.name,type:a.type},n=0,o=0;if(d=a.stack||(a.err?a.err.stack:""),d&&d.split)for(i=d.split("\n");n<i.length&&m.s.length<g;)j=i[n++],j&&m.s.push(c(j));else for(k=f(a.args||arguments,"callee"),n=0,o=0;k&&g>n;)l=h,k.skipTrace||(j=k.toString(),j&&j.substr&&(l=0===o?4*h:l,l=1==o?2*h:l,m.s.push(j.substr(0,l)),o++)),k=f(k,"caller"),n++;return m}function e(a,b){var c=b.m||b.message||"";return c+=a.m&&a.m.message?a.m.message:a.m&&a.m.target&&a.m.target.tagName?"Error handler invoked by "+a.m.target.tagName+" tag":a.m?a.m:a.message?a.message:"Unknown error"}function f(a,b){try{return a[b]}catch(c){return}}var g=20,h=256;a.constructErrorMessage=d}(amzncsm,window),function(){var a=Array.prototype.slice;try{a.call(document.documentElement)}catch(b){Array.prototype.slice=function(b,c){var d,e,f,g,h,i;if(c="undefined"!=typeof c?c:this.length,"[object Array]"===Object.prototype.toString.call(this))return a.call(this,b,c);if(e=[],g=this.length,h=b||0,h=h>=0?h:g+h,i=c?c:g,0>c&&(i=g+c),f=i-h,f>0)if(e=new Array(f),this.charAt)for(d=0;f>d;d++)e[d]=this.charAt(h+d);else for(d=0;f>d;d++)e[d]=this[h+d];return e}}}(),Object.keys||(Object.keys=function(){"use strict";var a=Object.prototype.hasOwnProperty,b=!{toString:null}.propertyIsEnumerable("toString"),c=["toString","toLocaleString","valueOf","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","constructor"],d=c.length;return function(e){if("object"!=typeof e&&("function"!=typeof e||null===e))throw new TypeError("Object.keys called on non-object");var f,g,h=[];for(f in e)a.call(e,f)&&h.push(f);if(b)for(g=0;d>g;g++)a.call(e,c[g])&&h.push(c[g]);return h}}()),window.JSON||(window.JSON={parse:function(sJSON){return eval("("+sJSON+")")},stringify:function(){var a=Object.prototype.toString,b=Array.isArray||function(b){return"[object Array]"===a.call(b)},c={'"':'\\"',"\\":"\\\\","\b":"\\b","\f":"\\f","\n":"\\n","\r":"\\r","	":"\\t"},d=function(a){return c[a]||"\\u"+(a.charCodeAt(0)+65536).toString(16).substr(1)},e=/[\\"\u0000-\u001F\u2028\u2029]/g;return function f(c){var g,h,i,j;if(null==c)return"null";if("number"==typeof c)return isFinite(c)?c.toString():"null";if("boolean"==typeof c)return c.toString();if("object"==typeof c){if("function"==typeof c.toJSON)return f(c.toJSON());if(b(c)){for(g="[",h=0;h<c.length;h++)g+=(h?", ":"")+f(c[h]);return g+"]"}if("[object Object]"===a.call(c)){i=[];for(j in c)c.hasOwnProperty(j)&&i.push(f(j)+": "+f(c[j]));return"{"+i.join(", ")+"}"}}return'"'+c.toString().replace(e,d)+'"'}}()}),Array.isArray||(Array.isArray=function(a){return"[object Array]"===Object.prototype.toString.call(a)}),String.prototype.endsWith||(String.prototype.endsWith=function(a,b){var c,d=this.toString();return("number"!=typeof b||!isFinite(b)||Math.floor(b)!==b||b>d.length)&&(b=d.length),b-=a.length,c=d.indexOf(a,b),-1!==c&&c===b}),function(){if(window.Event){var a=function(a,b){b=b||{bubbles:!1,cancelable:!1,detail:void 0};var c=document.createEvent("CustomEvent");return c.initCustomEvent(a,b.bubbles,b.cancelable,b.detail),c};a.prototype=window.Event.prototype,window.CustomEvent=a}}(),function(a){var b,c,d,e,f;a.performance||(a.performance={}),a.performance.now||(a.performance.now=performance.now||performance.webkitNow||performance.msNow||performance.mozNow),a.performance.now||(b=Date.now?Date.now():+new Date,performance.timing&&performance.timing&&(b=performance.timing.navigationStart),a.performance.now=function(){var a=Date.now?Date.now():+new Date;return a-b}),c=[],d={},e=function(a,b){for(var d=0,e=c.length,f=[];e>d;d++)c[d][a]==b&&f.push(c[d]);return f},f=function(a,b){for(var d,e=c.length;e--;)d=c[e],d.entryType!=a||void 0!==b&&d.name!=b||c.splice(e,1)},a.performance.mark||(a.performance.mark=a.performance.webkitMark||function(b){var e={name:b,entryType:"mark",startTime:a.performance.now(),duration:0};c.push(e),d[b]=e}),a.performance.measure||(a.performance.measure=a.performance.webkitMeasure||function(a,b,e){b=d[b].startTime,e=d[e].startTime,c.push({name:a,entryType:"measure",startTime:b,duration:e-b})}),a.performance.getEntriesByType||(a.performance.getEntriesByType=a.performance.webkitGetEntriesByType||function(a){return e("entryType",a)}),a.performance.getEntriesByName||(a.performance.getEntriesByName=a.performance.webkitGetEntriesByName||function(a){return e("name",a)}),a.performance.clearMarks||(a.performance.clearMarks=a.performance.webkitClearMarks||function(a){f("mark",a)}),a.performance.clearMeasures||(a.performance.clearMeasures=a.performance.webkitClearMeasures||function(a){f("measure",a)})}(window),amzncsm=amzncsm||{},amzncsm.log=function(a){try{-1!==window.location.href.indexOf("csm_debug_mode")&&window.console&&window.console.log(a)}catch(b){b.message&&amzncsm.errors.push(b.message)}},amzncsm.loadModules=function(a,b){var c,d,e;try{for(c=0;c<b.length;c++){if(d=b[c].name,e=b[c].params||[],window.performance&&window.performance.mark&&"function"==typeof window.performance.mark&&window.performance.mark("loadStart"+d+a),"[object Array]"!==Object.prototype.toString.call(e),amzncsm[d]){if(void 0===amzncsm[d].shortName)throw new amzncsm.invalidModuleException("Module shortName not defined for module "+d+". ");e.unshift(a),amzncsm[d].init.apply(amzncsm[d],e)}window.performance&&window.performance.mark&&"function"==typeof window.performance.mark&&(window.performance.mark("loadEnd"+d+a),window.performance.measure("lt"+amzncsm[d].shortName+a,"loadStart"+d+a,"loadEnd"+d+a))}}catch(f){f.message&&amzncsm.errors.push(f.message)}},amzncsm.define=function(a){var b,c,d,e,f,g,h,i;try{for(b=function(a){return"string"==typeof a?amzncsm[a]:a},c=Array.prototype.slice.call(arguments),d=c[0],e=c.length>2?c[1]:[],f=c[c.length-1],g=[],h=0,i=e.length;i>h;h++)g.push(b(e[h]));amzncsm[d]=f.apply(f,g)}catch(j){j.message&&amzncsm.errors.push(j.message)}},amzncsm.invalidModuleException=function(a){this.value=a,this.message="does not conform to the expected format of a module",this.toString=function(){return this.value+this.message}},amzncsm.define("utils",[],function(){var a={shortName:"ut"};return a.init=function(a){},a.getIEVersion=function(){var a,b,c=-1;return"Microsoft Internet Explorer"==navigator.appName?(a=navigator.userAgent,b=new RegExp("MSIE ([0-9]{1,}[.0-9]{0,})"),null!=b.exec(a)&&(c=parseFloat(RegExp.$1))):navigator.userAgent.match(/Trident.*rv\:11\./)?c=11:navigator.userAgent.match(/Edge\/\d+\.\d+/)&&(c=12),c},a.isIE=function(){var b=a.getIEVersion();return b>-1},a.isFirefox=function(){return"undefined"!=typeof InstallTrigger},a.isChrome=function(){return/Chrome/.test(navigator.userAgent)&&/Google Inc/.test(navigator.vendor)},a.isSafari=function(){return/Safari/.test(navigator.userAgent)&&/Apple Computer/.test(navigator.vendor)},a.isWebkit=function(){return a.isChrome()||a.isSafari()},a.isSupportedBrowser=function(){return a.isIE()&&amzncsm.config.supportedBrowsers.IE===!0||a.isFirefox()&&amzncsm.config.supportedBrowsers.Firefox===!0||a.isChrome()&&amzncsm.config.supportedBrowsers.Chrome===!0||a.isSafari()&&amzncsm.config.supportedBrowsers.Safari===!0},a.convertToInt=function(a){return"number"==typeof a?a:parseInt(a)},a.getPixelID=function(){var a=null;return function(){return null===a&&(a=Math.random().toString(36).substr(2)),a}}(),a.reportClientError=function(a){var b=a===parseInt(a,10)?a:JSON.stringify(amzncsm.constructErrorMessage(a)),c=amzncsm.instrURL,d='{"adViewability":[{"error": '+b+'}], "c": "viewability", "api": "RTB", "error": 1}';amzncsm.scrollImitationTimer&&clearInterval(amzncsm.scrollImitationTimer),/^https?:\/\//.test(c)===!1&&(c=document.location.protocol+"//"+c),"/"!=c.substr(c.length-1)&&(c+="/"),"https:"===document.location.protocol&&/^http:\/\//.test(c)===!0&&(c=c.replace("http://","https://")),(new Image).src=c+d+"&cb="+Math.round(1e7*Math.random())},a.setTimeout=function(b,c){return setTimeout(function(){try{b.call()}catch(c){c.message,a.reportClientError(c)}},c)},a.setInterval=function(b,c){return setInterval(function(){try{b.call()}catch(c){c.message,a.reportClientError(c)}},c)},a}),amzncsm.define("eventUtils",[],function(){var a={shortName:"eu"};return a.init=function(a){},a.addEvent=function(a,b,c,d){a.addEventListener?a.addEventListener(b,c,d):a.attachEvent&&a.attachEvent("on"+b,c)},a.addCustomEvent=function(a,b,c){document.addEventListener?document.addEventListener(a,b,c):document.attachEvent?document.attachEvent("on"+a,function(){return b.call(document,window.event)}):document["on"+a]=b},a.removeEvent=function(a,b,c){document.removeEventListener?a.removeEventListener(b,c,!1):document.detachEvent&&a.detachEvent("on"+b,c)},a.createEvent=function(){return document.createEvent?function(a){var b=document.createEvent("HTMLEvents");return b.initEvent(a,!0,!0),b}:function(a){var b=document.createEventObject();return b.eventType=a,b}}(),a.dispatchCustomEvent=function(b){document.dispatchEvent?document.dispatchEvent(a.createEvent(b)):document[b]?document[b]():document["on"+b]&&document["on"+b]()},a.stopPropagation=function(a){return a.stopPropagation?void a.stopPropagation():void(a.cancelBubble=!0)},a.preventDefault=function(a){a.preventDefault&&a.preventDefault(),a.returnValue=!1},a.getClickXY=function(a){return"pageX"in a?{pageX:a.pageX,pageY:a.pageY}:{pageX:a.clientX+document.documentElement.scrollLeft,pageY:a.clientY+document.documentElement.scrollTop}},a.handleVisibilityChange=function(b,c){var d,e=b.document;"undefined"!=typeof e.hidden?d="visibilitychange":"undefined"!=typeof e.mozHidden?d="mozvisibilitychange":"undefined"!=typeof e.msHidden?d="msvisibilitychange":"undefined"!=typeof e.webkitHidden&&(d="webkitvisibilitychange"),d&&a.addEvent(e,d,c,!1)},a.isPageVisibilitySupported=function(){return"undefined"!=typeof document.hidden||"undefined"!=typeof document.mozHidden||"undefined"!=typeof document.msHidden||"undefined"!=typeof document.webkitHidden},a.registerPostMessageHandler=function(a){var b=window.addEventListener?"addEventListener":"attachEvent",c=window[b],d="attachEvent"==b?"onmessage":"message";c(d,function(b){var c=b.message?"message":"data",d=b[c];a(d)},!1)},a.getVisibilityState=function(a){return"undefined"==typeof a.visibilityState?"Unknown":a.visibilityState},a.documentHasFocus=function(a){var b=!0;try{b=a.hasFocus?a.hasFocus():!0}catch(c){amzncsm.reportClientError(c)}return b},a.isWindowActive=function(b){var c,d;return"undefined"!=typeof b.hidden?c="hidden":"undefined"!=typeof b.mozHidden?c="mozHidden":"undefined"!=typeof b.msHidden?c="msHidden":"undefined"!=typeof b.webkitHidden&&(c="webkitHidden"),d=a.documentHasFocus(b),"undefined"==typeof b[c]?d:!b[c]},a}),amzncsm.define("pixelQueue",[],function(){var a,b={shortName:"pq"},c=2500,d=4;return b.init=function(a,b){amzncsm.csmReport.pq={queue:[],instrURL:b}},b.firePixel=function(a){var b=amzncsm.csmReport.pq.instrURL;""!==b&&(/^https?:\/\//.test(b)===!1&&(b=document.location.protocol+"//"+b),"/"!=b.substr(b.length-1)&&(b+="/"),"https:"===document.location.protocol&&/^http:\/\//.test(b)===!0&&(b=b.replace("http://","https://")),(new Image).src=b+a+"&cb="+Math.round(1e7*Math.random()))},a=function(){var a=amzncsm.csmReport.pq;a.queue.length>0&&(a.queue=[])},b.addPixel=function(b){var e=this,f=amzncsm.csmReport.pq;0===f.queue.length&&amzncsm.setTimeout(function(){f.queue.length>0&&(e.send(),a())},c),f.queue.push(JSON.parse(b)),f.queue.length>=d&&(e.send(),a())},b.send=function(){var a=amzncsm.getPixelID(),c=(new Date).getTime(),d=amzncsm.csmReport.pq;b.firePixel('{"adCsm": '+JSON.stringify(d.queue)+', "pixelId": "'+a+'", "ts": '+c+"}")},b}),amzncsm.detectViewability=function(a,b,c,d,e){function f(){return s.beaconSent.iab&&s.beaconSent.groupm}function g(a,b){if(s.getDuration){var c=s.end-s.start;s.totalTime+=c}}function h(a){}function i(a){}function j(){if(s.beaconSent.iab!==!0)try{var a=s.detectActualDimension(s.adElementContainer),b=amzncsm.isWindowActive(s.hostDoc),c=a>=s.iabAreaCutoff-.05&&b;c&&(m("viewable",{viewable:!0,defn:"iab"}),s.beaconSent.iab=!0,k())}catch(d){amzncsm.reportClientError(d)}}function k(){f()&&amzncsm.scrollImitationTimer&&clearInterval(amzncsm.scrollImitationTimer)}function l(a,b,c,d){var e=0,f=!1;s.visibilityState=amzncsm.getVisibilityState(s.hostDoc),amzncsm.isIE()?e=s.fractionInViewportIE(a,b):amzncsm.isChrome()?e=s.fractionInViewportWebkit(a,b):amzncsm.isFirefox()?e=s.fractionInViewportFF(a,b):amzncsm.isSafari()&&(s.fractionInViewportSafari(c,d),f=!0),f===!1&&d(e)}function m(a,b){var c=(new Date).getTime();try{switch(a){case"above_the_fold":o('{"adViewability":[{"above_the_fold": '+b.atf+', "vs": "'+s.visibilityState+'", '+(null!=s.leftPos&&isNaN(s.leftPos)===!1?'"leftPos": '+s.leftPos.toFixed(2)+", ":"")+(null!=s.topPos&&isNaN(s.topPos)===!1?'"topPos": '+s.topPos.toFixed(2)+", ":"")+'"ts": '+c+', "pixelId": "'+s.pixelId+'"}]}');break;case"viewable":o('{"adViewability":[{"viewable": true ,"vs": "'+s.visibilityState+'", '+(null!=s.leftPos&&isNaN(s.leftPos)===!1?'"leftPos": '+s.leftPos.toFixed(2)+", ":"")+(null!=s.topPos&&isNaN(s.topPos)===!1?'"topPos": '+s.topPos.toFixed(2)+", ":"")+'"defn": "'+b.defn+'", "ts": '+c+', "pixelId": "'+s.pixelId+'"}]}')}}catch(d){amzncsm.reportClientError(d)}}function n(a){function b(){s.beaconSent.iab===!1&&(s.timer&&clearTimeout(s.timer),s.timer=amzncsm.setTimeout(function(){j()},s.iabTimeCutoff))}function c(){h(n),s.start=(new Date).getTime()/1e3,b(),s.timerStarted=!0}function d(){clearTimeout(s.timer),s.timerStarted=!1,s.end=(new Date).getTime()/1e3,i(n),g(f,n)}var e,f=s.adElement,n=s.adElementContainer,o=s.adID;amzncsm.resetTimer=d,a===!0?(amzncsm.isSafari()&&s.initVCompSafari(),e=function(a){var b,d=amzncsm.isWindowActive(s.hostDoc);s.area=a,s.area>s.iabAreaCutoff?(b=!0,d&&c()):b=!1,window.performance&&window.performance.mark&&"function"==typeof window.performance.mark&&(window.performance.mark("atfCompEnd"+o),window.performance.measure("atfComp"+o,"atfCompStart"+o,"atfCompEnd"+o)),m("above_the_fold",{atf:b})},window.performance&&window.performance.mark&&"function"==typeof window.performance.mark&&window.performance.mark("atfCompStart"+o),l(f,n,a,e)):(e=function(a){s.beaconSent.groupm===!1&&a>=s.groupmAreaCutoff&&(m("viewable",{viewable:!0,defn:"groupm"}),s.beaconSent.groupm=!0,k()),s.beaconSent.iab===!1&&(amzncsm.isWindowActive(s.hostDoc)&&(0==s.focused||null==s.focused)&&a>s.iabAreaCutoff&&0==s.timerStarted&&c(),amzncsm.isWindowActive(s.hostDoc)?s.focused=!0:(d(),s.focused=!1),a>=s.iabAreaCutoff&&0==s.timerStarted?c():a<s.iabAreaCutoff&&1==s.timerStarted&&d()),s.area=a},l(f,n,a,e))}function o(){var a=Array.prototype.slice.call(arguments);amzncsm.pixelQueue.firePixel.apply(amzncsm.beacon,a)}function p(a){try{s.debug&&window.console&&window.console.log(a)}catch(b){}}var q,r,s=this,t=amzncsm.isSafari()?500:1e3;return this.adElement=a,this.adElementContainer=a,this.adWidth=a.document?a.document.body.offsetWidth:a.offsetWidth,this.adHeight=a.document?a.document.body.offsetHeight:a.offsetHeight,this.instrURL=b,this.adID=e,this.getDuration=!0,this.totalTime=0,this.leftPos=null,this.topPos=null,this.start=null,this.end=null,this.area=0,this.iabAreaCutoff=.5,this.groupmAreaCutoff=.9,this.iabTimeCutoff=1e3,this.focused=null,this.timer=!1,this.timerStarted=!1,this.beaconSent={iab:!1,groupm:!1},this.hostWindow=c,this.hostDoc=d,this.pixelId=amzncsm.getPixelID(),q=null,r=0,this.adElement&&this.adElement.document&&"IFRAME"!=this.adElement.tagName&&(this.adElement=this.adElement.document.body),this.adElementContainer&&this.adElementContainer.document&&"IFRAME"!=this.adElementContainer.tagName&&(this.adElementContainer=this.adElementContainer.document.body),amzncsm.isSupportedBrowser()===!1?!1:(amzncsm.csmReport[this.adID].container=this.adElementContainer,amzncsm.csmReport[this.adID].adElement=this.adElement,this.debug=-1!==window.location.href.indexOf("csm_debug_mode"),this.profile=-1!==window.location.href.indexOf("amzn_profile_mode"),amzncsm.log=p,void(this.collectData=function(){var a,b=this;n(!0),a=function(){try{if(document.visibilityState,f()===!1&&amzncsm.isWindowActive(b.hostDoc))var a=amzncsm.setTimeout(function(){a&&clearTimeout(a),n(!1)},50);else amzncsm.resetTimer()}catch(c){amzncsm.reportClientError(c)}},amzncsm.scrollImitationTimer=amzncsm.setInterval(function(){if(amzncsm.isFirefox())(!b.oldMozInnerScreenX||!b.oldMozInnerScreenY||Math.abs(window.mozInnerScreenX-b.oldMozInnerScreenX)>10||Math.abs(window.mozInnerScreenY-b.oldMozInnerScreenY)>10)&&a(),b.oldMozInnerScreenX=window.mozInnerScreenX,b.oldMozInnerScreenY=window.mozInnerScreenY;else if(amzncsm.isIE()){var c=document.elementFromPoint(b.adWidth/2,b.adHeight/2);null!=c&&amzncsm.isWindowActive(b.hostDoc)&&a()}else amzncsm.isSafari()?a():amzncsm.isChrome()},t),amzncsm.handleVisibilityChange(this.hostWindow,a),amzncsm.addEvent(this.hostWindow,"resize",a,!1)}))},amzncsm.extend=function(a,b){for(var c in b)b.hasOwnProperty(c)&&(a.prototype[c]=b[c])},amzncsm.rmR=function(a,b){var c,d,e;try{if(amzncsm.instrURL=a,c=b,d=c.document,!a)throw amzncsm.errorCodes.MALFORMED_URL;e=function(a){var b=a.readyState;return"complete"==b},e(d)?amzncsm.rm("RTB",{e:c,i:a,w:c,d:d}):void 0===document.onreadystatechange?amzncsm.rm("RTB",{e:c,i:a,w:c,d:d}):d.onreadystatechange=function(){try{e(d)&&amzncsm.rm("RTB",{e:c,i:a,w:c,d:d})}catch(b){amzncsm.reportClientError(b)}}}catch(f){amzncsm.reportClientError(f)}},amzncsm.extend(amzncsm.detectViewability,{getIframeWindowDimension:function(a,b){var c,d,e,f,g,h=b.body,i=a.innerWidth||b.documentElement.clientWidth||h.clientWidth||640,j=a.innerHeight||b.documentElement.clientHeight||h.clientHeight||480;return window.mozInnerScreenX&&window.mozInnerScreenY&&(c=90,d=a.mozInnerScreenX,e=a.mozInnerScreenY-c-10,f=window.screen.availWidth,g=window.screen.availHeight-c,0!=d&&(0>d?(i+=d,i=Math.max(0,i)):d>f?i=0:f-d>i||(i=f-d),i=Math.min(i,f)),0!=e&&(0>e?(j+=e,j=Math.max(0,j)):g>e?g-e>j||(j=g-e+2):j=0),j=Math.min(j,g)),{width:i,height:j}},fractionInViewportIE:function(a,b){var c,d,e=a.offsetWidth,f=a.offsetHeight,g=Number.MAX_VALUE,h=Number.MAX_VALUE,i=Number.MIN_VALUE,j=Number.MIN_VALUE,k=10,l=0,m=this.getIframeWindowDimension(window,document),n=m.width,o=m.height,p=(n/k+1)*(o/k+1);for(c=0;n>=c;c+=k)for(d=0;o>=d;d+=k)elem=document.elementFromPoint(c,d),null!=elem&&(l++,g>c?g=c:c>i&&(i=c),h>d?h=d:d>j&&(j=d));return e=i-g,f=j-h,(0>=e||0>=f)&&(e=0,f=0),0!=p?l/p:0},fractionInViewportFF:function(a,b){var c,d,e,f,g,h,i,j,k,l;return window.mozInnerScreenX&&window.mozInnerScreenY?(c=this.getIframeWindowDimension(window,document),d=c.width,e=c.height,f=b.offsetWidth,g=b.offsetHeight,h=100,this.leftPos=window.mozInnerScreenX,this.topPos=window.mozInnerScreenY-h,i=f,j=g,k=this.topPos,l=this.leftPos,l>=0&&(l=a.getBoundingClientRect().left),k>=0&&(k=a.getBoundingClientRect().top),0>k&&(j+=k),k+g>e&&(j-=k+g-e),0>l&&(i+=l),l+f>d&&(i-=l+f-d),0>i&&(i=0),i>f&&(i=f),0>j&&(j=0),j>g&&(j=g),0!=g&&0!=f?i*j/(g*f):0):0},fractionInViewportWebkit:function(a,b){return amzncsm.webkitFracViewport},initVCompSafari:function(){function a(a,b){var c,d,e,f=document.createElement("IFRAME"),g='var vs = false; function step() { vs = true; }; function dv() { vs = false; window.requestAnimationFrame(step); window.setTimeout(function() { if (vs === true) { parent.postMessage(window.frameElement.id + " vs", "*"); } else { parent.postMessage(window.frameElement.id + " ivs", "*"); } }, 20); }; (function registerPostMessageHandler() { var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent"; var eventer = window[eventMethod]; var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message"; eventer(messageEvent, function(e) { var key = e.message ? "message" : "data"; var data = e[key]; if (data == "dv") { dv(); } }, false); })(); ';f.id=b,f.height=5,f.width=5,f.style.position="absolute",f.style.opacity=0;for(c in a)a.hasOwnProperty(c)&&(f.style[c]=a[c]);document.body.appendChild(f);try{d=f.contentDocument,d&&(d.open(),d.writeln("<!DOCTYPE html><html><head><title></title></head><body></body></html>"),d.close(),e=d.createElement("script"),e&&(e.type="text/javascript",e.text=g,d.body.appendChild(e)))}catch(h){amzncsm.reportClientError(h)}return f}amzncsm.safv={itrCount:0,atfPixelFired:!1},a({top:"20px",right:"20px"},"adcfTR"),a({bottom:"20px",left:"20px"},"adcfBL"),a({bottom:"20px",right:"20px"},"adcfBR"),a({top:"20px",left:"20px"},"adcfTL"),a({top:"50%",left:"50%"},"adcfCenter"),a({top:"-1000px",right:"-1000px"},"adcfInv"),amzncsm.setTimeout(function(){amzncsm.safv.atfPixelFired===!1&&(amzncsm.safv.atfPixelFired=!0,amzncsm.safv.atfSuccessCb.call(null,0))},2e3),amzncsm.registerPostMessageHandler(function(a){var b=a.split(" ");"adcfInv"==b[0]?"vs"==b[1]?(amzncsm.safv.fp=!0,amzncsm.safv.vCount=0):amzncsm.safv.fp=!1:("vs"==b[1]||"ivs"==b[1])&&"vs"==b[1]&&amzncsm.safv.fp===!1&&amzncsm.safv.vCount++,amzncsm.safv.respCount++,6==amzncsm.safv.respCount&&(amzncsm.safv.itrCount++,amzncsm.safv.fp===!1&&amzncsm.safv.itrCount>2&&(1==amzncsm.safv.atfPixelFired?amzncsm.safv.viewSuccessCb.call(null,amzncsm.safv.vCount/5):(amzncsm.safv.atfPixelFired=!0,amzncsm.safv.atfSuccessCb.call(null,amzncsm.safv.vCount/5))))})},fractionInViewportSafari:function(a,b){var c,d;for(amzncsm.safv.vCount=0,amzncsm.safv.respCount=0,amzncsm.safv.fp=!1,a?amzncsm.safv.atfSuccessCb=b:amzncsm.safv.viewSuccessCb=b,c=document.getElementsByTagName("iframe"),d=0;d<c.length;d++)/adcf/.test(c[d].id)&&c[d].contentWindow.postMessage("dv","*")},domHitTestingWithBoundary:function(a,b,c,d,e,f,g,h,i){var j,k,l,m,n,o=Number.MAX_VALUE,p=Number.MAX_VALUE,q=Number.MIN_VALUE,r=Number.MIN_VALUE,s=0,t=0;for(k=a;b>=k;k+=e)for(l=c;d>=l;l+=f)s++,j=h.elementFromPoint(k,l),found=!1,g.call(null,j)&&(t++,i===!0&&(o>k?o=k:k>q&&(q=k),p>l?p=l:l>r&&(r=l)));return m=q-o,n=r-p,(0>=m||0>=n)&&(m=0,n=0),i?{height:n,width:m}:0!=s?t/s:0},detectActualDimension:function(a){if(amzncsm.isWebkit())return 1;if(amzncsm.isIE()){var b=a.getBoundingClientRect().top,c=a.getBoundingClientRect().left,d=a.offsetWidth,e=a.offsetHeight,f=function(a){return null!=a};return this.domHitTestingWithBoundary(c,c+d,b,b+e,5,5,f,this.hostDoc,!1)}return amzncsm.isFirefox(),1}}),amzncsm=amzncsm||{},amzncsm.rm=function(){var a,b,c,d={RTB:{viewability:!0,viewDuration:!1,hoverStats:!1,pageMetrics:!1,fraudMetrics:!1},supportedBrowsers:{IE:!0,Firefox:!0,Chrome:!1,Safari:!0}};return amzncsm.config=d,a=function(a){var b,c,d,e=window.performance.getEntriesByType("measure"),f={};for(b=0;b<e.length;++b)e[b].name.endsWith(a)&&(c=e[b],d=c.name.substring(0,c.name.length-a.length),f[d]=c.duration.toFixed(2));amzncsm.pixelQueue.addPixel(JSON.stringify(f))},b=function(b,d){var e,f=d.e,g=d.i,h=d.w,i=d.d,j=Math.round(1e7*Math.random()).toString();return amzncsm.csmReport=amzncsm.csmReport||{},amzncsm.csmReport.hasOwnProperty(j)?!1:(amzncsm.csmReport[j]={},c(b,f,g,h,i,j),window.performance&&window.performance.mark&&"function"==typeof window.performance.mark&&window.performance.mark("csmStart"+j),b=b.toUpperCase(),"RTB"!=b||(amzncsm.api=b,e=new amzncsm.detectViewability(f,g,h,i,j),e.collectData&&e.collectData()),window.performance&&window.performance.mark&&"function"==typeof window.performance.mark&&(window.performance.mark("csmEnd"+j),window.performance.measure("csmTot"+j,"csmStart"+j,"csmEnd"+j),a(j)),void(amzncsm.errors.length>0&&amzncsm.reportErrors(g)))},c=function(a,b,c,e,f,g){var h,i,j,k,l,m,n,o,p;amzncsm.loadModules(g,[{name:"eventUtils",params:[]}]);for(h in amzncsm.eventUtils)amzncsm.eventUtils.hasOwnProperty(h)&&(amzncsm[h]=amzncsm.eventUtils[h]);amzncsm.loadModules(g,[{name:"utils",params:[]}]);for(h in amzncsm.utils)amzncsm.utils.hasOwnProperty(h)&&(amzncsm[h]=amzncsm.utils[h]);if(amzncsm.loadModules(g,[{name:"pixelQueue",params:[c]}]),i=-1!==e.location.href.indexOf("csm_debug_mode"),i&&-1!==window.location.href.indexOf("csm_uems")){for(j=function(b){for(var c in d[a])d[a][c]=b},k=window.location.href.split("+").join(" "),l={},n=/[?&]?([^=]+)=([^&]*)/g;m=n.exec(k);)l[decodeURIComponent(m[1])]=decodeURIComponent(m[2]);for(o=l.csm_uems.split(","),j(!1),p=0;p<o.length;p++)"vd"==o[p]?d[a].viewDuration=!0:"hs"==o[p]?d[a].hoverStats=!0:"pm"==o[p]?d[a].pageMetrics=!0:"fm"==o[p]?d[a].fraudMetrics=!0:"all"==o[p]?j(!0):"none"==o[p]}d[a].viewDuration===!0&&(amzncsm.captureViewDuration=!0,amzncsm.loadModules(g,[{name:"viewDuration",params:[]}])),d[a].hoverStats===!0&&amzncsm.loadModules(g,[{name:"hoverStats",params:[b]}]),d[a].pageMetrics===!0&&amzncsm.loadModules(g,[{name:"pageMetrics",params:[e]}]),d[a].fraudMetrics===!0&&amzncsm.loadModules(g,[{name:"fraudMetrics",params:[e]}])},b}();