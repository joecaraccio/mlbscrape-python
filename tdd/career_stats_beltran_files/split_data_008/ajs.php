(function(){
var isIE = window.navigator.userAgent.indexOf("MSIE ") > 0;
var ifr = "<"+"iframe id=\"cto_iframe_bbfc057cd2\" frameBorder=\"0\" allowtransparency=\"true\" hspace=\"0\" marginwidth=\"0\" marginheight=\"0\" scrolling=\"no\" vspace=\"0\" width=\"160px\" height=\"600px\"\n";
if(isIE && document.domain !== window.location.hostname) {
ifr += " src=\"javascript:'<script>window.onload=function(){document.write(\\\'<script>document.domain = &quot;"+document.domain + "&quot;;<\\\\/script>\\\');document.close();};</script>'\"";
}
ifr += "><"+"/iframe>\n";
document.write(ifr);
var ifc = "\n";
ifc += "<"+"!DOCTYPE html>\n";
ifc += "<"+"html>\n";
ifc += "  <"+"head>\n";
ifc += "    <"+"meta name=\"format-detection\" content=\"telephone=no\"><"+"meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge,chrome=1\">\n";
ifc += "  <"+"/head>\n";
ifc += "  <"+"body><"+"script type=\"text/javascript\" src=\"http://a516.casalemedia.com/pcreative?au=5&c=1CE91B&pcid=025C000E3900&pr=55&r=25C000E&s=28AFA&t=571D1493&u=VkY1MUljQW9JSUlBQUFZZVJuRUFBQUFL&m=20a74ee70e455a2478b01a60caf17f05&wp=1BA&cp=1.67&aid=EAEF2A61027C028C&tid=0&dm=64&n=sports-reference.com&epr=bbfc057cd2\"><"+"/script>\n";
ifc += "<"+"div id=\'beacon_bbfc057cd2\' style=\'position: absolute; left: 0px; top: 0px; visibility: hidden;\'>\n";
ifc += "<"+"img width=\"0\" height=\"0\" src=\"http://cat.ny.us.criteo.com/delivery/lg.php?cppv=1&cpp=8fvKJHxwamZmbThmNWVjSXA3aTcwUGgxcHBIcG56L015bDdhWDYvYlJZYVFtRzd4QkhNTmY4RVhpYWd3RUJxeU1EWFNqTzRGUnU3OCtDWFVtNm05OTlrZ1NHWXB5YnB0ZGlhVmVHdSt5MzBaYXUxZGRwSHRxSVlqRGpEeUhDNmZ2MFlLbGdNbUJORmFBZkhrTklJVE5GTXNkcDVGYkVuUkdlSGF6Qk5IMGVOV29DNExSNUdTZFdXSUNDVVEwWXVybVJZYzNNWnF2MlgzVGg1cWV1VDR0UlVMVjZXVmROckRVbG81eFh5am4xUU9BekRSWVZ5UVcrL0Y3M3BwVUZyU0x2U1pYfA%3D%3D\"/>\n";
ifc += "<"+"/div>\n";
ifc += "<"+"/body>\n";
ifc += "<"+"/html>\n";

var fillIframe = function(ifrd) {
    var getDocument = function(iframe) {
        var result_document = iframe.contentWindow || iframe.contentDocument;
        if (result_document && result_document.document)
            result_document = result_document.document;
        return result_document;
    };
    var c = getDocument(ifrd);
    if (c) {
        c.open();
        c.write(ifc);
        c.close();
    }
};


var maxRetryAttempts = 100;
var loaded = false;
var pollIframe = function() {
    var ifrd = document.getElementById('cto_iframe_bbfc057cd2');
    if (ifrd && isIE) {
         ifrd.onload = function() {
            if(!loaded) {
                loaded = true;
                fillIframe(ifrd);
            }
        };
    } else if (ifrd) {
        loaded = true;
        fillIframe(ifrd);
    } else if (maxRetryAttempts-- > 0) {
        setTimeout(pollIframe, 10);
    }
};pollIframe();})();
