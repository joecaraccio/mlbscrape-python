!function(e){function n(e){var n=[];for(var i in e)e.hasOwnProperty(i)&&n.push(i);return n}function i(){var e=window.document.getElementsByTagName(h);for(var n in e)if(e[n]&&e[n].id&&e[n].id.indexOf(z)>=0)return e[n]}function t(){var e=Math.round((Date.now()-H)/1e3),i=G>=L;"undefined"==typeof f||d(A)!=d(f)?((i||!q)&&o(A),f=A,A={},B=O,C=Date.now(),E=0,q=!i):n(f).length>0&&Date.now()-C>B&&(T>E&&R>N&&(i||!q)&&(o(A),i||(q=!0)),f=A,A={},B*=D,C=Date.now(),E++,i&&(q=!1)),e>F&&(window.clearInterval(Q),window.clearInterval(K))}function o(e){var n=[],i=Math.round((Date.now()-H)/1e3);for(var t in e)e.hasOwnProperty(t)&&n.push("sL:"+i+",oV:1,"+t+",c:"+e[t]);r(M,n.join("=")),N++}function r(e,n){"undefined"!=typeof e&&"undefined"!=typeof n&&""!=n&&("https:"===location.protocol&&(e=e.replace("http:","https:")),(new Image).src=e+(e.contains("?")?"&":"?")+"d="+n+"&r="+Math.round(Math.random()*W))}function a(e){var n={};n.left=e.offsetLeft,n.top=e.offsetTop;try{"undefined"!=typeof e.offsetParent&&(n.left+=e.offsetParent.offsetLeft,n.top+=e.offsetParent.offsetTop)}catch(i){}return n}function w(e){var n={};if("undefined"==typeof window.mozInnerScreenY||"undefined"==typeof window.mozInnerScreenX)return n;var i=J?I:window.mozInnerScreenY-window.screenY,t=J?y:window.mozInnerScreenX-window.screenX,o=J?X:window.outerWidth-window.innerWidth-t,r=Y;n.isInIFrame=J,n.screenWidth=window.screen.availWidth,n.screenHeight=window.screen.availHeight,n.viewportWidth=window.outerWidth-(t+o),n.viewportHeight=window.outerHeight-(i+r),n.objWidth=e.offsetWidth,n.objHeight=e.offsetHeight,n.viewportScreenX=window.screenX+t,n.viewportScreenY=window.screenY+i,n.leftPadding=t,n.topPadding=i,n.rightPadding=o,n.bottomPadding=r,n.mozInnerScreenX=window.mozInnerScreenX,n.mozInnerScreenY=window.mozInnerScreenY;var w=a(e);return n.objScreenX=w.left+window.mozInnerScreenX-window.pageXOffset,n.objScreenY=w.top+window.mozInnerScreenY-window.pageYOffset,n.objViewableScreenX=Math.max(t,Math.max(n.objScreenX,Math.min(n.objScreenX+n.objWidth,n.viewportScreenX))),n.objViewableScreenY=Math.max(i,Math.max(n.objScreenY,Math.min(n.objScreenY+n.objHeight,n.viewportScreenY))),n.objViewableScreenX2=Math.max(n.objViewableScreenX,Math.min(n.screenWidth,Math.min(n.viewportScreenX+n.viewportWidth,n.objScreenX+n.objWidth))),n.objViewableScreenY2=Math.max(n.objViewableScreenY,Math.min(n.screenHeight,Math.min(n.viewportScreenY+n.viewportHeight,n.objScreenY+n.objHeight))),n.objViewableWidth=n.objViewableScreenX2-n.objViewableScreenX,n.objViewableHeight=n.objViewableScreenY2-n.objViewableScreenY,n.objViewableFrac=n.objViewableWidth*n.objViewableHeight/(n.objWidth*n.objHeight),n.objViewableFracX=n.objViewableWidth/n.objWidth,n.objViewableFracY=n.objViewableHeight/n.objHeight,n}function d(e){var n=[];for(var i in e)e.hasOwnProperty(i)&&"toString"!=i&&"keySet"!=i&&n.push(i);return n.join(",")}function c(e){var n=[];for(var i in e)e.hasOwnProperty(i)&&"toString"!=i&&"keySet"!=i&&n.push(i+":"+e[i]);return n.join(",")}function b(){if("undefined"!=typeof k)try{var e=w(k);if("undefined"==typeof e||"undefined"==typeof e.objViewableFrac)return;var n={};n.sW=e.screenWidth,n.sH=e.screenHeight,n.iF=e.isInIFrame,n.tP=e.topPadding,n.vX=e.viewportScreenX,n.vY=e.viewportScreenY,n.vW=e.viewportWidth,n.vH=e.viewportHeight,n.aX=e.objScreenX,n.aY=e.objScreenY,n.aW=e.objWidth,n.aH=e.objHeight,n.vP=Math.round(100*e.objViewableFrac);var i=c(n);i in A?A[i]++:A[i]=1,G=e.objViewableFrac}catch(t){}}var f,h="span",s="//www.test.com/a.gif?t=view",l=1e3,v=100,p=300,S="rfi",j=2,m=1e3,u=3,g=20,V=.5,I=119,y=11,X=41,Y=41,W=1e8,H=Date.now(),M=e&&e.viewabilityPixel?e.viewabilityPixel:s,P=e&&e.sendIntervalMillis?e.sendIntervalMillis:l,x=e&&e.checkViewabilityIntervalMillis?e.checkViewabilityIntervalMillis:v,F=e&&e.maxSecondsSinceLoad?e.maxSencondsSinceLoad:p,z=e&&e.adInstanceId?e.adInstanceId:S,T=e&&e.maxViewabilityResends?e.maxViewabilityResends:j,O=e&&e.initialTimeToResend?e.initialTimeToResend:m,D=e&&e.timeToResendFactor?e.timeToResendFactor:u,R=e&&e.maxViewabilitySends?e.maxViewabilitySends:g,L=e&&e.fracConsideredInView?e.fracConsideredInView:V,k=i(),C=0,B=O,E=0,N=0,q=!1,A={},G=-1,J=window.top!==window.self,K=window.setInterval(b,x),Q=window.setInterval(t,P)}(viewabilityOptions);
