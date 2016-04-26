var $logOn = false;
var _container;
var _imgDir = "";
var _settings;
var _elements = [];

function log() {
	if($logOn) {
		console.log(Array.prototype.slice.call(arguments));
	}
}

HTMLElement.prototype.removeClass = function(remove) {
    var newClassName = "";
    var i;
    var classes = this.className.split(" ");
    for(i = 0; i < classes.length; i++) {
        if(classes[i] !== remove) {
            newClassName += classes[i] + " ";
        }
    }
    this.className = newClassName;
}

HTMLElement.prototype.addClass = function(add) {
    var classes = this.className.split(" ");
    for(var i = 0; i < classes.length; i++) {
        if(classes[i] === add) {
            return;
        }
    }
    this.className = this.className + " " + add;
}

function createElement(elementType, settings, parent, ignore) {
	settings = settings || {};
	settings.css = settings.css || {};
	settings.css.position = settings.css.position || "absolute";
	setDefault("alpha", 1, settings.css);
	setDefault("force3d", true, settings);
	if("bg" in settings) {
		if(settings.bg.charAt(0) == "#" || settings.bg == "transparent") {
			settings.css.backgroundColor = settings.bg;
		}
		else {
			settings.css.backgroundImage = "url("+_imgDir+settings.bg+")";
		}
	}	

	var element = document.createElement(elementType);
	TweenLite.set(element, settings);

	if(parent) {
		addChild(element, parent);
	}
	if(!ignore) {
		addElement(element, settings);
	}
	return element;
}

function addElement(elem, settings) {
	TweenLite.set(elem, settings);
	_elements.push({element:elem, settings:settings});
}

function killAllTweens() {
	var len = _elements.length;
	for(var i = 0; i < len; i++) {
		TweenLite.killTweensOf(_elements[i].element);
	}
}

function resetElements() {
	var len = _elements.length;
	for(var i = 0; i < len; i++) {
		TweenLite.set(_elements[i].element, _elements[i].settings);
	}
}

function get(id) {
	return document.getElementById(id);
}

function select(selectors) {
	return document.querySelector(selectors);
}

function listen(target, eventType, callback) {

	if(target == null || typeof(target) == 'undefined') {
		return;
	}
	if(target.addEventListener) {
		target.addEventListener(eventType, callback, false);
	}
	else if (target.attachEvent) {
		target.attachEvent("on" + eventType, callback);
	}
	else {
		target["on"+eventType] = callback;
	}
}

function unlisten(target, eventType, callback) {
	target.removeEventListener(eventType, callback);
}

function addChild(child, parent) {
	parent = parent || _container;
	parent.appendChild(child);
}

function distance(x1, y1, x2, y2) {
	return Math.sqrt(Math.pow(x2-x1, 2) + Math.pow(y2-y1, 2));
}

function init(options) {
	setDefault("maxScale", Number.MAX_VALUE, options);
	setDefault("minScale", 0, options);
	_imgDir = setDefault("imgDir", "", options);

	var winW = window.innerWidth;
	var winH = window.innerHeight;
	var scaleX = options.scaleX = 1;
	var scaleY = options.scaleY = 1;

	log("INIT!");
	log(winW, winH, options.w, options.h);

	_container = options.container = createElement("div", {attr:{class:"banner-container"}}, document.getElementsByTagName("body")[0], true);	
	_settings = options;
	return _settings;
}

function setDefault(prop, val, target) {
	if(!(prop in target)) {
		target[prop] = val;
	}
	return target[prop];
}