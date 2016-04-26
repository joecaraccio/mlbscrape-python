(function(){
var isIE = window.navigator.userAgent.indexOf("MSIE ") > 0;
var ifr = "<"+"iframe id=\"cto_iframe_03c23a9c02\" frameBorder=\"0\" allowtransparency=\"true\" hspace=\"0\" marginwidth=\"0\" marginheight=\"0\" scrolling=\"no\" vspace=\"0\" width=\"160px\" height=\"600px\"\n";
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
ifc += "  <"+"body><"+"script type=\"text/javascript\" src=\"http://a560.casalemedia.com/pcreative?au=5&c=1CE91B&pcid=DCE6003E3900&pr=55&r=DCE6003E&s=28AFA&t=571CF808&u=VkY1MUljQW9JSUlBQUFZZVJuRUFBQUFL&m=059e6e3c4a8f701026abd40229c998b7&wp=1C7&cp=1.47&aid=EAEB9901186BBE42&tid=0&dm=64&n=sports-reference.com&epr=03c23a9c02\"><"+"/script>\n";
ifc += "<"+"div id=\'beacon_03c23a9c02\' style=\'position: absolute; left: 0px; top: 0px; visibility: hidden;\'>\n";
ifc += "<"+"img width=\"0\" height=\"0\" src=\"http://cat.ny.us.criteo.com/delivery/lg.php?cppv=1&cpp=8ILtlnxwamZmbThmNWVjSXA3aTcwUGgxcHBIcG56L015bDdhWDYvYlJZYVFtRzd4aTZ4TklvdEZPK2t1Y01ENkx4YWFpY25lZFdRM2c1SVRadm5qQzRCTWJhS1ZFZEVFQVl6d1h4K2diTHNLeUxLUGFOVXVRQ1Z0VVhNMElKek5WRzhSVW5mVXVnNDVsaEt2OCtkTTZad1Fpd215dXVmcVRpNDBCeCt2K3BLbC9hUElSaHBObWxIekxTSEI2UHFYMEdyOGZmOWJwaVJSOFYrenhUaEtaY3VLM0VmQnhPaldhRUNIVFNSc2NyaHBGclY1N1J2TytWZWZJK0NtRjdXTncvSEZLfA%3D%3D\"/>\n";
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
    var ifrd = document.getElementById('cto_iframe_03c23a9c02');
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
