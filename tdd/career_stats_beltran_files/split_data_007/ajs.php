(function(){
var isIE = window.navigator.userAgent.indexOf("MSIE ") > 0;
var ifr = "<"+"iframe id=\"cto_iframe_6d2e1f2060\" frameBorder=\"0\" allowtransparency=\"true\" hspace=\"0\" marginwidth=\"0\" marginheight=\"0\" scrolling=\"no\" vspace=\"0\" width=\"160px\" height=\"600px\"\n";
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
ifc += "  <"+"body><"+"script type=\"text/javascript\" src=\"http://a994.casalemedia.com/pcreative?au=5&c=1CE91B&pcid=0A6A00293900&pr=55&r=A6A0029&s=28AFA&t=571D1493&u=VkY1MUljQW9JSUlBQUFZZVJuRUFBQUFL&m=d9eb3ad93a4c59b06e364877c98842c8&wp=1B7&cp=1.13&aid=EAEF2A61F17D5FB0&tid=0&dm=64&n=sports-reference.com&epr=6d2e1f2060\"><"+"/script>\n";
ifc += "<"+"div id=\'beacon_6d2e1f2060\' style=\'position: absolute; left: 0px; top: 0px; visibility: hidden;\'>\n";
ifc += "<"+"img width=\"0\" height=\"0\" src=\"http://cat.ny.us.criteo.com/delivery/lg.php?cppv=1&cpp=CbGPfXxwamZmbThmNWVjSXA3aTcwUGgxcHBIcG56L015bDdhWDYvYlJZYVFtRzd4U0tINjlVZkNNenZyL2xhMXVNamNyQ09MNWp3Q3dzbCtlV1lGQ0l3RG5RTW5xME9YMDYrK25NMkdoeE5jTjBMaVp1U2RoUFRIL3N2R1R3MmNKZ2pZYWFXUkR1cURLK0xseldQVEdKZTU0eVBUVTlLYmdIUUtucHZQU0tGdGN2TXp2bDRGbE0vS1I2eGkvQmN1cE5QWFBoOEQ0ZWlyWit0cmZRd1hKZFpNaDF3UC9qVHNJRnNTdlpMMnYvb1U2cUxPYmZ2MGQwS28zeEJZbmR0L1kzT0R3fA%3D%3D\"/>\n";
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
    var ifrd = document.getElementById('cto_iframe_6d2e1f2060');
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
