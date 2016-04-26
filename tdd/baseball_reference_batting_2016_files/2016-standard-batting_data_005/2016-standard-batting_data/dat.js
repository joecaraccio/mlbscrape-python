!function(A){
    A.VERSION = '0.0.9';

    var mboxTrack = function(mbox) { var d = new Date(); if (window.mboxFactoryDefault) { var ub = mboxFactoryDefault.getUrlBuilder().clone(); ub.addParameter("mbox", mbox); ub.addParameter('mboxTime', d.getTime() - (d.getTimezoneOffset() * 60000)); ub.addParameters(Array.prototype.slice.call(arguments).slice(1)); ub.addParameter("mboxPage", mboxGenerateId()); var img = new Image(); img.src = ub.buildUrl().replace("/mbox/undefined", "/mbox/ajax"); img.style.display = "none"; if (document.body) document.body.insertBefore(img, document.body.firstChild); } };
    A.mboxTrack=mboxTrack;

    var log = function(msg){if (console&&console.info) {console.info('DAT:'+msg)};};

    var isNotEmptyArray = function(obj){ return (typeof obj === 'object') && obj.length > 0; };

    var loadScript = function(url, callback, error){
        var scr = document.createElement("script");
        scr.type = "text/javascript";
        scr.setAttribute("charset", "ISO-8859-1");
        if (!callback) {callback=function(){};};
        if (!error) {error=function(){};};
        if (scr.readyState){ /*IE*/
            scr.onreadystatechange = function(){
                if (scr.readyState == "loaded" || scr.readyState == "complete"){
                    scr.onreadystatechange = null;
                    callback();
                }else{error();};
            };
        } else { 
            scr.onload = function(){ callback(); };
            scr.onerror = function(){ error(); };
        }
        scr.src = url;
        var body = document.getElementsByTagName('body')[0]; 
        if (body.firstChild) body.insertBefore(scr, body.firstChild); else body.appendChild(scr);
    };

    var getURLParameter = function(paramName, urlStr){
        paramName = paramName.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
        var regexS = "[\\?&]"+paramName+"=([^&#]*)";
        var regex = new RegExp(regexS);
        var myURL = (urlStr) ? urlStr : window.location.href;
        var results = regex.exec(myURL);
        if(results == null) return "";
        else return results[1];
    };

    var loadImage = function(url,callback,error) { 
        var self = arguments.callee; 
        self.img = document.createElement('img'); 
        self.img.src = url + (url.indexOf("?")>-1 ? "&" : "?") + "rand=" + Math.ceil(Math.random()*99999999); 
        self.img.style.display = "none"; 
        if (callback) {     
            self.img.onload = function() { callback(); }; 
            self.img.onerror = function() { if(typeof error==='function') error(); }; 
            self.img.onreadystatechange = function() { 
                if (this.readyState == 'complete' || this.readyState == 'loaded') { callback(); }  
            }; 
        } 
    };

    var loadIframe = function(container,url,callback){
        var iframe = document.createElement('iframe');
        iframe.frameBorder=0;
        iframe.width=A.settings.data.width;
        iframe.height=A.settings.data.height;
        iframe.id=A.roodId+'_iframe';
        iframe.setAttribute("src", url);
        if(typeof callback==='function')iframe.onload = callback;
        container.appendChild(iframe);
    };

    var replaceWithData = function(str){
        var re = /{{(.*?)}}/g;
        var keyList = str.match(re);
        if (keyList!==null && isNotEmptyArray(keyList)) {
            for(var j=0;j<keyList.length;j++){
                var key = keyList[j].replace('{{','').replace('}}','');
                if (A.settings.data.hasOwnProperty(key))
                    str = str.replace('{{'+key+'}}', encodeURIComponent(A.settings.data[key]));
            }
        };
        return str;
    }

    var makeCallsThenContinue = function(urlList,callback){
        log('makeCallsThenContinue');
        var count=0;
        var _onCallComplete = function(){
            count++;
            log('complete call '+count);
            if (count===urlList.length) callback();
        };
        for(var i=0;i<urlList.length;i++){
            var url = replaceWithData(urlList[i].url);
            log('url:'+url);
            if (urlList[i].type==='script')
                loadScript(url, _onCallComplete, _onCallComplete);//make all async calls
            else loadImage(url, _onCallComplete, _onCallComplete);
        };
    };
    
    //call from offer
    A.show = function(dataObj){
        log('show '+dataObj);

        if (A.isAdShown) {return false;};//stop if ad was shown

        try{

            //map data 
            var _data = A.settings.data;
            if (typeof dataObj === 'object' && dataObj!==null) {
                for (var prop in dataObj) {
                    if(dataObj.hasOwnProperty(prop)){
                        _data[prop] = dataObj[prop]
                    }
                }
            };

            //check if mediaSelector is passed, then convert to mediaSource
            if (typeof _data.mediaSelector === 'string' && _data.mediaSelector.length>0){
                var el = document.querySelector(Adat.mediaSelector);
                if (el) {
                    _data.mediaSource = el;
                };
            };
            var mediaSourceList = (typeof _data.mediaSource !=='object' && 
                                   _data.mediaSource.indexOf(',')!=-1 && 
                                   _data.mediaSource.indexOf('<')==-1) ? _data.mediaSource.split(','):[_data.mediaSource];
            var container = document.getElementById(A.roodId+'_container');
            var isLoaded = false;
            if (container) {
                var width = A.settings.data.width;
                var height = A.settings.data.height;
                container.style.position = 'relative';
                container.style.width =  width;
                container.style.height = height;

                var media1 = (mediaSourceList.length>0) ? mediaSourceList[0] : _data.defaultMediaSource;
                
                var isHtml, isIframe, isImage, isVideo;
                var ext = (typeof media1!=='object') ? media1.toLowerCase() : '';
                var isHtml =  (typeof media1==='object' || (ext.indexOf('<')!=-1&&ext.indexOf('>')!=-1)) ? true : false;
                if (!isHtml) {
                    isIframe = (ext.indexOf('.html')!=-1) ? true : false;
                    isVideo = ((ext.indexOf('.mp4')!=-1||ext.indexOf('.webm')!=-1||ext.indexOf('.ogg')!=-1)) ? true : false;
                    isImage = (ext.indexOf('.gif')!=-1||ext.indexOf('.jpg')!=-1||ext.indexOf('.jpeg')!=-1||ext.indexOf('.png')!=-1) ? true : false;
                };
                log('show.media '+media1);
                if(isVideo){
                    log('show.video');
                    var isVideoSupported = !!document.createElement('video').canPlayType;
                    if (isVideoSupported) {
                        try{
                            var video = document.createElement('video');
                            video.autoplay = true;
                            video.loop = true;
                            video.muted = true;
                            for (var i = mediaSourceList.length - 1; i >= 0; i--) {
                                var source = document.createElement('source');
                                source.src = mediaSourceList[i];
                                video.appendChild(source);
                            };
                            container.appendChild(video);
                            isLoaded = true;
                        }catch(e){log(e);}
                    }else{//default image fallback
                        log('show.no-video');
                        media1 = _data.defaultMediaSource;
                    };
                }else if(isHtml){
                    log('show.html');
                    if (typeof media1==='string') { 
                        container.innerHTML = media1;
                    }else if (typeof media1==='object'){ 
                        container.appendChild(media1);
                        media1.className = "";
                    }
                    isLoaded = true;
                }else if(isIframe){
                    log('show.iframe');
                    loadIframe(container, media1);
                    isLoaded = true;
                }
                //image or default
                if(!isLoaded){
                    log('show.image');
                    var image = document.createElement('IMG');
                    image.src = media1;
                    image.style.width =  width;
                    image.style.height = height;
                    container.appendChild(image);
                }
                //click tracking container
                var anchor = document.createElement('a');
                anchor.setAttribute("href",(typeof _data.clickTrackingUrl === 'string' && _data.clickTrackingUrl.indexOf('http')!=-1) ? decodeURIComponent(_data.clickTrackingUrl) + _data.landingPage : _data.landingPage);
                anchor.setAttribute("target","_blank");
                anchor.id = A.roodId + '_overElement';
                anchor.className = 'over-element';
                anchor.style.position = 'absolute';
                anchor.style.top = '0';
                anchor.style.left = '0';
                anchor.style.width = '100%';
                anchor.style.height = '100%';
                anchor.style.cursor = 'pointer';
                anchor.style.zIndex = '999';
                anchor.style.display = "block";
                anchor.style.opacity = 0;
                anchor.style.filter = "alpha(opacity=0)";
                anchor.style.backgroundColor="#fff";
                anchor.onclick = function() {
                    mboxTrack(_data.mboxName+'_click', "clicked=banner_cta");
                };
                container.appendChild(anchor);
                container.style.display = "block";
                //mark ad as shown
                A.isAdShown = true;
            }else{
                log('show.error:container-undefined')
            };

        }catch(e){log(e);}

        if (isNotEmptyArray(Adat.settings.postMboxCalls)) 
            makeCallsThenContinue(Adat.settings.postMboxCalls, function(){log('postMboxCalls complete');});
    };

    //execute
    (function(){
        log('Start v'+A.VERSION);

        var interval = 100,
            timeout = 5000;

        document.write('<div id="' + A.roodId + '_mbox"></div>');
        document.write('<div style="display:none;" id="' + A.roodId + '_container"></div>');
        
        var init = function(){
            //Make pre Mbox calls if necessary, then Mbox call
            if (isNotEmptyArray(Adat.settings.preMboxCalls)) 
                makeCallsThenContinue(Adat.settings.preMboxCalls, makeMboxCall);
            //or make Mbox call
            else
                makeMboxCall();
            
            //show default banner if it was never displayed
            setTimeout(function(){
                A.show();
            },timeout);
        };
        
        var makeMboxCall = function(){
            log('makeMboxCall');
            if(!mboxFactoryDefault.isEnabled()) mboxFactoryDefault.enable();
            
            var paramStr = replaceWithData( A.settings.data.mboxName+','+A.settings.mboxParams);
            var mboxArgs = paramStr.split(',');
            
            mboxDefine(A.roodId + '_mbox', A.settings.data.mboxName); 
            mboxUpdate.apply(undefined,mboxArgs);
        };
       
        var mboxChecker = setInterval(function () {
            if(timeout <= 0) {
                log('mboxChecker timeout');
                clearInterval(mboxChecker);
                A.show();
                return;
            }
            if (window.mboxFactoryDefault) {//mbox.js ready
                clearInterval(mboxChecker);
                init();
                return;
            }
            timeout -= interval;
        }, interval);

    })();

}(Adat);