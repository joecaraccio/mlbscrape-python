(function(){
var s = "<"+"div class=\"adiply_ad_holder\" style=\"width:160px;height:600px;margin:0;padding:0\">\n";
s += "<"+"/div>\n";
s += "<"+"script type=\"text/javascript\">\n";
s += "var adiply_divs = document.getElementsByClassName(\"adiply_ad_holder\");\n";
s += "var adiply_final_div_id = \"adiply_ad_holder_\" + Math.floor((Math.random() * 100000) + 1);\n";
s += "for(var i=0;i<"+"adiply_divs.length; i++){\n";
s += "     if(adiply_divs[i].id) continue;\n";
s += "     adiply_divs[i].setAttribute(\"id\", adiply_final_div_id);\n";
s += "     break;\n";
s += "}\n";
s += "\n";
s += "  var OX_ads = OX_ads || [];\n";
s += "  OX_ads.push({\n";
s += "     slot_id: adiply_final_div_id,\n";
s += "     auid: \"537209676\"\n";
s += "  });\n";
s += "<"+"/script>\n";
s += "<"+"script type=\"text/javascript\" src=\"http://us-ads.openx.net/w/1.0/jstag\"><"+"/script>\n";
s += "<"+"div id=\'beacon_46202733f5\' style=\'position: absolute; left: 0px; top: 0px; visibility: hidden;\'>\n";
s += "<"+"img width=\"0\" height=\"0\" src=\"http://cat.ny.us.criteo.com/delivery/lg.php?cppv=1&cpp=%2FWE4H3xUNlJ3N3JnWmpZUm9Uc2xhVWdyWWhxWUJXK21lci9haWlpSEFJYWM3Ymgxa1VlT00zeHQrY0ZWajJaMXQzOFN6TS9vZDNIMmp0TmRUUFAxQmNrUG9ZUzJ6ZjFQcGdEMWphRzk5Q2xCaHQ0RWozbzlvclNSZDhROEJBWDFmUXpVNjJuUnBuNW9ldTVjRCtGNHpmZ0ZidUMvdmhTeFgwaFNEblNOUDc1bEttNFROVUU2RTJhdElVamZ1dTlXa01PcWpvMHpjT3pTdTBGZTc0eHQ4YzBsWk9CZXROSEVsWVV0ZUYzYk5vY25xR284PXw%3D\"/>\n";
s += "<"+"/div>\n";
s += "\n";
document.write(s);})();
