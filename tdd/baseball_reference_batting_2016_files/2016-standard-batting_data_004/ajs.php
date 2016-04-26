(function(){
var isIE = window.navigator.userAgent.indexOf("MSIE ") > 0;
var ifr = "<"+"iframe id=\"cto_iframe_4425e4c02e\" frameBorder=\"0\" allowtransparency=\"true\" hspace=\"0\" marginwidth=\"0\" marginheight=\"0\" scrolling=\"no\" vspace=\"0\" width=\"160px\" height=\"600px\"\n";
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
ifc += "  <"+"body><"+"script type=\"text/javascript\" src=\"http://a494.casalemedia.com/pcreative?au=5&c=6C0994&pcid=15CC00092700&pr=55&r=15CC0009&s=28AFA&t=571B93F9&u=VkY1MUljQW9JSUlBQUFZZVJuRUFBQUFL&m=40774619204061630dce267adfdb3994&wp=144&cp=1.13&aid=EABF1720F70A9E32&tid=0&dm=64&n=sports-reference.com&epr=4425e4c02e\"><"+"/script>\n";
ifc += "<"+"div id=\'beacon_4425e4c02e\' style=\'position: absolute; left: 0px; top: 0px; visibility: hidden;\'>\n";
ifc += "<"+"img width=\"0\" height=\"0\" src=\"http://cat.ny.us.criteo.com/delivery/lg.php?cppv=1&cpp=y5lmC3xwamZmbThmNWVjSXA3aTcwUGgxcHBIcG56L015bDdhWDYvYlJZYVFtRzd4RzB4bllFV0x5b09MdHEweW1UaWNra3JPMnZLVGloa3JsaUhkczJYYVFCN2p6K0ZYTC9nQVVpcGpaWEE4dXZsK2dleUdqdWozWVpKK1J1dWlSK3VINmpvVlNLVWNkV3dxYkt6MjlwK2tZeHNrWUY1UG44UW1SU2RuYklmTFo0SWd1anU4VUZ0MTkrWGxiMUlnTXZpRnN0dWl2TElVZ1dSQk1CU0o4N0w0MjgxQ3F3N0xONDdTTmtTbXNwTU1CL21KR252QmcyYXFCT2ZBY2t1TlhmQ2M0fA%3D%3D\"/>\n";
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
    var ifrd = document.getElementById('cto_iframe_4425e4c02e');
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
