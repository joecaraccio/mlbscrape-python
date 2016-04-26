(function() {

    var APP = {
        init: function() {
            APP.cacheUI();
            APP.addEventListeners();
        },

        cacheUI: function() {
            APP.form = document.getElementById('scBannerForm');
            APP.input = document.getElementById('scBannerInput');
        },

        addEventListeners: function() {
            APP.form.addEventListener('submit', APP.formSubmitHandler);
			APP.input.addEventListener('keypress', APP.inputKeypressHandler);
        },

        formSubmitHandler: function(e) {
            e.preventDefault();
            var url = APP.form.action;
            var zip = APP.input.value;

            if (zip.length < 5) { return; }

			var fullURL = url + '?PerfMktgBannerZip=' + zip;
			window.open(fullURL, '_blank');
        },
		
		inputKeypressHandler: function(e) {
			if ((e.charCode >= 48 && e.charCode <= 57) || e.charCode === 0 || e.charCode == 8) {
				return true;
			} else {
				e.preventDefault();
				return false;
			}
		}
    };

    document.addEventListener('DOMContentLoaded', function(e) {
        APP.init();
    });

})();
