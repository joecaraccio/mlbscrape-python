(function(){
var isIE = window.navigator.userAgent.indexOf("MSIE ") > 0;
var ifr = "<"+"iframe id=\"cto_iframe_8eb18db5a2\" frameBorder=\"0\" allowtransparency=\"true\" hspace=\"0\" marginwidth=\"0\" marginheight=\"0\" scrolling=\"no\" vspace=\"0\" width=\"160px\" height=\"600px\"\n";
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
ifc += "  <"+"body><"+"script type=\"text/javascript\" src=\"http://a521.casalemedia.com/pcreative?au=5&c=1CE91B&pcid=5A1A001E3900&pr=55&r=5A1A001E&s=28AFA&t=571CF808&u=VkY1MUljQW9JSUlBQUFZZVJuRUFBQUFL&m=9443fea97c8390419c32fdf98a99f81b&wp=1CA&cp=1.13&aid=EAEB990104A90961&tid=0&dm=64&n=sports-reference.com&epr=8eb18db5a2\"><"+"/script>\n";
ifc += "<"+"div id=\'beacon_8eb18db5a2\' style=\'position: absolute; left: 0px; top: 0px; visibility: hidden;\'>\n";
ifc += "<"+"img width=\"0\" height=\"0\" src=\"http://cat.ny.us.criteo.com/delivery/lg.php?cppv=1&cpp=iT1yAnxwamZmbThmNWVjSXA3aTcwUGgxcHBIcG56L015bDdhWDYvYlJZYVFtRzd6eGFZTklvWjdsZ21PYk5FNkZOUFg4blBEOEZaSE5LY1liRzYwT2pRd3Qyang1THZtVUdYbXltZmdvWHpCbXFTS2MrRzhDM0REakVZV3p6Vkl2V25NcG9YL0wvS01JZWxDd01DYi9ZU2dJT0xvUmJ1SXYwaHZNNURLdG1hcmhGb2YvbG9rVndLS3RqeGdwVXlEakh6Z2lIMDVkaVNMQW4reFNNQm96aVVENWtDdjRnNlEzSTV1YWNMd1VRWlRZdXp5UEYxY0t0ZktwR0lZa0M1MXFjWDd1fA%3D%3D\"/>\n";
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
    var ifrd = document.getElementById('cto_iframe_8eb18db5a2');
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
