$(document).ready(function(){

	var device = navigator.userAgent.toLowerCase();
	var ios = device.match(/(iphone|ipod|ipad)/);

	// Player Search Autocomplete Handler (uses JS from old version of the site)
	$(document).on('keyup','.psearchinput',function() {
		sport = $(this).data('sport');
		searchstring = $(this).val();
		$('.psearchinput').each(function() {
			$('#mainPlayerSearch').show();
			autoCompleteSearch(searchstring, sport);
		});
	});

	// Close Player Search AutoComplete
	$(document).on('click','#closePlayerSearch',function(e) {
		e.preventDefault();
		$('#mainPlayerSearch').hide();
	});

	// Allows placeholder tags to be used and work with IE
	$('input, textarea').placeholder();

	if (!(ios)) {
		// Controls the hover effect on the home page navigation
		$('.navsectiontop').hover(
			function(){
				$(this).addClass('nsthover');
				$(this).find('.longnavtitle').show();
				$(this).find('.navicon').hide();
				$(this).find('.naviconhover').show();
			},
			function(){
				$(this).removeClass('nsthover');
				$(this).find('.longnavtitle').hide();
				$(this).find('.navicon').show();
				$(this).find('.naviconhover').hide();
			}
		);

		// Controls the hover effect on the small secondary sports
		$('.thinnav').hover(
			function(){
				$(this).addClass('thinnavhover');
				$(this).find('.thinnavicon').hide();
				$(this).find('.thinnaviconhover').show();
			},
			function(){
				$(this).removeClass('thinnavhover');
				$(this).find('.thinnavicon').show();
				$(this).find('.thinnaviconhover').hide();
			}
		);

		// Controls the hover effect on the top right nav button

		$('.captionwrap').hover(
			function(){
				$(this).addClass('opacity90');
			},
			function(){
				$(this).removeClass('opacity90');
			}
		);

		$('.toptenbox').hover(
			function(){
				$(this).addClass('toptenhighlight');
			},
			function(){
				$(this).removeClass('toptenhighlight');
			}
		);

		$('.toparticle').hover(
			function(){
				$(this).addClass('toptenhighlight');
			},
			function(){
				$(this).removeClass('toptenhighlight');
			}
		);

		$('.mega-row').hover(
			function(){
				$(this).addClass('highlight');
			},
			function(){
				$(this).removeClass('highlight');
			}
		);

		$(document).on("mouseenter mouseleave", ".story-row", function() {
			$(this).toggleClass('highlight');
		});

		$(document).on("click", ".compranks-biolink", function() {
			$(this).parent().nextAll('.compranks-bio').first().toggle();
		});

	}

	// Helps prevent orphans in headlines
	$(".mega-article a").each(function() {
	        var wordArray = $(this).text().split(" ");
	        wordArray[wordArray.length-2] += "&nbsp;" + wordArray[wordArray.length-1];
	        wordArray.pop();
	        $(this).html(wordArray.join(" "));
	});

	// Helps prevent orphans in headlines
	$(".article-headline h1").each(function() {
	        var wordArray = $(this).text().split(" ");
	        wordArray[wordArray.length-2] += "&nbsp;" + wordArray[wordArray.length-1];
	        wordArray.pop();
	        $(this).html(wordArray.join(" "));
	});

	// Helps prevent orphans in headlines
	$(".hlinestory a").each(function() {
	        var wordArray = $(this).text().split(" ");
	        wordArray[wordArray.length-2] += "&nbsp;" + wordArray[wordArray.length-1];
	        wordArray.pop();
	        $(this).html(wordArray.join(" "));
	});

	// Enables tablesorter for any table with this class
	$(".makesortable").tablesorter({ sortInitialOrder: 'desc' });

	// Enables tablesorter for any table with this class (intended for article tables)
	$(".articlesort").tablesorter({ sortInitialOrder: 'desc' });

	// Enables sorting on projections table
	$(".projections-table").tablesorter({ sortInitialOrder: 'desc' });

	// Enables tablesorter for any table with this class
	$(".optimizer-sticky").tablesorter({
		sortInitialOrder: 'desc',
		widgets: [ 'stickyHeaders' ],
		widgetOptions: {
			stickyHeaders_attachTo : '#lineupopt-poolbox'
    	}
    });

	// Enables tablesorter for any table with this class
	$(".rwo-sticky").tablesorter({
		sortInitialOrder: 'desc',
		widgets: [ 'stickyHeaders' ],
		widgetOptions: {
			stickyHeaders_attachTo : '#rwo-poolbox'
    	}
    });
	// same as rwo-sticky - for daily trends page
    $(".trends-sticky").tablesorter({
		sortInitialOrder: 'desc',
		widgets: [ 'stickyHeaders' ],
		widgetOptions: {
			stickyHeaders_attachTo : '#trends-poolbox'
    	}
    });

    	// same as rwo-sticky - for daily trends page
    $(".trends-sticky2").tablesorter({
		sortInitialOrder: 'desc',
		widgets: [ 'stickyHeaders' ],
		widgetOptions: {
			stickyHeaders_attachTo : '#trends-poolbox2'
    	}
    });

	// Enables tablesorter on the MLB player pages and sub-pages and sets the sorting to descending by default
	$(".basicstats").tablesorter({ sortInitialOrder: 'desc' });
	$(".advancedstats").tablesorter({ sortInitialOrder: 'desc' });
	$(".careerstats").tablesorter({ sortInitialOrder: 'desc' });

	$(".headerfollows").tablesorter({ sortInitialOrder: 'desc', stringTo: 'min', emptyTo: 'emptyMin', widgets: ["stickyHeaders"] });
	$(".headerfollowsAsc").tablesorter({ sortInitialOrder: 'asc', stringTo: 'min', emptyTo: 'emptyMin', widgets: ["stickyHeaders"] });

	// BASIC STATS: Show/Hide Minor League Stats on MLB Player Pages
	$('.show-minors').click(function(event) {
		event.preventDefault();
		$('.statrow-minors').show();
		$(this).hide();
		$('.hide-minors').show();
	});

	$('.hide-minors').click(function(event) {
		event.preventDefault();
		$('.statrow-minors').hide();
		$(this).hide();
		$('.show-minors').show();
	});

	// BASIC STATS: Show/Hide Partial Seasons on MLB Player Pages
	$('.show-partial').click(function(event) {
		event.preventDefault();
		$('.partial').show();
		$('.show-partial').hide();
		$('.hide-partial').show();
	});

	$('.hide-partial').click(function(event) {
		event.preventDefault();
		$('.partial').hide();
		$('.hide-partial').hide();
		$('.show-partial').show();
	});

	// ADVANCED STATS: Show/Hide Partial Seasons on MLB Player Pages
	$('.show-partialadv').click(function(event) {
		event.preventDefault();
		$('.partialadv').show();
		$(this).hide();
		$('.hide-partialadv').show();
	});

	$('.hide-partialadv').click(function(event) {
		event.preventDefault();
		$('.partialadv').hide();
		$(this).hide();
		$('.show-partialadv').show();
	});

	// ADVANCED STATS: Show/Hide Minor League Stats on MLB Player Pages
	$('.show-minorsadv').click(function(event) {
		event.preventDefault();
		$('.statrow-minorsadv').show();
		$(this).hide();
		$('.hide-minorsadv').show();
	});

	$('.hide-minorsadv').click(function(event) {
		event.preventDefault();
		$('.statrow-minorsadv').hide();
		$(this).hide();
		$('.show-minorsadv').show();
	});


	// Show/Hide 5x5 Stats on MLB Player Pages
	$('.show-fivebyfive').click(function(event) {
		event.preventDefault();
		$('.statcolumn-optional').hide();
		$('.fivebyfive-border').css("border-left","1px solid #bbbbbb");
		$(this).hide();
		$('.hide-fivebyfive').show();
	});

	$('.hide-fivebyfive').click(function(event) {
		event.preventDefault();
		$('.statcolumn-optional').show();
		$('.fivebyfive-border').css("border-left","0px");
		$(this).hide();
		$('.show-fivebyfive').show();
	});

	// BASIC STATS: For baseball players with no major league stats, trigger a click to show the minor league stats and hides the option to hide minor league stats
	if($('.showminorsflag').text() == "Yes") {
		$('.show-minors').trigger('click');
		$('.hide-minors').hide();
		$('.show-eligiblepos').hide();
	}

	// BASIC STATS: For baseball players with less than four years of major league experience, trigger a click to show the minor league stats
	if($('.showminorsyearsflag').text() == "Yes") {
		$('.show-minors').trigger('click');
	}

	// ADVANCED STATS: For baseball players with no major league stats, trigger a click to show the minor league stats and hides the option to hide minor league stats
	if($('.showminorsadvflag').text() == "Yes") {
		$('.show-minorsadv').trigger('click');
		$('.hide-minorsadv').hide();
	}

	// ADVANCED STATS: For baseball players with less than four years of major league experience, trigger a click to show the minor league stats
	if($('.showminorsyearsadvflag').text() == "Yes") {
		$('.show-minorsadv').trigger('click');
	}

	if($('.partialyearsflag').text() == "No") {
		$('.show-partial').hide();
		$('.show-partialadv').hide();
	}

	// BATTER GAME LOGS: Choose # of Days on MLB Player Pages
	$('.show-7days').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.show-7days-sel').show();
		$('.show-14days').show();
		$('.show-30days').show();
		$('.show-14days-sel').hide();
		$('.show-30days-sel').hide();
		$('.gl7').show();
		$('.gl14').hide();
		$('.gl30').hide();
	});

	$('.show-14days').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.show-14days-sel').show();
		$('.show-7days').show();
		$('.show-30days').show();
		$('.show-7days-sel').hide();
		$('.show-30days-sel').hide();
		$('.gl7').show();
		$('.gl14').show();
		$('.gl30').hide();
	});

	$('.show-30days').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.show-30days-sel').show();
		$('.show-7days').show();
		$('.show-14days').show();
		$('.show-7days-sel').hide();
		$('.show-14days-sel').hide();
		$('.gl7').show();
		$('.gl14').show();
		$('.gl30').show();
	});

	// BATTER GAME LOGS: Choose # of Days on MLB Player Pages
	$('.show-p14days').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.show-p14days-sel').show();
		$('.show-p30days').show();
		$('.show-p60days').show();
		$('.show-p30days-sel').hide();
		$('.show-p60days-sel').hide();
		$('.gl14p').show();
		$('.gl30p').hide();
		$('.gl60p').hide();
	});

	$('.show-p30days').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.show-p30days-sel').show();
		$('.show-p14days').show();
		$('.show-p60days').show();
		$('.show-p14days-sel').hide();
		$('.show-p60days-sel').hide();
		$('.gl14p').show();
		$('.gl30p').show();
		$('.gl60p').hide();
	});

	$('.show-p60days').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.show-p60days-sel').show();
		$('.show-p14days').show();
		$('.show-p30days').show();
		$('.show-p14days-sel').hide();
		$('.show-p30days-sel').hide();
		$('.gl14p').show();
		$('.gl30p').show();
		$('.gl60p').show();
	});

	// Shows/Hides the contract information on MLB player pages
	$('.showcontract').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.hidecontract').show();
		$('.mlb-player-contractbox').show();
	});

	$('.hidecontract').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.showcontract').show();
		$('.mlb-player-contractbox').hide();
	});

	// Partial Seasons - Basic Stats
	$('.partial').each(function() {
		$(this).prev("tr").addClass("partial");
	});

	$('.partial').hide();

	// Partial Seasons - Advanced Stats
	$('.partialadv').each(function() {
		$(this).prev("tr").addClass("partialadv");
	});

	$('.partialadv').hide();


	// Shows the ADP Round calculation popover
	$('.adprounds').popover({ delay: { show: 300, hide: 100 }});

	// Sorts the worst pitcher matchups by OPS ascending
    $(".bestpitchmatch").tablesorter({
        sortList: [[11,0],[2,1],[7,1]],
        headers: {
            1: { sorter: false },
            3: { sorter: false },
            4: { sorter: false },
            5: { sorter: false },
            6: { sorter: false },
            8: { sorter: false },
            9: { sorter: false },
            10: { sorter: false }
        }
    });

	// Sorts the worst batter matchups by OPS ascending
    $(".worstbatmatch").tablesorter({
        sortList: [[11,0],[2,1],[7,1]],
        headers: {
            1: { sorter: false },
            3: { sorter: false },
            4: { sorter: false },
            5: { sorter: false },
            6: { sorter: false },
            8: { sorter: false },
            9: { sorter: false },
            10: { sorter: false }
        }
    });

    // Stat Explanations on MLB Player Pages
    $('.statbd-explain[rel=popover]').popover({ delay: { show: 500, hide: 100 }});

	// General popover
	$('body').popover({
		selector: 'span[rel=popover]',
		trigger: 'hover',
		delay: { show: 500, hide: 100 }
	});

	// NFL DOLLAR VALUES POSITION FILTER
	$('.dvalues-ALLFB-dvplink').click(function(event) {
		event.preventDefault();
		$('p[class*="dvpselected"]').hide();
		$('p[class*="dvplink"]').show();
		$('.nflposrank').hide();
		$(this).hide();
		$('.dvalues-ALLFB-dvpselected').show();
		$('tr[class*="dvprow"]').show();
		$('.dvalues-posname').text("Overall");
	});

	$('.dvalues-QB-dvplink').click(function(event) {
		event.preventDefault();
		$('p[class*="dvpselected"]').hide();
		$('p[class*="dvplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.dvalues-QB-dvpselected').show();
		$('tr[class*="dvprow"]').hide();
		$('.dvalues-dvprow-QB').show();
		$('.dvalues-posname').text("Quarterbacks");
	});

	$('.dvalues-RB-dvplink').click(function(event) {
		event.preventDefault();
		$('p[class*="dvpselected"]').hide();
		$('p[class*="dvplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.dvalues-RB-dvpselected').show();
		$('tr[class*="dvprow"]').hide();
		$('.dvalues-dvprow-RB').show();
		$('.dvalues-posname').text("Running Backs");
	});

	$('.dvalues-WR-dvplink').click(function(event) {
		event.preventDefault();
		$('p[class*="dvpselected"]').hide();
		$('p[class*="dvplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.dvalues-WR-dvpselected').show();
		$('tr[class*="dvprow"]').hide();
		$('.dvalues-dvprow-WR').show();
		$('.dvalues-posname').text("Wide Receivers");
	});

	$('.dvalues-TE-dvplink').click(function(event) {
		event.preventDefault();
		$('p[class*="dvpselected"]').hide();
		$('p[class*="dvplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.dvalues-TE-dvpselected').show();
		$('tr[class*="dvprow"]').hide();
		$('.dvalues-dvprow-TE').show();
		$('.dvalues-posname').text("Tight Ends");
	});

	$('.dvalues-K-dvplink').click(function(event) {
		event.preventDefault();
		$('p[class*="dvpselected"]').hide();
		$('p[class*="dvplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.dvalues-K-dvpselected').show();
		$('tr[class*="dvprow"]').hide();
		$('.dvalues-dvprow-K').show();
		$('.dvalues-posname').text("Kickers");
	});

	$('.dvalues-ALLFBD-dvplink').click(function(event) {
		event.preventDefault();
		$('p[class*="dvpselected"]').hide();
		$('p[class*="dvplink"]').show();
		$('.nflposrank').hide();
		$(this).hide();
		$('.dvalues-ALLFBD-dvpselected').show();
		$('tr[class*="dvprow"]').show();
		$('.dvalues-posname').text("Overall");
	});

	$('.dvalues-DL-dvplink').click(function(event) {
		event.preventDefault();
		$('p[class*="dvpselected"]').hide();
		$('p[class*="dvplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.dvalues-DL-dvpselected').show();
		$('tr[class*="dvprow"]').hide();
		$('.dvalues-dvprow-DL').show();
		$('.dvalues-posname').text("Defensive Linemen");
	});

	$('.dvalues-LB-dvplink').click(function(event) {
		event.preventDefault();
		$('p[class*="dvpselected"]').hide();
		$('p[class*="dvplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.dvalues-LB-dvpselected').show();
		$('tr[class*="dvprow"]').hide();
		$('.dvalues-dvprow-LB').show();
		$('.dvalues-posname').text("Linebackers");
	});

	$('.dvalues-DB-dvplink').click(function(event) {
		event.preventDefault();
		$('p[class*="dvpselected"]').hide();
		$('p[class*="dvplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.dvalues-DB-dvpselected').show();
		$('tr[class*="dvprow"]').hide();
		$('.dvalues-dvprow-DB').show();
		$('.dvalues-posname').text("Defensive Backs");
	});

	// NFL CUSTOM RANKINGS POSITION FILTER
	$('.custnflrank-ALLFB-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.nflposrank').hide();
		$(this).hide();
		$('.custnflrank-ALLFB-crpselected').show();
		$('tr[class*="crprow"]').show();
		$('.custnflrank-crprow-K').hide();
		$('.custrank-overallcolhead').show();
		$('.custrank-overallcol').show();
		$('.custnflrank-posname').text("Overall");
	});

	$('.custnflrank-QB-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.custnflrank-QB-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custnflrank-crprow-QB').show();
		$('.custrank-overallcolhead').show();
		$('.custrank-overallcol').show();
		$('.custnflrank-posname').text("Quarterbacks");
	});

	$('.custnflrank-RB-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.custnflrank-RB-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custnflrank-crprow-RB').show();
		$('.custrank-overallcolhead').show();
		$('.custrank-overallcol').show();
		$('.custnflrank-posname').text("Running Backs");
	});

	$('.custnflrank-WR-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.custnflrank-WR-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custnflrank-crprow-WR').show();
		$('.custrank-overallcolhead').show();
		$('.custrank-overallcol').show();
		$('.custnflrank-posname').text("Wide Receivers");
	});

	$('.custnflrank-TE-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.custnflrank-TE-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custnflrank-crprow-TE').show();
		$('.custrank-overallcolhead').show();
		$('.custrank-overallcol').show();
		$('.custnflrank-posname').text("Tight Ends");
	});

	$('.custnflrank-K-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.nflposrank').show();
		$(this).hide();
		$('.custnflrank-K-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custnflrank-crprow-K').show();
		$('.custrank-overallcolhead').hide();
		$('.custrank-overallcol').hide();
		$('.custnflrank-posname').text("Kickers");
	});

	// NHL CUSTOM RANKINGS POSITION FILTER
	$('.custranks-NHL-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.custranks-indivposrank').show();
		$('.custranks-groupposrank').hide();
		$('.nhlposrank').hide();
		$('.custrank-poscolumn').show();
		$(this).hide();
		$('.custranks-NHL-crpselected').show();
		$('tr[class*="crprow"]').show();
		$('.custranks-posname').text("Overall");
	});

	$('.custranks-NHLC-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.custranks-indivposrank').show();
		$('.custranks-groupposrank').hide();
		$('.nhlposrank').show();
		$('.custrank-poscolumn').hide();
		$(this).hide();
		$('.custranks-NHLC-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custranks-crprow-C').show();
		$('.custranks-posname').text("Centers");
	});

	$('.custranks-NHLLW-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.custranks-indivposrank').show();
		$('.custranks-groupposrank').hide();
		$('.nhlposrank').show();
		$('.custrank-poscolumn').hide();
		$(this).hide();
		$('.custranks-NHLLW-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custranks-crprow-LW').show();
		$('.custranks-posname').text("Left Wings");
	});

	$('.custranks-NHLRW-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.custranks-indivposrank').show();
		$('.custranks-groupposrank').hide();
		$('.nhlposrank').show();
		$('.custrank-poscolumn').hide();
		$(this).hide();
		$('.custranks-NHLRW-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custranks-crprow-RW').show();
		$('.custranks-posname').text("Right Wings");
	});

	$('.custranks-NHLD-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.custranks-indivposrank').show();
		$('.custranks-groupposrank').hide();
		$('.nhlposrank').show();
		$('.custrank-poscolumn').hide();
		$(this).hide();
		$('.custranks-NHLD-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custranks-crprow-D').show();
		$('.custranks-posname').text("Defensemen");
	});

	$('.custranks-NHLG-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.custranks-indivposrank').show();
		$('.custranks-groupposrank').hide();
		$('.nhlposrank').show();
		$('.custrank-poscolumn').hide();
		$(this).hide();
		$('.custranks-NHLG-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custranks-crprow-G').show();
		$('.custranks-posname').text("Goalies");
	});

	$('.custranks-NHLF-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$('.custranks-indivposrank').hide();
		$('.custranks-groupposrank').show();
		$('.nhlposrank').show();
		$('.custrank-poscolumn').show();
		$(this).hide();
		$('.custranks-NHLF-crpselected').show();
		$('tr[class*="crprow"]').hide();
		$('.custranks-crprow-C').show();
		$('.custranks-crprow-LW').show();
		$('.custranks-crprow-RW').show();
		$('.custranks-posname').text("Forwards");
	});

	$('.custranks-NHLSK-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$(this).hide();
		$('.custranks-NHLSK-crpselected').show();
		$('.custranks-posname').text("Skater");
		$('.custranks-goalies').hide();
		$('.custranks-skaters').show();
	});

	$('.custranks-NHLGOAL-crplink').click(function(event) {
		event.preventDefault();
		$('p[class*="crpselected"]').hide();
		$('p[class*="crplink"]').show();
		$(this).hide();
		$('.custranks-NHLGOAL-crpselected').show();
		$('.custranks-posname').text("Goalie");
		$('.custranks-skaters').hide();
		$('.custranks-goalies').show();
	});

	$('.mlbinj-morereturns-button').click(function(event) {
		$(this).parents("table.mlbinj-retsoon").css("margin-bottom","5px");
		$('.mlbinj-morereturns-button').hide();
		$('.mlbinj-morereturns-gap').hide();
		$('.mlbinj-morereturns').show();
	});

	$('.mlbdepth-injbutton').click(function(event) {
		$('.mlbdepth-out').toggle();
	});

	// Show/hide position and team filters on NFL news pages
	$('.nflnews-bypos').click(function(event) {
		event.preventDefault();
		$('.nflnews-bypos-filter').toggle();
		$('.nflnews-byteam-filter').hide();
	});

	$('.nflnews-byteam').click(function(event) {
		event.preventDefault();
		$('.nflnews-byteam-filter').toggle();
		$('.nflnews-bypos-filter').hide();
	});

	$('.footballcs-expandbtn').click(function(event) {
		event.preventDefault();
		$('.footballcs-expandbtn').hide();
		$('.footballcs-hiddenrow').show();
		$('.footballcs-compressbtn').show();
	});

	$('.footballcs-compressbtn').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.footballcs-hiddenrow').hide();
		$('.footballcs-expandbtn').show();
	});

	// PLAYER PAGE: Show/Hide Playoff Stats
	$('.show-playoffs').click(function(event) {
		event.preventDefault();
		$('.playoff-gamestats').show();
		$(this).hide();
		$('.hide-playoffs').show();
	});

	$('.hide-playoffs').click(function(event) {
		event.preventDefault();
		$('.playoff-gamestats').hide();
		$(this).hide();
		$('.show-playoffs').show();
	});

    // Controls expandable player outlooks on player pages
	$('.expandable-player-outlooktext').show().truncate({maxLength: 420});
	$('.expandable-outlook-placeholder').hide();

    // Controls expandable author bios on article pages
	$('.authorbio p').show().truncate({maxLength: 110});

	$('.view-first-series').click(function(event) {
		event.preventDefault();
		$('.second-racing-series').hide();
		$('.first-racing-series').show();
	});

	$('.view-second-series').click(function(event) {
		event.preventDefault();
		$('.first-racing-series').hide();
		$('.second-racing-series').show();
	});

	$('.nflinj-showmore').click(function(event) {
		event.preventDefault();
		$(this).closest('.nflinj-teams').find(".nflinj-nonskill").show();
		$(this).hide();
	});

	$('.nhlplayer-gamelogtable').click(function() {
		$('.nhlplayer-moregamelog').remove();
		$('.nhlplayer-pastgamelog').show();
		$('.nhlplayer-gamelog').attr("style","height:auto");
		$(this).trigger('update');
	});

	$('.nbaplayer-gamelogtable').click(function() {
		$('.nbaplayer-moregamelog').remove();
		$('.nbaplayer-pastgamelog').show();
		$('.nbaplayer-gamelog').attr("style","height:auto");
		$(this).trigger('update');
	});

	$('.pgaplayer-gamelogtable').click(function() {
		$('.pgaplayer-moregamelog').remove();
		$('.pgaplayer-pastgamelog').show();
		$('.pgaplayer-gamelog').attr("style","height:auto");
		$(this).trigger('update');
	});

	$('.cbbplayer-gamelogtable').click(function() {
		$('.cbbplayer-moregamelog').remove();
		$('.cbbplayer-pastgamelog').show();
		$('.cbbplayer-gamelog').attr("style","height:auto");
		$(this).trigger('update');
	});

	$('.mlb-player-dcshowmore').click(function() {
		$(this).parents('.mlb-player-dcpos').find('.mlb-player-dcextra').show();
		$(this).hide();
		$('.mlb-player-dcbox').attr("style","min-height:600px;height:auto;");
		$('.mlb-player-dc').attr("style","min-height:600px;height:auto;");
	});

	// Datepickers for start and end dates
	$('#dpstart').datepicker({
		format: 'mm/dd/yyyy'
	});

	$('#dpend').datepicker({
		format: 'mm/dd/yyyy'
	});

	$('.bcpr-batterlink').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.bcpr-batterlink-sel').show();
		$('.bcpr-pitcherlink-sel').hide();
		$('.bcpr-pitcherlink').show();
		$('.bcpr-pitchers').hide();
		$('.bcpr-batters').show();
	});

	$('.bcpr-pitcherlink').click(function(event) {
		event.preventDefault();
		$(this).hide();
		$('.bcpr-pitcherlink-sel').show();
		$('.bcpr-batterlink-sel').hide();
		$('.bcpr-batterlink').show();
		$('.bcpr-batters').hide();
		$('.bcpr-pitchers').show();
	});

	$('.dfr-togglekey').click(function(event) {
		$('.dfr-statkey').toggle();
		$(this).text(function(i, text){
          return text === "Show Stat Explanations" ? "Hide Stat Explanations" : "Show Stat Explanations";
		});
    });

    $(document).on('click', '.toggle-element', function() {
    	var $togglelink = $(this);
    	var targetel = $togglelink.data('targetel');

    	var othertext = $togglelink.data('othertext');
    	var buttontext = $togglelink.text();
    	var isOthertext = (othertext) ? true : false ;

    	$('#' + targetel).toggleClass('hide');

    	if (isOthertext){
    		$togglelink.text(othertext);
    		$togglelink.data('othertext', buttontext);
    	}
    });

	$('.team-row-filter-btn').click(function(event) {
		event.preventDefault();
		$('.team-row-filter').toggle();
	});

	$('.show-lineups-exp').click(function(event) {
		event.preventDefault();
		$('.lineups-exp').toggle();
	});

	$('#universalrank-showfullpos').click(function(event) {
		$('.universalrank-fullpos').toggle();
		$('.universalrank-genpos').toggle();
		$(this).text(function(i, text){
          return text === "Show detailed positions" ? "Hide detailed positions" : "Show detailed positions";
		});
	});

	$('#universalrank-av-togglecents').click(function(event) {
		var pdfParam;

		$('.universalrank-avcents').toggle();
		$('.universalrank-avnocents').toggle();
		$(this).text(function(i, text){
          return text === "Show Cents" ? "Hide Cents" : "Show Cents";
		});

		// Specific to baseball auction tiers page
		if ($(this).hasClass('togglecents-pdf')) {
			if ($(this).text() === "Hide Cents") { pdfParam = "Yes"; } else { pdfParam = "No"; }
			$('#auctiontiers-pdf').attr('href',replaceUrlParam($('#auctiontiers-pdf').attr('href'), 'showcents', pdfParam));
		}
	});

	$('.datepicker').datepicker({ format: 'mm/dd/yyyy', autoclose: true });

	$('.bottombar-promo-dismiss').click(function(event) {
		createCookie("rwbottompromo",false,30);
		$(this).parents('.bottombar-promo').hide();
	});

	$('#compranks-flipbutton').click(function(event) {
		var individualsCheck = $(".compranks-individuals").is(':visible');
		var txt = individualsCheck ? 'Show Individual Ranks' : 'Show Rank Averages';
		$("#compranks-flipbutton").text(txt);

     	if (individualsCheck) {
	     	$(".compranks-individuals").hide();
	     	$(".compranks-averages").show();
     	}
     	else {
	     	$(".compranks-averages").hide();
	     	$(".compranks-individuals").show();
     	}
	});

	$('.weatherfeed-overview-col').matchHeight();

	// START AUTOMATIC SPONSOR NOTE LOGIC

		var sponsorAdCopy = "";
		var randomFanDuel = 1 + Math.floor(Math.random() * 2);

		var metaColumnID = parseInt($('meta[name=rotowireColumnID]').attr("content"));
		var metaArticleID = parseInt($('meta[name=rotowireArticleID]').attr("content"));

		function sponsorNote(adcopy,placementSlot,breakCount,sponsorNoteStop) {
			// Look for a tag in the article overriding the default placement slot
			var placementOverride = $('#autoplacement-dgames').data('slot');
			if (placementOverride !== undefined) { placementSlot = placementOverride; }

			$('.article-container br').each(function(i, val) {
				if ($(this).next().is('br') && $(this).prev().not('br')) {
					breakCount++;
				}
				if (breakCount == placementSlot && sponsorNoteStop === false) {
					$(this).after(adcopy);
					sponsorNoteStop = true;
				}
			});
		}

		// FANDUEL ALL SPORTS Sponsored Article Check
		if (metaArticleID > 21169 && $.inArray(metaColumnID, [42,46,53,82,135,158,163,165,175,199,210,212,216,229,255,272]) !== -1) {


			// Choose random ad copy between the two options
			if (randomFanDuel === 1) {
				sponsorAdCopy = '<div class="sponsor-linenote"><b>Sponsored Note</b> &ndash; <i>FREE 6-MONTH ROTOWIRE SUBSCRIPTION &ndash; Get a free subscription when you deposit $25 at FanDuel. <a target="_blank" href="https://fanduel.com/free-rotowire-sub">CLICK HERE</a></i></div>';
			}
			else if (randomFanDuel === 2) {
				sponsorAdCopy = '<div class="sponsor-linenote"><b>Sponsored Note</b> &ndash; <i>FREE 6-MONTH ROTOWIRE SUBSCRIPTION &ndash; Get a free subscription when you deposit $25 at FanDuel. <a target="_blank" href="https://fanduel.com/free-rotowire-sub">CLICK HERE</a></i></div>';
			}

			sponsorNote(sponsorAdCopy,5,0,false);
		}

		// DRAFTKINGS NFL Sponsored Article Check
		if (metaArticleID > 22797 && $.inArray(metaColumnID, [221]) !== -1) {
			sponsorAdCopy = '<div class="sponsor-linenote"><b>Sponsored Note</b> &ndash; <i>First time depositors can try DraftKings for FREE!<br><a target="_blank" href="https://www.draftkings.com/gateway?s=999007746">Click on this link</a> and draft your NFL team for a shot at thousands in prizes.</i></div>';
			sponsorNote(sponsorAdCopy,5,0,false);
		}

		// DRAFTKINGS NHL Sponsored Article Check
		if (metaArticleID > 22797 && $.inArray(metaColumnID, [308]) !== -1) {
			sponsorAdCopy = '<div class="sponsor-linenote"><b>Sponsored Note</b> &ndash; <i>First time depositors can try DraftKings for FREE!<br><a target="_blank" href="https://www.draftkings.com/gateway?s=154192607">Click on this link</a> and draft your NHL team for a shot at thousands in prizes.</i></div>';
			sponsorNote(sponsorAdCopy,5,0,false);
		}

		// DRAFTKINGS MLB Sponsored Article Check
		if (metaArticleID > 22797 && $.inArray(metaColumnID, [27,214,273]) !== -1) {
			sponsorAdCopy = '<div class="sponsor-linenote"><b>Sponsored Note</b> &ndash; <i>First time depositors can try DraftKings for FREE!<br><a target="_blank" href="https://www.draftkings.com/gateway?s=852054694">Click on this link</a> and draft your MLB team for a shot at thousands in prizes.</i></div>';
			sponsorNote(sponsorAdCopy,5,0,false);
		}

		// DRAFTKINGS NBA Sponsored Article Check
		if (metaArticleID > 22797 && $.inArray(metaColumnID, [207]) !== -1) {
			sponsorAdCopy = '<div class="sponsor-linenote"><b>Sponsored Note</b> &ndash; <i>First time depositors can try DraftKings for FREE!<br><a target="_blank" href="https://www.draftkings.com/gateway?s=944352396">Click on this link</a> and draft your NBA team for a shot at thousands in prizes.</i></div>';
			sponsorNote(sponsorAdCopy,5,0,false);
		}

		// DRAFTKINGS PGA Sponsored Article Check
		if (metaArticleID > 22797 && $.inArray(metaColumnID, [261]) !== -1) {
			sponsorAdCopy = '<div class="sponsor-linenote"><b>Sponsored Note</b> &ndash; <i>First time depositors can try DraftKings for FREE!<br><a target="_blank" href="https://www.draftkings.com/gateway?s=292579537">Click on this link</a> and draft your PGA team for a shot at $40,000 in prizes.</i></div>';
			sponsorNote(sponsorAdCopy,5,0,false);
		}

		// DRAFTKINGS MMA Sponsored Article Check
		if (metaArticleID > 22797 && $.inArray(metaColumnID, [290]) !== -1) {
			sponsorAdCopy = '<div class="sponsor-linenote"><b>Sponsored Note</b> &ndash; <i>First time depositors can try DraftKings for FREE!<br><a target="_blank" href="https://www.draftkings.com/gateway?s=185177405">Click on this link</a> and draft your MMA team for a shot at thousands in prizes.</i></div>';
			sponsorNote(sponsorAdCopy,8,0,false);
		}

		// DRAFTKINGS Soccer Sponsored Article Check
		if (metaArticleID > 22797 && $.inArray(metaColumnID, [254]) !== -1) {
			sponsorAdCopy = '<div class="sponsor-linenote"><b>Sponsored Note</b> &ndash; <i>First time depositors can try DraftKings for FREE!<br><a target="_blank" href="https://www.draftkings.com/gateway?s=390259756">Click on this link</a> and draft your soccer team for a shot at thousands in prizes.</i></div>';
			sponsorNote(sponsorAdCopy,5,0,false);
		}

	// END AUTOMATIC SPONSOR NOTE LOGIC

	// Clears the search box
	function clearSearchBox() {
		var view = $('#universalrank-playersearch').data('view');

		if (view == "Projections") {
			$playerSet = $('.universalrank-table').find('tr.universalrank-players');
		}
		else if (view == "Outlooks") {
			$playerSet = $('.universalrank-outlookrow');
		}

		$playerSet.show();

		$('#universalrank-playersearch').val('').removeClass('universalrank-clear-search');
	}

	// Clears the search box if you click the clear button
	$(document).on('click','.universalrank-clear-search',function(e) {
		var cursorPagePosX = e.pageX;
		var leftInputEdge = $(this).offset().left;
		var inputWidth = $(this).width();
		var percentNotClickable = 0.94;

		if (parseInt(cursorPagePosX - leftInputEdge) > parseInt(inputWidth * percentNotClickable)) {
				clearSearchBox();
		}
	});

	// Rankings Search
	$(document).on('keyup mousedown','#universalrank-playersearch',function(event) {
		var name;
		var userSearch = $(this).val();
		var view = $(this).data('view');
		var missingOverall = $('#mlbrankings-table').hasClass('universalrank-noshowov');
		var selectedPos = $('.universalrank-posfilter-sel').data('pos');

		if (event.type === 'mousedown') {
			if ($('#mlbplayersearch').length && $('.universalrank-posfilter-sel').data('pos') !== 'A' && userSearch.length === 0) {
				if (missingOverall) {
					if (selectedPos === 'SP' || selectedPos === 'RP' || selectedPos === 'P') {
						$('.universalrank-posfilter-pos[data-pos=P]').click();
					}
					else {
						$('.universalrank-posfilter-pos[data-pos=B]').click();
					}
				}
				else {
					$('.universalrank-posfilter-pos[data-pos=A]').click();
				}
			}
		}
		else {
			if (userSearch.length === 0) { clearSearchBox(); }
			else { $(this).addClass('universalrank-clear-search'); }

			if (view === "Projections" || view === "Stats" || view === "Earned Auction Values") {
				$playerSet = $('.universalrank-table').find('tr.universalrank-players');
			}
			else if (view === "Outlooks") {
				$playerSet = $('.universalrank-outlookrow');
			}

			if (userSearch.length !== 0) {
				$playerSet.each(function () {
					name = $(this).find('.universalrank-playername').text();
					if (name.search(new RegExp(userSearch, "i")) < 0) { $(this).hide(); } else { $(this).show(); }
				});
			}
		}

	});

	// Rankings position filters
	$(document).on('click','.universalrank-posfilter-pos',function() {
		if (!$(this).hasClass("universalrank-posfilter-sel")) {
			var clickedPos = $(this).data('pos');
			var view = $(this).data('view');
			$(this).addClass('universalrank-posfilter-sel');
			$(this).siblings('.universalrank-posfilter-pos').removeClass('universalrank-posfilter-sel');

			if ($(this).parents('#mlb-posfilter').length) {
				displayRankingsPosMLB(clickedPos,view);
			}
			else {
				displayRankingsPos(clickedPos,view);
			}
		}
	});

	// Check for position in URL (universal rankings)
	if ($('#universalrank-urlpos').length) {
		var urlPos = $('#universalrank-urlpos').text();
		$('.universalrank-posfilter-pos[data-pos=' + urlPos + ']').click();
	}

	// Shows or hides players based on position
	function displayRankingsPos(clickedPos,view) {
		var $playerSet;
		if (view === "Projections" || view === "Stats") {
			$playerSet = $('.universalrank-table').find('tr.universalrank-players');
		}
		else if (view === "Outlooks") {
			$playerSet = $('.universalrank-outlookrow');
		}
		var playerPos;
		if (clickedPos === 'A') {
			$playerSet.show();
		}
		else {
			$playerSet.each(function () {
				playerPos = $(this).find('.universalrank-position').data('pos');
				if (playerPos.indexOf(clickedPos + ',') >= 0) { $(this).show(); } else { $(this).hide(); }
			});
		}
	}

	// Using this to change text in MLB rankings table head
	function getFullPosMLB(pos) {
		var posName;

		if (pos === 'B') 		{ posName = 'Batter'; }
		else if (pos === 'P') 	{ posName = 'Pitcher'; }
		else if (pos === 'SP') 	{ posName = 'Starter'; }
		else if (pos === 'RP') 	{ posName = 'Reliever'; }
		else if (pos === 'C') 	{ posName = 'Catcher'; }
		else if (pos === '1B') 	{ posName = 'First Base'; }
		else if (pos === '2B') 	{ posName = 'Second Base'; }
		else if (pos === '3B') 	{ posName = 'Third Base'; }
		else if (pos === 'SS') 	{ posName = 'Shortstop'; }
		else if (pos === 'OF') 	{ posName = 'Outfielder'; }
		else if (pos === 'DH') 	{ posName = 'DH'; }
		else 					{ posName = ''; }

		return posName;
	}

	// Shows or hides players based on position (customized for MLB)
	function displayRankingsPosMLB(clickedPos,view) {
		// Grab all tables (so that the sticky headers get classes added to them too)
		var $tables = $('table');
		var $playerTable = $('#mlbrankings-table');
		var rankType = $playerTable.data('ranktype');
		var $excelLink = $('#universalrank-excel-link');
		var excelURL = $excelLink.attr('href');
		var $pdfLink = $('#universalrank-pdf-link');
		var pdfURL = $pdfLink.attr('href');

		var $playerSet;
		if (view === "Projections" || view === "Stats" || view === "Earned Auction Values") {
			$playerSet = $('#mlbrankings-table').find('tr.universalrank-players');
		}
		else if (view === "Outlooks") {
			$playerSet = $('.universalrank-outlookrow');
		}

		$('#universalrank-dynamicpos').text(' ' + getFullPosMLB(clickedPos));

		// Clear the search box
		$('#universalrank-playersearch').val("");

		var $currentPlayer;
		var playerPos;
		var playerColSpan;
		var footerColSpan;

		var classesToRemove = 'universalrank-showov universalrank-hidepitch universalrank-hidebat universalrank-specA universalrank-specB universalrank-specP universalrank-specSP universalrank-specRP universalrank-specC universalrank-spec1B universalrank-spec2B universalrank-spec3B universalrank-specSS universalrank-specOF universalrank-specDH';

		if (clickedPos === 'A') {

			if (view === "Projections" || view === "Stats" || view === "Earned Auction Values") {
				$tables.each(function(){
					if ($(this).hasClass('universalrank-showov') && !$(this).hasClass('universalrank-noshowov')) {
						playerColSpan = $(this).find('.universalrank-playerspan').attr('colspan');
						footerColSpan = $(this).find('.universalrank-footer').attr('colspan');
						if (rankType !== "Auction") {
							$(this).find('.universalrank-footer').attr('colspan',parseInt(footerColSpan) - 1);
							$(this).find('.universalrank-playerspan').attr('colspan',parseInt(playerColSpan) - 1);
						}
					}

					$(this).removeClass(classesToRemove).addClass('universalrank-specA');
				});
			}
			else if (view === "Outlooks") {
				$('#mlbrankings-outlooks').removeClass(classesToRemove).addClass('universalrank-specA');
			}

			$playerSet.show();

			if (view !== "Earned Auction Values") {
				// Change the position attribute in the Excel AND PDF URLs
				$excelLink.attr('href',replaceUrlParam(excelURL, 'pos', 'OVR'));
				$pdfLink.attr('href',replaceUrlParam(pdfURL, 'pos', 'OVR'));
			}
		}
		else if (clickedPos === 'P') {

			if (view === "Projections" || view === "Stats" || view === "Earned Auction Values") {
				$tables.each(function(){
					if (!$(this).hasClass('universalrank-showov') && !$(this).hasClass('universalrank-noshowov')) {
						playerColSpan = $(this).find('.universalrank-playerspan').attr('colspan');
						footerColSpan = $(this).find('.universalrank-footer').attr('colspan');

						if (rankType !== "Auction") {
							$(this).find('.universalrank-playerspan').attr('colspan',parseInt(playerColSpan) + 1);
							$(this).find('.universalrank-footer').attr('colspan',parseInt(footerColSpan) + 1);
						}
					}

					$(this).removeClass(classesToRemove).addClass('universalrank-showov universalrank-specP universalrank-hidebat');
				});
			}
			else if (view === "Outlooks") {
				$('#mlbrankings-outlooks').removeClass(classesToRemove).addClass('universalrank-specP universalrank-showov');
			}

			$playerSet.each(function () {
				$currentPlayer = $(this);
				playerPos = $currentPlayer.find('.universalrank-position').data('pos');
				if (playerPos.indexOf(',SP,') !== -1 || playerPos.indexOf(',RP,') !== -1 || playerPos.indexOf(',P,') !== -1) { $currentPlayer.show(); } else { $currentPlayer.hide(); }
			});

			if (view !== "Earned Auction Values") {
				// Change the position attribute in the Excel AND PDF URLs
				$excelLink.attr('href',replaceUrlParam(excelURL, 'pos', 'P'));
				$pdfLink.attr('href',replaceUrlParam(pdfURL, 'pos', 'P'));
			}
		}
		else if (clickedPos === 'B') {

			if (view === "Projections" || view === "Stats" || view === "Earned Auction Values") {
				$tables.each(function(){
					if (!$(this).hasClass('universalrank-showov') && !$(this).hasClass('universalrank-noshowov')) {
						playerColSpan = $(this).find('.universalrank-playerspan').attr('colspan');
						footerColSpan = $(this).find('.universalrank-footer').attr('colspan');

						if (rankType !== "Auction") {
							$(this).find('.universalrank-playerspan').attr('colspan',parseInt(playerColSpan) + 1);
							$(this).find('.universalrank-footer').attr('colspan',parseInt(footerColSpan) + 1);
						}
					}

					$(this).removeClass(classesToRemove).addClass('universalrank-showov universalrank-specB universalrank-hidepitch');
				});
			}
			else if (view === "Outlooks") {
				$('#mlbrankings-outlooks').removeClass(classesToRemove).addClass('universalrank-specB universalrank-showov');
			}

			$playerSet.each(function () {
				$currentPlayer = $(this);
				playerPos = $currentPlayer.find('.universalrank-position').data('pos');
				if (playerPos.indexOf(',SP,') !== -1 || playerPos.indexOf(',RP,') !== -1 || playerPos.indexOf(',P,') !== -1) { $currentPlayer.hide(); } else { $currentPlayer.show(); }
			});

			if (view !== "Earned Auction Values") {
				// Change the position attribute in the Excel AND PDF URLs
				$excelLink.attr('href',replaceUrlParam(excelURL, 'pos', 'B'));
				$pdfLink.attr('href',replaceUrlParam(pdfURL, 'pos', 'B'));
			}
		}
		else {
			if (view !== "Earned Auction Values") {
				// Change the position attribute in the Excel AND PDF URLs
				$excelLink.attr('href',replaceUrlParam(excelURL, 'pos', clickedPos));
				$pdfLink.attr('href',replaceUrlParam(pdfURL, 'pos', clickedPos));
			}

			if (clickedPos === "SP" || clickedPos === "RP") {

				if (view === "Projections" || view === "Stats" || view === "Earned Auction Values") {
					$tables.each(function(){
						if (!$(this).hasClass('universalrank-showov') && !$(this).hasClass('universalrank-noshowov')) {
							playerColSpan = $(this).find('.universalrank-playerspan').attr('colspan');
							footerColSpan = $(this).find('.universalrank-footer').attr('colspan');

							if (rankType !== "Auction") {
								$(this).find('.universalrank-playerspan').attr('colspan',parseInt(playerColSpan) + 1);
								$(this).find('.universalrank-footer').attr('colspan',parseInt(footerColSpan) + 1);
							}
						}

						$(this).removeClass(classesToRemove).addClass('universalrank-showov universalrank-spec' + clickedPos + ' universalrank-hidebat');
					});
				}
				else if (view === "Outlooks") {
					$('#mlbrankings-outlooks').removeClass(classesToRemove).addClass('universalrank-showov universalrank-spec' + clickedPos);
				}
			}
			else {

				if (view === "Projections" || view === "Stats" || view === "Earned Auction Values") {
					$tables.each(function(){
						if (!$(this).hasClass('universalrank-showov') && !$(this).hasClass('universalrank-noshowov')) {
							playerColSpan = $(this).find('.universalrank-playerspan').attr('colspan');
							footerColSpan = $(this).find('.universalrank-footer').attr('colspan');

							if (rankType !== "Auction") {
								$(this).find('.universalrank-playerspan').attr('colspan',parseInt(playerColSpan) + 1);
								$(this).find('.universalrank-footer').attr('colspan',parseInt(footerColSpan) + 1);
							}
						}

						$(this).removeClass(classesToRemove).addClass('universalrank-showov universalrank-spec' + clickedPos + ' universalrank-hidepitch');
					});
				}
				else if (view === "Outlooks") {
					$('#mlbrankings-outlooks').removeClass(classesToRemove).addClass('universalrank-showov universalrank-spec' + clickedPos);
				}
			}

			$playerSet.each(function () {
				$currentPlayer = $(this);
				playerPos = $currentPlayer.find('.universalrank-position').data('pos');
				if (playerPos.indexOf(',' + clickedPos + ',') !== -1) { $currentPlayer.show(); } else { $currentPlayer.hide(); }
			});
		}
	}

	// College Football Depth Charts Conference Filter
	$(document).on('click','.confnav',function() {
		var theConf = $(this).data('conf');
		$(this).addClass('confnav-active');
		$(this).siblings().removeClass('confnav-active');

		$('.cfbdepthchart').each(function() {
			if (theConf === "All" || theConf === $(this).data('conf')) { $(this).show(); } else { $(this).hide(); }
		});
	});

	// Simple News Team Filter
	$(document).on('click','.simplenewsnav',function() {
		var theTeam = $(this).data('team');
		$(this).addClass('simplenewsnav-active');
		$(this).siblings().removeClass('simplenewsnav-active');

		$('.simplenews-item').each(function() {
			if (theTeam === "All" || theTeam === $(this).data('team')) { $(this).show(); } else { $(this).hide(); }
		});
	});

	$(document).on('click','.rounding-switch',function() {
		if (this.checked) {
			$('.dproj-rounded').show();
			$('.dproj-precise').hide();
		}
		else {
			$('.dproj-rounded').hide();
			$('.dproj-precise').show();
		}
	});

	// Equalize Column Heights
	$('.equalheight').matchHeight();

	// Auction Tier $0 Player Show/Hide Toggle
	$('#auction-togglezero').on('click', function() {
		var zeroStatus;

		$('.auction-tier-zero').toggle();
		$('.auction-tier-zero-msg').toggle();
		$.fn.matchHeight._update();

		if ($(this).is(':checked')) { zeroStatus = "Yes"; } else { zeroStatus = "No"; }
		$('#auctiontiers-pdf').attr('href',replaceUrlParam($('#auctiontiers-pdf').attr('href'), 'showzero', zeroStatus));
	});

	// Auction Tiers Show/Hide Toggle
	$('#auction-toggletiers').on('click', function() {
		var tierStatus;

		$('.auction-tier-section').toggle();
		$.fn.matchHeight._update();

		if ($(this).is(':checked')) { tierStatus = "Yes"; } else { tierStatus = "No"; }
		$('#auctiontiers-pdf').attr('href',replaceUrlParam($('#auctiontiers-pdf').attr('href'), 'showtiers', tierStatus));

	});

	// Latest Article Pages (expand description)
	$('.latest-article-main').on({
    	mouseenter: function(){
        	$(this).css('max-height','500px');
    	},
		mouseleave: function(){
		 	$(this).css('max-height','107px');
    	}
	});

	// Latest Article Pages (get more articles)
	$(document).on('click','.latest-article-more',function(){
		var $button = $(this);
		var $articlesBox = $button.parents('.articlelist-articles');
		var sport = $button.data('sport');
		var isDaily = $button.data('daily');
		var lastDate = $button.data('lastdate');
		var numArticles = $button.data('num');
		var excludedArticles = [];
		var itemClass;

		if (isDaily === 'Y') { itemClass = 'latest-article-daily'; } else { itemClass = 'latest-article-season'; }

		// Put the excluded IDs in a string
		if (isDaily === 'Y') {
			$(".latest-article-daily").each(function() { excludedArticles.push($(this).data('articleid')); });
		}
		else {
			$(".latest-article-season").each(function() { excludedArticles.push($(this).data('articleid')); });
		}

		// if ($.inArray(24090, excludedArticles) !== -1) {  }

		$(this).text('Loading more articles...');

		$.ajax({
			type: 'POST',
			data: { 'sport': sport, 'isDaily': isDaily, 'lastDate': lastDate, 'numArticles': numArticles },
			url: '/articles-getmore.asp',
			dataType: 'json',
			success: function(results) {
				var newArticles = '';

				if (results.message) {
					$button.css('background-color','#cc1100').css('color','#fff').text(message);
				}
				else {

					// Loop through all the articles
					var addedArticles = 0;
					$.each(results, function(index,article) {
						if ($.inArray(article.aID, excludedArticles) === -1) {
							newArticles += '<div class="span23 latest-article-item ' + itemClass + '" data-articleid="' + article.aID + '">';
							newArticles += '<div class="span23 latest-article-row">';
							newArticles += '<div class="span6">';
							newArticles += '<a href="/' + article.directory + '/showArticle.htm?id=' + article.aID + '">';
							newArticles += '<img alt="' + article.sportName + '" src="http://content.rotowire.com' + article.picture +'"></a></div>';
							newArticles += '<div class="span16 latest-article-main">';
							newArticles += '<div class="span16 latest-article-meta">';
							newArticles += '<span class="latest-article-sport"><a href="/' + article.directory + '/features/">' + article.sportName + '</a></span>';
							newArticles += '<span class="latest-article-date">' + article.publishDateNice + '</span>';
							newArticles += '</div>';
							newArticles += '<div class="span16 latest-article-headline">';
							newArticles += '<a href="/' + article.directory + '/showArticle.htm?id=' + article.aID + '">' + article.headline + '</a></div>';
							newArticles += '<div class="span16 latest-article-desc">' + article.desc + '</div>';
							newArticles += '</div></div></div>';

							lastDate = article.publishDate;
							addedArticles++;
						}
					});

					var moreButton = '<div class="latest-article-more" data-sport="' + sport + '" data-lastdate="' + lastDate + '" data-daily="' + isDaily + '" data-num="' + numArticles + '">Show More Articles</div>';
					var noMoreButton = '<div style="text-align:center;font-size:16px;line-height:50px;color:#666;">There are no more articles to display.</div>';
					$articlesBox.append(newArticles);

					// Only show the "Show More" button if there are more articles to show, otherwise display "no more" message
					if (addedArticles !== 0) { $articlesBox.append(moreButton); } else { $articlesBox.append(noMoreButton); }

					$button.remove();
				}
			},
			error: function(results) {
				$button.css('background-color','#cc1100').css('color','#fff').text('Unable to load more articles');
			}
		});
	});

	// Clear the article search input
	function clearArticleSearch() {
		// Hide the clear button
		$('.articlesearch-clear').hide();

		// Erase the input
		$('#articlesearch-input').val('');

		// Make sure the search results section is hidden
		$('.articlelist-searchresults').hide();

		// Clear out any error messages and hide the error section
		$('.articlelist-search-message').text('').hide();

		// Set the search button text back to its original value
		$('#articlesearch-button').text($('#articlesearch-button').data('origtext'));
	}

	// Get the blog category name for a sport
	function sportToBlogCat(sport) {
		 var catName;

		 switch(sport) {
		 case 'NFL':
		 	catName = 'Fantasy Football';
		 	break;
		 case 'MLB':
		 	catName = 'Fantasy Baseball';
		 	break;
		 case 'NBA':
		 	catName = 'Fantasy Basketball';
		 	break;
		 case 'NHL':
		 	catName = 'Fantasy Hockey';
		 	break;
		 case 'CFB':
		 	catName = 'College Football';
		 	break;
		 case 'CBB':
		 	catName = 'College Basketball';
		 	break;
		 case 'PGA':
		 	catName = 'Fantasy Golf';
		 	break;
		 case 'RAC':
		 	catName = 'Fantasy NASCAR';
		 	break;
		 case 'SOC':
		 	catName = 'Fantasy Soccer';
		 	break;
		 case 'MMA':
		 	catName = 'Fantasy MMA';
		 	break;
		 default:
		 	catName = 'All';
		}

		return catName;
	}

	function showSearchResults() {

		// Show the results section
		$('.articlelist-searchresults').fadeIn();

		// Equalize Search Result Column Heights
		$('.equalheight').matchHeight();

		// Set the search button text back to its original value
		$('#articlesearch-button').text($('#articlesearch-button').data('origtext'));
	}

	function searchBlogArticles(searchTerm,sport) {
		var resultsLimit = 100;
		var searchedCategory = sportToBlogCat(sport);
		var $mainResultsSection = $('.articlelist-searchresults-blogsection');

		$('#articlesearch-button').text('Searching RotoWire Blog...');

		// DO THE BLOG SEARCH HERE
		$.ajax({
			url: 'http://www.rotowire.com/blog/?s=' + searchTerm + '&feed=json',
			dataType: 'json',
			success: function(results) {
				var newArticles = '';

				// Loop through all the articles
				var addedArticles = 0;
				var articleYear = 0;
				var lastArticleYear = 0;
				$.each(results, function(index,article) {
					var articleDate = $.format.date(article.date, 'MMMM d');
					var categoryName = $.trim(article.categories[0]);

					// Only search within the sport unless it's searching all sports or in the default generic blog category
					if (categoryName === searchedCategory || searchedCategory === 'All' || categoryName === 'Fantasy Sports') {
						articleYear = $.format.date(article.date, 'yyyy');

						// If it's a new year, then display the year heading
						if (articleYear !== lastArticleYear) { newArticles += '<div class="articlelist-searchresults-year">' + articleYear + '</div>'; }

						// Build the article item and append it to the string
						newArticles += '<div class="articlelist-searchresult">';
						newArticles += '<div class="latest-article-meta">';
						newArticles += '<span class="latest-article-sport">' + categoryName + '</span>';
						newArticles += '<span class="latest-article-date">' + articleDate + '</span>';
						newArticles += '</div>';
						newArticles += '<div class="latest-article-headline">';
						newArticles += '<a href="' + article.permalink + '">' + article.title + '</a></div>';

						newArticles += '<div class="latest-article-byline">';
						newArticles += 'By ' + article.author;
						newArticles += '</div>';
						newArticles += '<div class="latest-article-desc">' + $.trim(article.excerpt).substring(0, 100).split(' ').slice(0, -1).join(' ') + '...</div>';
						newArticles += '</div>';

						lastArticleYear = articleYear;
						addedArticles++;
					}
				});

				if (addedArticles === resultsLimit) {
					newArticles += '<div class="articlelist-search-limited"><b>There were more than ' + resultsLimit + ' results for your search.</b><br> In order to keep our search function as fast as possible, we limit the number of articles displayed in the results to the ' + resultsLimit + ' most recent matching articles. In most cases, you can find what you\'re looking for with a more specific search though.</div>';
				}

				if (addedArticles === 0) {
					newArticles += '<div class="articlelist-searchresults-none">Unfortunately, no blog articles were found that matched your search term.</div>';
				}

				// Add the results to the main search results section
				$mainResultsSection.html(newArticles);
				showSearchResults();
			},
			error: function(results) {
				// If there was an error with the search, show an error message
				$mainResultsSection.html('<div class="articlelist-searchresults-none">Unfortunately, no blog articles were found that matched your search term.</div>');
				showSearchResults();
			}
		});
	}

	function articleSearch(searchTerm,sport) {
		var resultsLimit = 100;
		var $messageArea = $('.articlelist-search-message');
		var $mainResultsSection = $('.articlelist-searchresults-section');

		// Google Analytics Event Tracking
		if (typeof ga !== 'undefined') { ga('send', 'event', 'Article Search', searchTerm, sport, false); }

		// Put the search term in quotation marks in the search result header
		$('#articlelist-searchterm').text(searchTerm);

		// If the search term is at least 3 characters long, then run the search
		if (searchTerm.length >= 3) {
			$messageArea.text('').hide();
			$('#articlesearch-button').text('Searching RotoWire...');

			$.ajax({
				type: 'POST',
				data: { 'sport': sport, 'search': searchTerm, 'limit': resultsLimit },
				url: '/articles-search.asp',
				dataType: 'json',
				success: function(results) {
					var newArticles = '';

					// If there were no articles found, show that message
					if (results[0].message) {
						$mainResultsSection.html('<div class="articlelist-searchresults-none">' + results[0].message + '</div>');
						searchBlogArticles(searchTerm,sport);
					}
					else {

						// Loop through all the articles
						var addedArticles = 0;
						var articleYear = 0;
						var lastArticleYear = 0;
						$.each(results, function(index,article) {
							var authors  = '';
							articleYear = article.publishYear;

							// If it's a new year, then display the year heading
							if (articleYear !== lastArticleYear) { newArticles += '<div class="articlelist-searchresults-year">' + articleYear + '</div>'; }

							// Build the article item and append it to the string
							newArticles += '<div class="articlelist-searchresult">';
							newArticles += '<div class="latest-article-meta">';
							newArticles += '<span class="latest-article-sport"><a href="/' + article.directory + '/features/">' + article.sportName + '</a></span>';
							newArticles += '<span class="latest-article-date">' + article.publishDateNice + '</span>';
							newArticles += '</div>';
							newArticles += '<div class="latest-article-headline">';
							newArticles += '<a href="/' + article.directory + '/showArticle.htm?id=' + article.aID + '">' + article.headline + '</a></div>';

							newArticles += '<div class="latest-article-byline">';

							// If there are no authors, do not start the byline
							if ($.trim(article.authors.length) > 0) { newArticles += 'By '; }

							// Loop through each author
							$.each(article.authors, function(index,authorItem) {
								authors += '<a href="/expert.htm?name=' + authorItem.username + '">' + authorItem.author + '</a> & ';
							});

							// Trim the spaces and ampersand from the last author
							authors = authors.slice(0,-3);

							newArticles += authors;
							newArticles += '</div>';
							newArticles += '<div class="latest-article-desc">' + article.desc + '</div>';
							newArticles += '</div>';

							lastArticleYear = articleYear;
							addedArticles++;
						});

						if (addedArticles === resultsLimit) {
							newArticles += '<div class="articlelist-search-limited"><b>There were more than ' + resultsLimit + ' results for your search.</b><br> In order to keep our search function as fast as possible, we limit the number of articles displayed in the results to the ' + resultsLimit + ' most recent matching articles. In most cases, you can find what you\'re looking for with a more specific search though.</div>';
						}

						// Add the results to the main search results section
						$mainResultsSection.html(newArticles);

						searchBlogArticles(searchTerm,sport);
					}
				},
				error: function(results) {
					// If there was an error with the search, show an error message
					$mainResultsSection.html('<div class="articlelist-searchresults-none" style="color:#cc1100;">We were unable to finish this search due to an error.</div>');
					searchBlogArticles(searchTerm,sport);

					// Google Analytics Event Tracking for Errors
					if (typeof ga !== 'undefined') { ga('send', 'event', 'Article Search Error', searchTerm, sport, false); }
				}
			});
		}
		else {
			$('.articlelist-searchresults').hide();
			$messageArea.text('Your search must be at least 3 characters long.').show();
		}
	}

	// Article Search (Enter Key)
	$(document).on('keyup','#articlesearch-input',function(event){
		var searchTerm = $.trim($(this).val());
		var sport = $('#articlesearch-button').data('sport');

		// Show (or hide) the clear search button
		if (searchTerm.length > 0) { $('.articlesearch-clear').fadeIn(); } else { $('.articlesearch-clear').hide(); }

		// Only run the search if they hit enter
		if(event.keyCode == 13) {
			articleSearch(searchTerm,sport);
		}
	});

	// Article Search (Search Button)
	$(document).on('click','#articlesearch-button',function(event){
		var searchTerm = $.trim($('#articlesearch-input').val());
		var sport = $(this).data('sport');

		articleSearch(searchTerm,sport);
	});

	// Clear Article Search (Search Button)
	$(document).on('click','.articlesearch-clear',clearArticleSearch);


	$(document).on('click','#dfsnotice-valuereport', function() {
		$(this).parent().fadeOut();
		createCookie("hidenoticevr",true,30);
	});

	$(document).on('click','#dfsnotice-optimizer', function() {
		$(this).parent().fadeOut();
		createCookie("hidenoticeopt",true,30);
	});

	$(document).on('click','#projections-optimizer', function() {
		$(this).parent().fadeOut();
		createCookie("hideprojectionsopt",true,30);
	});

	// Show more podcast episodes on podcasts page
	$(document).on('click','.pod-showmore', function() {
		$(this).fadeOut();
		$(this).siblings('.pod-hidden').fadeIn();
	});

	// Show hidden in-season baseball rankings position eligibilty settings
	$(document).on('click','#show-inseason-poseligible',function(){
		$(this).hide();
		$('#inseason-elig-controls').attr('style','display:block;').fadeIn();
	});

	// Display podcast and videos links
	$('.mediafeed-container').each(function(){
		var $mediaSection = $(this);
		var sport = $mediaSection.data('sport');
		var numPods = $mediaSection.data('numpods') || 5;

		var podcasts = {
  		//Tim Mccaigue - 3/24/2016 - setting all to use MLB, query was bringing back any podcast with RotoWire in the description (FanGraph podcast)
			//'All'                : 'https://api.audioboom.com/audio_clips?find[query]=RotoWire',
			'All'                : 'https://api.audioboom.com/channels/4579428/audio_clips',
			'Basketball'         : 'https://api.audioboom.com/channels/4579432/audio_clips',
			'Football'           : 'https://api.audioboom.com/channels/4661748/audio_clips',
			'Baseball'           : 'https://api.audioboom.com/channels/4579428/audio_clips',
			'College Football'   : 'https://api.audioboom.com/channels/4579434/audio_clips',
			'East Coast Offense' : 'https://api.audioboom.com/channels/4579443/audio_clips',
			'Soccer'             : 'https://api.audioboom.com/channels/4579456/audio_clips',
			'DFS'                : 'https://api.audioboom.com/channels/4579437/audio_clips',
			'Football Draft Kit' : 'https://api.audioboom.com/channels/4579445/audio_clips',
			'Hockey'             : 'https://api.audioboom.com/channels/4579449/audio_clips',
			'Prospect'           : 'https://api.audioboom.com/channels/4579452/audio_clips',
			'Short Hops'         : 'https://api.audioboom.com/channels/4579454/audio_clips'
		};

		var sections = {
			'Cricket'         : { 'feed': podcasts.All, 				'displaySport': '' },
			'DFS'             : { 'feed': podcasts.DFS, 				'displaySport': 'DFS' },
			'eSports'         : { 'feed': podcasts.All, 				'displaySport': '' },
			'Golf'            : { 'feed': podcasts.All, 				'displaySport': '' },
			'HOME'            : { 'feed': podcasts.All, 				'displaySport': '' },
			'MMA'             : { 'feed': podcasts.All, 				'displaySport': '' },
			'MLB'             : { 'feed': podcasts.Baseball, 			'displaySport': 'MLB' },
			'NASCAR'          : { 'feed': podcasts.All, 				'displaySport': '' },
			'NBA'             : { 'feed': podcasts.Basketball, 			'displaySport': 'NBA' },
			'NCAA Basketball' : { 'feed': podcasts.All, 				'displaySport': '' },
			'NCAA Football'   : { 'feed': podcasts['College Football'], 'displaySport': 'NCAA Football' },
			'NFL'             : { 'feed': podcasts.Football, 			'displaySport': 'NFL' },
			'NHL'             : { 'feed': podcasts.Hockey, 				'displaySport': 'NHL' },
			'Soccer'          : { 'feed': podcasts.Soccer, 				'displaySport': 'Soccer' }
		};

		var feed = sections[sport].feed;

		$mediaSection.find('h2').text('RotoWire ' + sections[sport].displaySport + ' Podcasts & Videos');

		var episodesHTML = '';

		$.ajax({
			url: feed,
			dataType: 'json',
			success: function(data) {
				var episodes = data.body.audio_clips;
				$.each(episodes,function(index,episode){
					if (index === numPods) { return false; }
					var episodeTitle = episode.title;
					var episodeLink = episode.urls.detail;
					var episodeDesc = episode.description;
					var episodeDate = $.format.date(episode.uploaded_at,'MMMM d, yyyy');

					episodesHTML += '<div class="span17 story-row" title="' + episodeDesc + ' ' + episodeDate + '."><div class="span17 media-story"><img class="sound-icon" src="/images/sound-icon-blue.png"><a href="' + episodeLink + '" target="_blank">' + episodeTitle + '</a></div></div>';
				});

				// Add the videos link
				episodesHTML += '<div class="span17 story-row"><div class="span17 media-story"><img class="video-icon" src="/images/video-icon-blue.png"><a href="/videos/">Check Out RotoWire on 120 Sports</a></div></div>';

				$('.media-loading').remove();
				$mediaSection.append(episodesHTML);
			}
		});


	});

	// Display blog articles
	$('.blogfeed-container').each(function(){
		var $blogSection = $(this);
		var sport = $blogSection.data('sport');
		var rowCol = $blogSection.data('rowcol') || 17;
		var numArticles = $blogSection.data('numarticles') || 5;

		var feedURLs = {
			'CBB'  : 'http://www.rotowire.com/blog/sport/ncaa-basketball/feed/json',
			'CFB'  : 'http://www.rotowire.com/blog/sport/ncaa-football/feed/json',
			'HOME' : 'http://www.rotowire.com/blog/feed/json',
			'MLB'  : 'http://www.rotowire.com/blog/sport/mlb/feed/json',
			'MMA'  : 'http://www.rotowire.com/blog/sport/mma/feed/json',
			'NBA'  : 'http://www.rotowire.com/blog/sport/nba/feed/json',
			'NFL'  : 'http://www.rotowire.com/blog/sport/nfl/feed/json',
			'NHL'  : 'http://www.rotowire.com/blog/sport/nhl/feed/json',
			'PGA'  : 'http://www.rotowire.com/blog/sport/golf/feed/json',
			'RAC'  : 'http://www.rotowire.com/blog/sport/nascar/feed/json',
			'SOC'  : 'http://www.rotowire.com/blog/sport/soccer/feed/json'
		};

		var feedURL = $blogSection.data('feed') || feedURLs[sport];

		var sportIcons = {
			'College Basketball' : 'ncaabicon20',
			'College Football'   : 'ncaaficon20',
			'Fantasy Baseball'   : 'mlbicon20',
			'Fantasy Basketball' : 'nbaicon20',
			'Fantasy Football'   : 'nflicon20',
			'Fantasy Golf'       : 'golficon20',
			'Fantasy Hockey'     : 'nhlicon20',
			'Fantasy MMA'        : 'mmaicon20',
			'Fantasy NASCAR'     : 'nascaricon20',
			'Fantasy Soccer'     : 'soccericon20',
		};

		var sportFeedPath = {
			'HOME' : '',
			'CFB' : '/sport/ncaa-football',
			'CBB' : '/sport/ncaa-basketball',
			'MLB' : '/sport/mlb',
			'NBA' : '/sport/nba',
			'NFL' : '/sport/nfl',
			'PGA' : '/sport/golf',
			'NHL' : '/sport/nhl',
			'MMA' : '/sport/mma',
			'RAC' : '/sport/nascar',
			'SOC' : '/sport/soccer'
		};

		var sections = {
			'HOME' : '',
			'CFB' : 'NCAA Football',
			'CBB' : 'NCAA Basketball',
			'MLB' : 'Fantasy Baseball',
			'NBA' : 'NBA',
			'NFL' : 'NFL',
			'PGA' : 'GOLF',
			'NHL' : 'NHL',
			'MMA' : 'MMA',
			'RAC' : 'NASCAR',
			'SOC' : 'Soccer'
		};

		$blogSection.find('h2').text('Latest From Our ' + sections[sport] + ' Blog');

		var articleListHTML = '';

		$.ajax({
			url: feedURL,
			dataType: 'json',
			success: function(data) {
				$.each(data, function(index, article){
				  	if (index === numArticles) { return false; }

					var storyRow = '';
					var articleCategory = article.categories[0];
					var sportIcon =  sportIcons[articleCategory] || "default";
					var leftSportSection = (sportIcon === "default") ? '&nbsp;' : '<div class="' + sportIcon + '"></div>';
					var articleLink = '<a href="'+ article.permalink + '" target="_blank">' + article.title + '</a>';

					if (sport === 'HOME') {
						storyRow = '<div class="span2 story-sport">' + leftSportSection + '</div><div class="span' + (rowCol-2) + ' story">' + articleLink;
					}
					else {
						storyRow = '<div class="span' + rowCol + ' story" style="padding-left:15px;">' + articleLink;
					}

					articleListHTML += '<div class="span' + rowCol + ' story-row">' + storyRow + '</div></div>';
				});

				var blogSectionLink = '<a href="http://www.rotowire.com/blog' + sportFeedPath[sport] + '/">';
				var readMoreText = (sport === 'HOME') ?  'Read More On The RotoWire Blog' : 'Read More On Our ' + sport + ' Blog';

				// Add the Read More Link
				articleListHTML += '<div class="span' + rowCol + ' story-row"><div class="span2 story-sport"><div class="icon-share-alt readmore-icon"></div></div><div class="span' + (rowCol-2) + ' story">' + blogSectionLink + readMoreText + '</a></div></div>';

				// Add the HTML to the page
				$('.blog-loading').remove();
				$blogSection.append(articleListHTML);
			}
		});
	});

	// eSports News Pages (get more news)
	$(document).on('click','.esports-news-showmore',function(){
		var $button = $(this);
		var $articlesBox = $('#esports-news-items');
		var lastDate = $button.data('lastdate');
		var newLastDate;
		var game = $button.data('game');
		var origButtonText = $button.text();
		var excludedNotes = [];

		$(".es-news-item").each(function() { excludedNotes.push($(this).data('uid')); });

		$(this).text('Loading more news...');

		$.ajax({
			type: 'POST',
			data: { 'game': game, 'lastDate': lastDate },
			url: '/esports/gamenews-getmore.php',
			dataType: 'json',
			success: function(results) {
				var noMoreButton = '<div style="text-align:center;font-size:24px;line-height:30px;font-weight:300;color:#666;">There are no more news updates to read.</div>';
				var addedNotes = 0;
				var newNotes = '';

				// Catch error message
				if (results.message) {
					$button.css('background-color','#cc1100').css('color','#fff').text(message);
					return;
				}

				// Loop through all the articles
				$.each(results.records, function(index,note) {
					var newsItemClass;
					var logoURL;
					var noteDate = $.format.date(note.updatedatetime, "M/d/yyyy");
					if ($.inArray(note.uid, excludedNotes) === -1) {
						if (index % 2 === 0) { newsItemClass = 'news-item'; } else { newsItemClass = 'news-item-shaded'; }
						if (note.team_id) {
							logoURL = 'http://content.rotowire.com/images/teamlogo/esports/' + note.team_id + '.png';
						}
						else {
							logoURL = 'http://content.rotowire.com/images/teamlogo/esports/default' + note.game_id + '.png';
						}

						newNotes +=
						'<div class="span34 es-news-item ' + newsItemClass + '" data-uid="' + note.uid + '">' +
							'<div class="offset1 span4 news-teamlogo">' +
								'<img src="http://content.rotowire.com/images/teamlogo/esports/' + note.team_id + '.png">' +
								'<p class="news-item-date">' + noteDate + '</p>' +
							'</div>' +

							'<div class="span28">' +
								'<div class="span28 news-player">' +
									'<div class="span28">' +
										'<a href="/esports/player.php?id=' + note.UNQ + '">' + note.gamertag + '</a> &nbsp;&nbsp;' + note.teamname +
									'</div>' +
								'</div>' +

								'<div class="news-item-news">' + note.updatenotes + '</div>' +
								'<div class="news-item-analysis">' +
									'<p>RotoWire Analysis</p>' +
									note.recommendation +
								'</div>' +

							'</div>' +
						'</div>';

						newLastDate = note.updatedatetime;
						addedNotes++;
					}
				});

				// Append the news items to the news box and update the button
				$articlesBox.append(newNotes);
				$button.text(origButtonText).data('lastdate',newLastDate);

				// If less than 50 updates come back, show a "no more news message"
				if (results.records.length < 50) {
					$button.after(noMoreButton);
					$button.remove();
				}
			},
			error: function(results) {
				$button.css('background-color','#cc1100').css('color','#fff').text('Unable to load more articles');
			}
		});
	});

	/**********************************************
	DFS PLAYER PAGE - SLIDE OUT PANEL
	  How to use:
	  1) Add an ID of "dfsPanelsOn" to any element on the page.
	  2) On the #dfsPanelsOn element, add a data attribute named "site" with the site name (ex. FanDuel) as the value.
	  3) Add the "dplayer-link" class to the player links you want to trigger the player panel
	***********************************************/

	    var playerPanel = {

			// Get the sport from the footer and return the correct DFS section directory
			getDFSDirectory: function(){
				var sport = $('#site-footer').data('sport');
				var folders = {
					'CBB': 'ncaab',
					'CFB': 'college',
					'CRI': 'cricket',
					'ESP': 'esports',
					'MLB': 'mlb',
					'MMA': 'mma',
					'NBA': 'nba',
					'NFL': 'nfl',
					'NHL': 'nhl',
					'PGA': 'golf',
					'RAC': 'racing',
					'SOC': 'soccer'
				};

				return folders[sport] || 'MLB';
			},

	        // Handles a click outside of player panel
	        handleClickOutside: function(e){
	            var $panel = $('#playerPanel');

	            // Check if the user clicked somewhere other than the player panel
	            var clickOutsidePanel = (!$panel.has(e.target).length || $panel.is(e.target)) ? true : false;

	            // If the user clicked outside the player panel, close the player panel and reset the page to its original state
	            if (clickOutsidePanel) { playerPanel.reset(); }
	        },

	        // Loads a panel inside the player page (one of the tabs)
	        loadPanel: function(panelName){

	            // Get the sport, partner site and the player ID
	            // This info is stored in data attributes on the navigation tabs container
	            var $tabs = $('#pp-tabs');
	            var sport = $tabs.data('sport').toLowerCase();
	            var site = $tabs.data('site');
	            var playerID = $tabs.data('playerid');
				var team = $tabs.data('team');
				var pos = $tabs.data('pos');
				var throws = $tabs.data('throws');

	            // Find the panel that is being loaded
	            var $panel = $('#pp-' + panelName);

	            // Check to see if it needs to be loaded or not by looking inside the panel
	            // If an element with the 'pp-need-to-load' is found, then the panel needs to be loaded
	            var needsToLoad = ($panel.find('.pp-need-to-load').length > 0) ? true : false;

	            // If the panel is already loaded, exit out without trying to reload the data
	            if (!needsToLoad) { return; }

	            // Load the panel via AJAX
	            var ajaxCall = $.ajax({
	                type: 'POST',
	                data: { 'playerID': playerID, 'site': site, 'team': team, 'pos': pos, 'throws': throws },
	                url: '/daily/' + sport + '/player-' + panelName + '.php'
	            });

	            // If it fails, show an error
	            ajaxCall.fail(playerPanel.showLoadPanelError);

	            // If it suceeds, load the page data into the panel
	            ajaxCall.done(function(pageData){
					if (pageData.length > 0) {

		                // Load the page data
		                $panel.html(pageData);

		                // Enable tablesorter sticky headers inside the player panel
		                // Sticky headers keep the table headings at the top while you scroll the panel (useful for game log panel)
		                $('.pp-sticky').tablesorter({
		                    sortInitialOrder: 'desc',
		                    widgets: [ 'stickyHeaders' ],
		                    widgetOptions: {
		                      // jQuery selector or object to attach sticky header to
		                      stickyHeaders_attachTo: '.pp-section',
		                      stickyHeaders_offset: 110
		                    }
		                });
					}
					else {
						playerPanel.showLoadPanelError();
					}

	            });
	        },

	        open: function(playerID,site){

	            // Build the html for the player panel loading indicator
	            var loadingIndicator = '<div class="pp-loading"><img class="infinite-spin" src="http://content.rotowire.com/images/rw-logo-circle.png">Loading Player Information...</div>';

	            // Add a class to the body to prevent it from scrolling and append the player panel background
	            $('body').addClass('pp-prevent-scroll').append('<div class="pp-panel-background"></div>');

	            // Append the player panel (with the loading indicator inside) to the player panel background
	            $('.pp-panel-background').append('<div id="playerPanel">' + loadingIndicator + '</div>');

	            // Animate the player panel sliding out from the left (starts at -650px and moves to 0px)
	            $('#playerPanel').animate({ left: '0' });

				// Get the daily section folder
				var sportFolder = playerPanel.getDFSDirectory();

	            // Get the player panel with the overview tab data loaded in by default
	            var ajaxCall = $.ajax({
	                type: 'POST',
	                data: { 'playerID': playerID, 'site': site },
	                url: '/daily/' + sportFolder + '/player.php'
	            });

	            // If it fails to load, show an error
	            ajaxCall.fail(playerPanel.showLoadError);

	            // Load the player panel page data into the player panel container
	            ajaxCall.done(function(response){
					if (response.length > 0) {
						$('#playerPanel').html(response);
					}
					else {
						playerPanel.showLoadError();
					}
	            });
	        },

	        // Close the player panel and resets the state of the page
	        reset: function(){

	            // Remove the class that prevents the body from scrolling
	            $('body').removeClass('pp-prevent-scroll');

	            // Move the player panel to the left 650px so it's offscreen
	            $('#playerPanel').animate({ left: '-650px' }, {

	                // Once the animation is complete,
	                // remove the player panel background and the player panel
	                complete: function() {
	                    $('.pp-panel-background').remove();
	                    $(this).remove();
	                }
	            });
	        },

	        // Show an error if the entire player panel fails to load
	        showLoadError: function(panelName) {

	            // Remove any existing error bars (just in case they trigger multiple errors quickly)
	            $('.pp-error-bar').remove();

	            // Reset the page
	            playerPanel.reset();

	            // Build the error message html
	            var errorHTML = '<div class="pp-error-bar">We were unable to load this player. Please try again.</div>';

	            // Show an error message at the bottom of the screen
	            $('body').append(errorHTML);

	            // Remove the error bar from the page after four seconds
	            setTimeout(function(){ $('.pp-error-bar').remove(); }, 4000);
	        },

	        // Show an error if a panel doesn't load
	        showLoadPanelError: function(panelName) {

	            // Find the panel where the error will be displayed
	            var $panel = $('#pp-' + panelName);

	            // The html for the error message
	            var errorHTML = '<div class="pp-panel-loaderror pp-need-to-load">Sorry. We couldn\'t load the player data.<br><button class="btn btn-defaultflat pp-reload-panel" data-name="' + panelName + '">Try Reloading Now</button></div>';

	            // Replace the contents of the panel with the error message
	            $panel.html(errorHTML);
	        },

	        // Switch to a different player panel tab
	        switchTab: function(panelName){

	            // Get the navigation tab for the panel the user is switching to
	            var $navItem = $('.pp-tab[data-name="' + panelName + '"]');

	            // Switch the selected nav item class to that panel
	            $navItem.addClass('pp-tab-sel').siblings('.pp-tab').removeClass('pp-tab-sel');

	            // Hide all the other panels except the one clicked on
	            $('.pp-section').addClass('hide');
	            $('#pp-' + panelName).removeClass('hide');

	            // Load the panel
	            playerPanel.loadPanel(panelName);
	        },

	        // Triggers opening a player panel
	        triggerOpen: function(e){

	            // The default action of a link is to take the user to the href location
	            // This prevents that
	            e.preventDefault();

	            var $playerLink = $(this);

				// Get the site name from the element with the id of #dfsPanelsOn
	            var site = $('#dfsPanelsOn').data('site');

				// Parse the URL to find the playerID
				var link = $playerLink.attr('href').toLowerCase();
				var queryString = link.substring( link.indexOf('?') + 1 );
				var playerID = $.getQueryParameters(queryString).id;

				// Show an error if the data is not available
				if (!playerID || !site){
					playerPanel.showLoadError();
					return;
				}

	            // Open the player panel
	            playerPanel.open(playerID,site);
	        },

	        // Triggers a reload of a panel that failed to load initially
	        triggerPanelReload: function(){

	            // Get the name of the panel to reload
	            var panelName = $(this).data('name');

	            // Reload the panel
	            playerPanel.loadPanel(panelName);
	        },

	        // Triggers a switch to a different panel (using the navigation tabs)
	        triggerTabSwitch: function(){

	            // Get the name of the panel to switch to
	            var panelName = $(this).data('name');

	            // Switch to the panel
	            playerPanel.switchTab(panelName);
	        },

	        // Triggers a switch to a different panel (from any element with the matching data attribute)
	        triggerTabSwitchData: function(){

	            // Get the name of the panel switch to
	            var panelName = $(this).data('switchtab');

	            // Switch to the panel
	            playerPanel.switchTab(panelName);
	        },

	        // Add Event Listeners
	        activate: function(){

	            // Triggers a switch to a different panel (using the navigation tabs)
	            $(document).on('click','.pp-tab', playerPanel.triggerTabSwitch);

	            // Triggers a switch to a different panel (from any button with the matching data attribute)
	            $(document).on('click','button[data-switchtab]', playerPanel.triggerTabSwitchData);

	            // Controls DFS player panel links
	            $(document).on('click','.dplayer-link', playerPanel.triggerOpen);

	            // Close player panel (using close button)
	            $(document).on('click','.pp-close-panel', playerPanel.reset);

	            // Handles click outside of player panel
	            $(document).on('click','.pp-panel-background', playerPanel.handleClickOutside);

	            // Tries to reload a panel that failed to load
	            $(document).on('click','.pp-reload-panel', playerPanel.triggerPanelReload);
	        }
	    };
	    playerPanel.activate();

	/**********************************************
	 END DFS PLAYER PAGE - SLIDE OUT PANEL
	***********************************************/

/**********************************************
 PLAYER POOL MANAGEMENT
 To use this feature:

 1) Add the .playerpool class to the table <tbody> element.
 2) Add .playerpool-name to the player name cells, .playerpool-salary to the salary cells, and .playerpool-pos to the position cells.
 3) Add a pid attribute (playerID) and team attribute to the table row elements.
 4) Use playerpool-postabs, playerpool-postab, and playerpool-postab-sel for the position filter classes.
 5) Use playerpool- as the prefix (instead of lineupopt- or rwo-) in the games schedule section, player search, excluded players section, etc.
 6) See /daily/ncaab/dailytrends.php for example usage.
***********************************************/

	var playerPool = {

		// Adds player(s) back to the player pool (takes a single player ID or an array of player IDs)
        addPlayersBackToPool: function(playerIDs) {

            // Convert a single player ID to an array when only one player ID is passed in
            playerIDs = ($.isArray(playerIDs)) ? playerIDs : [playerIDs];

            // Cache the length of the array of player IDs to speed up the for loop below
            var playerCount = playerIDs.length;

            // Loop through the array of player IDs
            for(var i = 0; i < playerCount; i++) {

                // Get the current player's ID
                var playerID = playerIDs[i];

                // Get the current player's table row in the player pool
                var $excludedPlayerRow = playerPool.getPlayerRow(playerID);

                // Remove the excluded class from the player row (in the player pool table)
                $excludedPlayerRow.removeClass('excluded');

                // Remove the excluded class from the player row (in the optimal lineup table)
                $('#lineup').find('tr[data-pid="' + playerID + '"]').removeClass('excluded');

                // Remove the player from the excluded players section of the page
                $('.playerpool-excludedlist-player[data-pid="' + playerID + '"]').remove();
            }
        },

		// Adds player(s) to the excluded players section of the page (takes a single player ID or an array of player IDs)
        addPlayersToExcludedSection: function(playerIDs) {

            // Convert a single player ID to an array when only one player ID is passed in
            playerIDs = ($.isArray(playerIDs)) ? playerIDs : [playerIDs];

            // This is the string we're going to add excluded players to
            var excludedPlayerRows = '';

            // Cache the length of the array of player IDs to speed up the for loop below
            var playerCount = playerIDs.length;

            // Loop through the array of player IDs
            for(var i = 0; i < playerCount; i++) {

                // Get the current player's ID
                var playerID = playerIDs[i];

                // Get the current player's table row in the player pool
                var player = playerPool.getPlayerData(playerID);

                // A temporary div is used so we can strip out any span tags from the player link
                var playerLink = $('<div>').append(player.link).clone().find('span').remove().end().html();

                // Add the player to the HTML string
                excludedPlayerRows = excludedPlayerRows +
				'<div class="span20 playerpool-excludedlist-player" data-pid="' + playerID + '" data-team="' + player.team + '">' +
					'<div class="span2 playerpool-addback"><img src="/images/olineup-addback.png"></div>' +
					'<div class="span8">' + player.link + '</div>' +
					'<div class="span3">' + player.team + '</div>' +
					'<div class="span2">' + player.pos + '</div>' +
					'<div class="span3">' + player.salary + '</div>' +
				'</div>';
            }

            // Now that all the player rows have been combined into one HTML string, add it to the page
			$('#playerpool-excluded-players-list').prepend(excludedPlayerRows);
        },

		// Adds team(s) of players back to the player pool (takes single value or array)
        addTeamsBackToPool: function(teamNames){

            // Convert a single team name to an array when only one team name is passed in
            teamNames = ($.isArray(teamNames)) ? teamNames : [teamNames];

            // This is an array we're going to use to store all the player IDs that need to be added back
            var playersToAddBack = [];

            // Cache the length of the array of teams to speed up the for loop below
            var teamCount = teamNames.length;

            // Loop through the array of team names
            for(var i = 0; i < teamCount; i++) {

                // Get the current team name
                var teamName = teamNames[i];

                // Find the team element on the page
                var $team = $('.playerpool-game-team[data-team="' + teamName + '"]');

                // Visually turn the team back on by removing the opacity class
                $team.removeClass('opacity30');

                // Restore the @ symbol so it's no longer grayed out by removing the opacity class
                $team.siblings('.playerpool-game-at').removeClass('opacity30');

                // Get the page element that contains all the games for a time period
                var $timePeriodGameBox = $team.parents('.playerpool-games-box');

                // Find the time period the game is in by finding the nearest time period box element
                var timePeriod = $timePeriodGameBox.siblings('.playerpool-gametime-box').data('time');

                // If there are no other excluded teams left in the time period, include the whole time period
                if ($team.parents('.playerpool-games-box').find('.playerpool-game-team.opacity30').length === 0) {
                    playerPool.includeTimePeriod(timePeriod);
                }
            }

            // Loop through the excluded players
            $('.playerpool').find('tr.excluded').each(function () {
                var $playerRow = $(this);
                var playerID = $playerRow.data('pid');
                var playerTeam = $playerRow.data('team');
                var playerOnTeamBeingAddedBack = ($.inArray(playerTeam, teamNames) > -1) ? true : false;

                if (playerOnTeamBeingAddedBack) { playersToAddBack.push(playerID); }
            });

            // Add the players back to the player pool
            playerPool.addPlayersBackToPool(playersToAddBack);

            // Make sure that the day toggle links are in the correct state
            playerPool.adjustDayToggleLinks();
        },

		// Make sure that the day toggle link(s) are in the correct state
        adjustDayToggleLinks: function(){

            // Loop through the days
            $('.playerpool-gamedate-row').each(function(){

                // Get the date for this date row
                var day = $(this).find('.playerpool-toggleday').data('day');

                // Check if all the teams with games on this date are excluded
                var allTeamsExcluded = ($('.playerpool-game-team:not(.opacity30)[data-day="' + day + '"]').length === 0) ? true : false;

                // Get the day toggle link element
                var $dayToggleLink = $('.playerpool-toggleday[data-day="' + day + '"]');

                // If all teams are excluded, we want the "Add Day Back" link to show, otherwise show the "Exclude Day" link
                if (allTeamsExcluded) {

                    // Swap out the exclude day class for the include day class
                    $dayToggleLink.addClass('playerpool-includeday').removeClass('playerpool-excludeday').text('Add Day Back');
                }
                else {

                    // Swap out the include day class for the exclude day class
                    $dayToggleLink.addClass('playerpool-excludeday').removeClass('playerpool-includeday').text('Exclude Day');
                }
            });
        },

		// Show/hide the correct players by taking these things into account:
        // 1) The selected position tab
        // 2) The user's search term (if any)
        adjustPlayerPool: function(){

            // Get the position string from the currently selected position tab
            // This could be a single position or
            // it might be a comma-delimited list of positions (ex. the Batters tab might have C,1B,2B,3B,SS,OF)
            var selectedPos = playerPool.getSelectedPosition();

            // Get all the players who are not excluded
            var $eligiblePlayers = $('.playerpool').find('tr:not(.excluded)');

            // Get the contents of the player search box (if any)
            var userSearch = $('#playerpool-playersearch').val();

            // Split the selected position string into an array
            var posList = selectedPos.split(',');

            // Start off with a clean slate by making all the non-excluded players visible
            $eligiblePlayers.removeClass('hidden');

            // Then loop through and hide the players that should be hidden
            $eligiblePlayers.each(function () {

                // The current player's table row
                var $playerRow = $(this);

                // The current player's ID
                var playerID = $playerRow.data('pid');

                // The player's object (contains a bunch of data)
                var player = playerPool.getPlayerData(playerID);

                // Check if the player's name matches the search term (if applicable)
                var nameMatches = (player.name.search(new RegExp(userSearch, "i")) < 0) ? false : true;

                // Check if the All Players tab is selected
                var allPlayersTabSelected = $.inArray('ALL',posList) > -1 ? true : false;

                // Check if the player's position is in the selected position array
                var listedAtSelectedPos = ($.inArray(player.pos,posList) > -1) ? true : false;

                // HIDE THE PLAYER IF THEY MATCH ANY OF THESE CONDITIONS:
                // 1) The player's position is not currently selected and the user is not on the All Players tab
                // 2) There's a search term in the search box and the player's name doesn't match it
                if ( (!listedAtSelectedPos && !allPlayersTabSelected) || (userSearch && !nameMatches) ) {
                     $playerRow.addClass('hidden');
                }
            });
        },

		// Clear the search box
        clearSearch: function(){

            // Clear out the search input box
            $('#playerpool-playersearch').val('');

            // Hide the clear search button
            $('.playerpool-search-clear').addClass('hide');

            // Show/hide the correct players to match the state of the locked positions, selected position tab, and the user's search term (if any)
            playerPool.adjustPlayerPool();
        },

		// Get the total number of seconds given a timestamp in 24 hour format
        convertTimeToSeconds: function(timestamp) {

            // Take the timestamp and break it into hours, minutes and seconds
            var timeParts = timestamp.split(':');
            var hours = timeParts[0];
            var minutes = timeParts[1];
            var seconds = timeParts[2];

            // Add up the seconds and return the total
            return (hours * 3600) + (minutes * 60) + seconds;
        },

		// Equalize the height the time period section and games section
        // This expands the time period click area so it's more user-friendly
        equalizeGameTimeSectionHeights: function(){

            // Loop through all the time period boxes
            $('.playerpool-gametime-box').each(function () {

                // The time period box element
                var $timePeriodBox = $(this);

                // Get the height of the games container next to it
                var gameboxHeight = $timePeriodBox.next('.playerpool-games-box').css('height');

                // Set the height of the time period box to match the height of the games container next to it
                $timePeriodBox.css('height', gameboxHeight);
            });
        },

		// Deactivate games that have already started (unless all the games have been played)
        excludePastGames: function(){

            // Find out if there are any games that haven't started yet (possible values: "Yes","Maybe","No")
            var gamesLeft = $('#playerpool-maxtime').data('gamesleft');

            // This is the array of teams that will need to be excluded
            var teamsToExclude = [];

            // If there are games left on schedule, exclude the games that have already started
            if (gamesLeft === 'Yes' || gamesLeft === 'Maybe' && playerPool.getTimeAtPageLoad() < playerPool.getLatestGameStartTime()) {

                // Loop through all the teams
                $('.playerpool-game-team').each(function(){

                    // The current team element
                    var $team = $(this);

                    // The current team name
                    var teamName = $team.data('team');

                    // Has this game started? (possible values: "Yes","Maybe","No")
                    // This is usually "Maybe", but would be "Yes" if the game date is in the past
                    var hasGameStarted = $team.data('gamedone');

                    // Get the doubleheader value (MLB-only) (possible values: 0,1,2)
                    var doubleHeader = ($team.data('doubleheader')) ? $team.data('doubleheader') : 0;

                    // Get the time that the game starts (24-hour format: 19:00:00)
                    var gameStartTime = playerPool.convertTimeToSeconds($team.data('gametimeonly'));

                    // If the game has started, add the team to the list of teams to exclude
                    if (hasGameStarted === 'Yes' || (hasGameStarted === 'Maybe' && playerPool.getTimeAtPageLoad() >= gameStartTime)) {

                        // Skip the teams in the first game of doubleheader (MLB-only)
                        if (doubleHeader !== 1) { teamsToExclude.push(teamName); }
                    }
                });

                // Exclude the teams in the array
                playerPool.excludeTeams(teamsToExclude);
            }
        },

		// Excludes player(s) from the optimal lineup (takes a single player ID or an array of player IDs)
        excludePlayers: function(playerIDs) {

            // Convert a single player ID to an array when only one player ID is passed in
            playerIDs = ($.isArray(playerIDs)) ? playerIDs : [playerIDs];

            // This is the array of player IDs that will need to be excluded
            var playersToExclude = [];

            // Cache the length of the array of player IDs to speed up the for loop below
            var playerCount = playerIDs.length;

            // Loop through the player IDs to exclude
            for(var i = 0; i < playerCount; i++) {

                // The current player's ID
                var playerID = playerIDs[i];

                // The current player's table row in the player pool
                var $playerRow = playerPool.getPlayerRow(playerID);

                // The current player's object
                var player = playerPool.getPlayerData(playerID);

                // Add the player to the excluded players section on the page
                playersToExclude.push(playerID);

                // Add the excluded class to the player row (in the player pool)
                $playerRow.addClass('excluded');

                // Add the excluded class to the player row (in the optimal lineup table)
                $('#lineup').find('tr[data-pid="' + playerID + '"]').addClass('excluded');
            }

            // Add the players to the excluded players section on the page
            playerPool.addPlayersToExcludedSection(playersToExclude);

        },

		// Excludes entire team(s) from the optimal lineup (takes a single team name an array of team names)
        excludeTeams: function(teamNames){

            // Convert a single team name to an array when only one player ID is passed in
            teamNames = ($.isArray(teamNames)) ? teamNames : [teamNames];

            // This is the array of player IDs that will need to be excluded
            var playersToExclude = [];

            // Cache the length of the array of team names to speed up the for loop below
            var teamCount = teamNames.length;

            // Loop through the array of team names
            for(var i = 0; i < teamCount; i++) {

                // The current team name
                var teamName = teamNames[i];

                // The current team element
                var $team = $('.playerpool-game-team[data-team="' + teamName + '"]');

                // Gray out the team element in the game matchups section
                $team.addClass("opacity30");

                // Check if their opponent in the matchup has been excluded
                var opponentIsExcluded = ($team.siblings('.opacity30').length === 1) ? true : false;

                // If their opponent was already excluded, gray out the @ symbol for the matchup
                if (opponentIsExcluded) {
                    $team.siblings('.playerpool-game-at').addClass('opacity30');
                }

                // Get the page element that contains all the games for a time period
                var $timePeriodGameBox = $team.parents('.playerpool-games-box');

                // Find the time period the game is in by finding the nearest time period box element
                var timePeriod = $timePeriodGameBox.siblings('.playerpool-gametime-box').data('time');

                // If there are no other included teams left in the time period, exclude the whole time period
                if ($team.parents('.playerpool-games-box').find('.playerpool-game-team:not(.opacity30)').length === 0) {
                    playerPool.excludeTimePeriod(timePeriod);
                }
            }

            // Loop through the players who are currently eligible for the optimal lineup
            $('.playerpool').find('tr:not(.excluded)').each(function() {
                var $playerRow = $(this);
                var playerID = $playerRow.data('pid');
                var playerTeam = $playerRow.data('team');
                var playerIsOnExcludedTeam = ($.inArray(playerTeam, teamNames) > -1) ? true : false;

                if (playerIsOnExcludedTeam) { playersToExclude.push(playerID); }
            });

            // Exclude players
            playerPool.excludePlayers(playersToExclude);

            // Make sure that the day toggle links are in the correct state
            playerPool.adjustDayToggleLinks();
        },

		// Exclude a set of games during a time period in or out of the player pool
        excludeTimePeriod: function(clickedTime) {

            // Get the time period box element
            var $timePeriod = $('.playerpool-gametime-box[data-time="' + clickedTime + '"]');

            // Get the games container next to the time period box
            var $gamesBox = $timePeriod.next('.playerpool-games-box');

            // This is an array of the teams that will need to be excluded
            var teamsToExclude = [];

            // Swap out the exclude icon for the include icon in this time period
            $timePeriod.find('.playerpool-timeperiod-icon').attr('src','/images/olineup-add.png').addClass('playerpool-includetime').removeClass('playerpool-excludetime');

            // Gray out all the @ symbols for games in this time period
            $timePeriod.parent().find('.playerpool-game-at').addClass('opacity30');

            // Loop through all the included teams in this time period
            $gamesBox.find('.playerpool-game-team:not(.opacity30)').each(function(){

                // The included team's name
                var teamName = $(this).data('team');

                // Add the team to the array of teams to exclude
                teamsToExclude.push(teamName);
            });

            // Exclude the teams in the array of teams to exclude
            playerPool.excludeTeams(teamsToExclude);
        },

		filterByPos: function(posString){
			playerPool.selectPosTab(posString);
			playerPool.adjustPlayerPool();
		},

		// Get the time of the game with the latest start time (in seconds)
        getLatestGameStartTime: function(){
            return playerPool.convertTimeToSeconds($('#playerpool-maxtime').text());
        },

		getPlayerData: function(playerID) {
			var $player = playerPool.getPlayerRow(playerID);

			var playerTeam = $player.data('team');
			var playerLink = $player.find('.playerpool-name').html();
			var playerName = $.trim($player.find('.playerpool-name').text());
			var playerPos = $player.find('.playerpool-pos').data('pos');
			var playerSalary = $player.find('.playerpool-salary').text();

			return {
				'name': playerName,
				'team': playerTeam,
				'link': playerLink,
				'pos': playerPos,
				'salary': playerSalary
			};
		},

		getPlayerRow: function(playerID) {
			return $('.playerpool').find('tr[data-pid="' + playerID + '"]');
		},

		// Get the currently selected position (set it to 'ALL' as a default)
        getSelectedPosition: function(){
            return $('.playerpool-postab-sel').data('pos') || 'ALL';
        },

		// Get the time that the page was loaded (in seconds)
        getTimeAtPageLoad: function() {
            return playerPool.convertTimeToSeconds($('#playerpool-currenttime').text());
        },

		// Include a set of games during a time period in or out of the player pool
        includeTimePeriod: function(clickedTime) {

            // Get the time period box element for the selected time
            var $timePeriod = $('.playerpool-gametime-box[data-time="' + clickedTime + '"]');

            // Get the games container next to that time period box
            var $gamesBox = $timePeriod.next('.playerpool-games-box');

            // This is an array of teams that will need to be added back
            var teamsToAddBack = [];

            // Swap out the include icon for the exclude icon in this time period
            $timePeriod.find('.playerpool-timeperiod-icon').attr('src','/images/olineup-remove.png').addClass('playerpool-excludetime').removeClass('playerpool-includetime');

            // Restore all the @ symbols for games so they're no longer grayed out in this time period
            $timePeriod.parent().find('.playerpool-game-at').removeClass('opacity30');

            // Loop through the excluded teams in this time period
            $gamesBox.find('.playerpool-game-team.opacity30').each(function(){

                // The current team
                var teamName = $(this).data('team');

                // Add the team to the array of teams to add back
                teamsToAddBack.push(teamName);
            });

            // Add back the teams listed in the teams to add back array
            playerPool.addTeamsBackToPool(teamsToAddBack);
        },

		// Change the selected position tab
        selectPosTab: function(posString){

            // There's no need to do anything if the user is already on the position tab they clicked on
            if (posString === playerPool.getSelectedPosition()) { return; }

            // Get the selected position tab element
            var $posTabToActivate = $('.playerpool-postab[data-pos="' + posString + '"]');

            // Add the selected position class to that position tab
            $posTabToActivate.addClass('playerpool-postab-sel');

            // Remove the selected position class from all the other position tabs
            $posTabToActivate.siblings('.playerpool-postab').removeClass('playerpool-postab-sel');
        },

		toggleTimePeriod: function(time){

			// Get the time period box element that matches the given time
            var $timePeriodBox = $('.playerpool-gametime-box[data-time="' + time + '"]');

            // See if the user is trying to exclude a time period (by checking for the exclude icon)
            var excludeTriggered = ($timePeriodBox.find('.playerpool-excludetime').length) ? true : false;

            // If the user is trying to exclude, exclude the time period. Otherwise, include the time period.
            if (excludeTriggered) {
                playerPool.excludeTimePeriod(time);
            }
            else {
                playerPool.includeTimePeriod(time);
            }
		},

		triggerAddPlayerBack: function(event){
			var playerID = $('.playerpool-excludedlist-player').data('pid');
			playerPool.addPlayersBackToPool(playerID);
		},

		triggerExcludePlayer: function(event){
			var playerID = $(this).parent('tr').data('pid');
			playerPool.excludePlayers(playerID);
		},

		// Triggers a search for player as the user types in the search box
        triggerPlayerSearch: function () {

            // Get the contents of the player search box (if any)
            var userSearch = $('#playerpool-playersearch').val();

            // If there is text in the search box, show the clear search button. Otherwise, hide it.
            if (userSearch) {
                $('.playerpool-search-clear').removeClass('hide');
            }
            else {
                $('.playerpool-search-clear').addClass('hide');
            }

            // Automatically switch the user to the "All Players" tab
            playerPool.selectPosTab('ALL');

            // Show/hide the correct players to match the state of the locked positions, selected position tab, and the user's search term (if any)
            playerPool.adjustPlayerPool();
        },

		triggerPosFilter: function(event){
			var pos = $(this).data('pos');
			playerPool.filterByPos(pos);
		},

		triggerToggleTeam: function(event){
			var $team = $(this);
			var isTeamIncluded = ($team.hasClass('opacity30')) ? false : true;
			var team = $team.data('team');

			if (isTeamIncluded) {
				playerPool.excludeTeams(team);
			}
			else {
				playerPool.addTeamsBackToPool(team);
			}
		},


		triggerTimePeriodToggle: function(event){
			var time = $(this).data('time');
			playerPool.toggleTimePeriod(time);
		},

		activate: function(){

			playerPool.excludePastGames();
			playerPool.equalizeGameTimeSectionHeights();

			$(document).on('click','.playerpool-exclude-player', playerPool.triggerExcludePlayer);
			$(document).on('click','.playerpool-addback', playerPool.triggerAddPlayerBack);
			$(document).on('click','.playerpool-game-team', playerPool.triggerToggleTeam);
			$(document).on('click','.playerpool-postab', playerPool.triggerPosFilter);
			$(document).on('click','.playerpool-gametime-box', playerPool.triggerTimePeriodToggle);

			// Clear Player Search
            $('.playerpool-search-wrapper').on('click', '.playerpool-search-clear', playerPool.clearSearch);

			// Search For Player
            $('#playerpool-playersearch').on('keyup', playerPool.triggerPlayerSearch);
		}
	};

	playerPool.activate();

/**********************************************
 END PLAYER POOL MANAGEMENT
***********************************************/

$(document).on('click','.tablefilter-tab', function(){
	var $selectedfilter = $(this);
	var selectionname = $selectedfilter.data("name");
	$selectedfilter.addClass('tablefilter-tab-sel');

	$selectedfilter.siblings('.tablefilter-tab').removeClass('tablefilter-tab-sel');

	$('.table-tofilter tbody tr').removeClass('hide');
	$('.table-tofilter tbody tr[data-name!="' + selectionname + '"]').addClass('hide');

});

$(document).on('click', '.togglehiderows', function(){
	var selectionname = $(this).data("connectedto");
	$('.' + selectionname).toggleClass('hide');

	var buttontext = $(this).text();
	var othertext = $(this).data("text");
	$(this).text(othertext).data("text", buttontext);
});

});

// Smooth scrolling to anchors
$(function() {
  $('a[href*="#"]:not([href="#"],[href="#myCarousel"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 750);
        return false;
      }
    }
  });
});

// Replace a URL parameter
function replaceUrlParam(url, paramName, paramValue){
    var pattern = new RegExp('('+paramName+'=|'+paramName+'%3D).*?(&|%26|$)');
    var newUrl = url;
    if(url.search(pattern)>=0){
        newUrl = url.replace(pattern,'$1' + paramValue + '$2');
    }
    else {
        newUrl = newUrl + (newUrl.indexOf('?')>0 ? '&' : '?') + paramName + '=' + paramValue;
    }
    return newUrl;
}

// Create or change a cookie
function createCookie(name,value,days) {
    var expires;
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        expires = "; expires="+date.toGMTString();
    }
    else expires = "";
    document.cookie = name+"="+value+expires+"; path=/";
}

// Custom Tablesorter Game Log Date Parser
$.tablesorter.addParser({
  id: 'glog-date',
  is: function(s, table, cell, $cell) {
	var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
	var startsWithShortMonth = ($.inArray(s.split(' ')[0],months) === -1) ? false : true;

	return startsWithShortMonth;
  },
  format: function(s, table, cell, cellIndex) {
	  var months = {
		  'Jan': 1,
		  'Feb': 2,
		  'Mar': 3,
		  'Apr': 4,
		  'May': 5,
		  'Jun': 6,
		  'Jul': 7,
		  'Aug': 8,
		  'Sep': 9,
		  'Oct': 10,
		  'Nov': 11,
		  'Dec': 12
	  };

	  var today = new Date();
	  var currentMonth = today.getMonth() + 1;

	  var monthName = s.split(' ')[0] || '';
	  var month = months[monthName] || 0;
	  var day = s.split(' ')[1] || 0;

	  var yearIndex = (month <= currentMonth) ? 2 : 1;

	  if (String(month).length === 1) { month = '0' + month; }
	  if (day.length === 1) { day = '0' + day; }

	  s = '' + yearIndex + '' + month + '' + day;

    return +s;
  },
  parsed: false,
  type: 'numeric'
});

// Sort column with input fields (numeric values only)
$.tablesorter.addParser({
  id: 'input-num',
  is: function(s, table, cell, $cell) { return false; },
  format: function(s, table, cell, cellIndex) { return $(cell).find('input').val() || s; },
  parsed: false,
  type: 'numeric'
});


/* jshint ignore:start */


//  getQueryParameters.js  Copyright (c) 2014 Nicholas Ortenzio  The MIT License (MIT)
jQuery.extend({
  getQueryParameters : function(str) {
	  return (str || document.location.search).replace(/(^\?)/,'').split("&").map(function(n){return n = n.split("="),this[n[0]] = n[1],this}.bind({}))[0];
  }
});
// AutoComplete Search JS from old version of site
function autoCompleteSearch(e,t){xmlHttp=GetXmlHttpObject();var n="/ajax_getnames-rd.htm";n=n+"?ajaxSearchName="+e;n=n+"&sport="+t;n=n+"&sid="+Math.random();xmlHttp.onreadystatechange=searchStateChanged;xmlHttp.open("GET",n,true);xmlHttp.send(null)}function GetXmlHttpObject(){var e=null;try{e=new XMLHttpRequest}catch(t){try{e=new ActiveXObject("Msxml2.XMLHTTP")}catch(t){e=new ActiveXObject("Microsoft.XMLHTTP")}}return e}function searchStateChanged(){if(xmlHttp.readyState==4){document.getElementById("mainPlayerSearch").innerHTML=xmlHttp.responseText}else{if(xmlHttp.readyState!=0){document.getElementById("mainPlayerSearch").innerHTML='<img src="/images/rw-loading.gif" style="margin-top: 40px; margin-left: 100px;" />'}}}

// toggleItem - used in the app help pages
function getItem(e){var t=false;if(document.getElementById)t=document.getElementById(e);else if(document.all)t=document.all[e];else if(document.layers)t=document.layers[e];return t}function toggleItem(e){itm=getItem(e);if(!itm)return false;if(itm.style.display=="none"){itm.style.display=""}else{itm.style.display="none"}}

// Allow placeholder tag in Internet Explorer
/*! http://mths.be/placeholder v2.0.7 by @mathias */
;(function(f,h,$){var a='placeholder' in h.createElement('input'),d='placeholder' in h.createElement('textarea'),i=$.fn,c=$.valHooks,k,j;if(a&&d){j=i.placeholder=function(){return this};j.input=j.textarea=true}else{j=i.placeholder=function(){var l=this;l.filter((a?'textarea':':input')+'[placeholder]').not('.placeholder').bind({'focus.placeholder':b,'blur.placeholder':e}).data('placeholder-enabled',true).trigger('blur.placeholder');return l};j.input=a;j.textarea=d;k={get:function(m){var l=$(m);return l.data('placeholder-enabled')&&l.hasClass('placeholder')?'':m.value},set:function(m,n){var l=$(m);if(!l.data('placeholder-enabled')){return m.value=n}if(n==''){m.value=n;if(m!=h.activeElement){e.call(m)}}else{if(l.hasClass('placeholder')){b.call(m,true,n)||(m.value=n)}else{m.value=n}}return l}};a||(c.input=k);d||(c.textarea=k);$(function(){$(h).delegate('form','submit.placeholder',function(){var l=$('.placeholder',this).each(b);setTimeout(function(){l.each(e)},10)})});$(f).bind('beforeunload.placeholder',function(){$('.placeholder').each(function(){this.value=''})})}function g(m){var l={},n=/^jQuery\d+$/;$.each(m.attributes,function(p,o){if(o.specified&&!n.test(o.name)){l[o.name]=o.value}});return l}function b(m,n){var l=this,o=$(l);if(l.value==o.attr('placeholder')&&o.hasClass('placeholder')){if(o.data('placeholder-password')){o=o.hide().next().show().attr('id',o.removeAttr('id').data('placeholder-id'));if(m===true){return o[0].value=n}o.focus()}else{l.value='';o.removeClass('placeholder');l==h.activeElement&&l.select()}}}function e(){var q,l=this,p=$(l),m=p,o=this.id;if(l.value==''){if(l.type=='password'){if(!p.data('placeholder-textinput')){try{q=p.clone().attr({type:'text'})}catch(n){q=$('<input>').attr($.extend(g(this),{type:'text'}))}q.removeAttr('name').data({'placeholder-password':true,'placeholder-id':o}).bind('focus.placeholder',b);p.data({'placeholder-textinput':q,'placeholder-id':o}).before(q)}p=p.removeAttr('id').hide().prev().attr('id',o).show()}p.addClass('placeholder');p[0].value=p.attr('placeholder')}else{p.removeClass('placeholder')}}}(this,document,jQuery));

// HTML Truncator for jQuery
// by Henrik Nyh <http://henrik.nyh.se> 2008-02-28.
// Free to modify and redistribute with credit.
(function(factory){if(typeof define==='function'&&define.amd)define(['jquery'],factory);else factory(jQuery)}(function($){var trailing_whitespace=true;$.fn.truncate=function(options){var opts=$.extend({},$.fn.truncate.defaults,options);$(this).each(function(){var content_length=$.trim(squeeze($(this).text())).length;if(content_length<=opts.maxLength)return;var actual_max_length=opts.maxLength-opts.more.length-3;var truncator=(opts.stripFormatting?truncateWithoutFormatting:recursivelyTruncate);var truncated_node=truncator(this,actual_max_length);var full_node=$(this).hide();truncated_node.insertAfter(full_node);findNodeForMore(truncated_node).append(opts.moreSeparator+'<a href="#showMoreContent">'+opts.more+'</a>');if(opts.less)findNodeForLess(full_node).append(opts.lessSeparator+'<a href="#showLessContent">'+opts.less+'</a>');var nodes=truncated_node.add(full_node);var controlLinkSelector='a[href^="#show"][href$="Content"]:last';if(opts.linkClass&&opts.linkClass.length>0)nodes.find(controlLinkSelector).addClass(opts.linkClass);nodes.find(controlLinkSelector).click(function(){nodes.toggle();return false})})};$.fn.truncate.defaults={maxLength:100,more:' read more',less:'',moreSeparator:'...&nbsp;',lessSeparator:'&nbsp;',stripFormatting:false};function truncateWithoutFormatting(node,max_length){return $(node).clone().empty().text(squeeze($(node).text()).slice(0,max_length))}function recursivelyTruncate(node,max_length){return((node.nodeType==3)?truncateText:truncateNode)(node,max_length)}function truncateNode(node,max_length){var node=$(node);var new_node=node.clone().empty();var truncatedChild;node.contents().each(function(){var remaining_length=max_length-new_node.text().length;if(remaining_length===0)return;truncatedChild=recursivelyTruncate(this,remaining_length);if(truncatedChild)new_node.append(truncatedChild)});return new_node}function truncateText(node,max_length){var text=squeeze(node.data);if(trailing_whitespace)text=text.replace(/^ /,'');trailing_whitespace=!!text.match(/ $/);text=text.slice(0,max_length);return $('<div/>').text(text).html()}function squeeze(string){return string.replace(/\s+/g,' ')}function findNodeForMore(node){var isBlock=function(i){var display=$(this).css('display');return(display&&display!='inline')};var child=node.children(":last").filter(isBlock);return child.length>0?findNodeForMore(child):node}function findNodeForLess(node){return $(node.children(":last").filter('p')[0]||node)}}));

/*!
 * Datepicker for Bootstrap v1.5.0-dev (https://github.com/eternicode/bootstrap-datepicker)
 *
 * Copyright 2012 Stefan Petre
 * Improvements by Andrew Rowls
 * Licensed under the Apache License v2.0 (http://www.apache.org/licenses/LICENSE-2.0)
 */
!function(a,b){function c(){return new Date(Date.UTC.apply(Date,arguments))}function d(){var a=new Date;return c(a.getFullYear(),a.getMonth(),a.getDate())}function e(a,b){return a.getUTCFullYear()===b.getUTCFullYear()&&a.getUTCMonth()===b.getUTCMonth()&&a.getUTCDate()===b.getUTCDate()}function f(a){return function(){return this[a].apply(this,arguments)}}function g(b,c){function d(a,b){return b.toLowerCase()}var e,f=a(b).data(),g={},h=new RegExp("^"+c.toLowerCase()+"([A-Z])");c=new RegExp("^"+c.toLowerCase());for(var i in f)c.test(i)&&(e=i.replace(h,d),g[e]=f[i]);return g}function h(b){var c={};if(p[b]||(b=b.split("-")[0],p[b])){var d=p[b];return a.each(o,function(a,b){b in d&&(c[b]=d[b])}),c}}var i=function(){var b={get:function(a){return this.slice(a)[0]},contains:function(a){for(var b=a&&a.valueOf(),c=0,d=this.length;d>c;c++)if(this[c].valueOf()===b)return c;return-1},remove:function(a){this.splice(a,1)},replace:function(b){b&&(a.isArray(b)||(b=[b]),this.clear(),this.push.apply(this,b))},clear:function(){this.length=0},copy:function(){var a=new i;return a.replace(this),a}};return function(){var c=[];return c.push.apply(c,arguments),a.extend(c,b),c}}(),j=function(b,c){this._process_options(c),this.dates=new i,this.viewDate=this.o.defaultViewDate,this.focusDate=null,this.element=a(b),this.isInline=!1,this.isInput=this.element.is("input"),this.component=this.element.hasClass("date")?this.element.find(".add-on, .input-group-addon, .btn"):!1,this.hasInput=this.component&&this.element.find("input").length,this.component&&0===this.component.length&&(this.component=!1),this.picker=a(q.template),this._buildEvents(),this._attachEvents(),this.isInline?this.picker.addClass("datepicker-inline").appendTo(this.element):this.picker.addClass("datepicker-dropdown dropdown-menu"),this.o.rtl&&this.picker.addClass("datepicker-rtl"),this.viewMode=this.o.startView,this.o.calendarWeeks&&this.picker.find("tfoot .today, tfoot .clear").attr("colspan",function(a,b){return parseInt(b)+1}),this._allow_update=!1,this.setStartDate(this._o.startDate),this.setEndDate(this._o.endDate),this.setDaysOfWeekDisabled(this.o.daysOfWeekDisabled),this.setDatesDisabled(this.o.datesDisabled),this.fillDow(),this.fillMonths(),this._allow_update=!0,this.update(),this.showMode(),this.isInline&&this.show()};j.prototype={constructor:j,_process_options:function(e){this._o=a.extend({},this._o,e);var f=this.o=a.extend({},this._o),g=f.language;switch(p[g]||(g=g.split("-")[0],p[g]||(g=n.language)),f.language=g,f.startView){case 2:case"decade":f.startView=2;break;case 1:case"year":f.startView=1;break;default:f.startView=0}switch(f.minViewMode){case 1:case"months":f.minViewMode=1;break;case 2:case"years":f.minViewMode=2;break;default:f.minViewMode=0}f.startView=Math.max(f.startView,f.minViewMode),f.multidate!==!0&&(f.multidate=Number(f.multidate)||!1,f.multidate!==!1&&(f.multidate=Math.max(0,f.multidate))),f.multidateSeparator=String(f.multidateSeparator),f.weekStart%=7,f.weekEnd=(f.weekStart+6)%7;var h=q.parseFormat(f.format);if(f.startDate!==-1/0&&(f.startDate=f.startDate?f.startDate instanceof Date?this._local_to_utc(this._zero_time(f.startDate)):q.parseDate(f.startDate,h,f.language):-1/0),1/0!==f.endDate&&(f.endDate=f.endDate?f.endDate instanceof Date?this._local_to_utc(this._zero_time(f.endDate)):q.parseDate(f.endDate,h,f.language):1/0),f.daysOfWeekDisabled=f.daysOfWeekDisabled||[],a.isArray(f.daysOfWeekDisabled)||(f.daysOfWeekDisabled=f.daysOfWeekDisabled.split(/[,\s]*/)),f.daysOfWeekDisabled=a.map(f.daysOfWeekDisabled,function(a){return parseInt(a,10)}),f.datesDisabled=f.datesDisabled||[],!a.isArray(f.datesDisabled)){var i=[];i.push(q.parseDate(f.datesDisabled,h,f.language)),f.datesDisabled=i}f.datesDisabled=a.map(f.datesDisabled,function(a){return q.parseDate(a,h,f.language)});var j=String(f.orientation).toLowerCase().split(/\s+/g),k=f.orientation.toLowerCase();if(j=a.grep(j,function(a){return/^auto|left|right|top|bottom$/.test(a)}),f.orientation={x:"auto",y:"auto"},k&&"auto"!==k)if(1===j.length)switch(j[0]){case"top":case"bottom":f.orientation.y=j[0];break;case"left":case"right":f.orientation.x=j[0]}else k=a.grep(j,function(a){return/^left|right$/.test(a)}),f.orientation.x=k[0]||"auto",k=a.grep(j,function(a){return/^top|bottom$/.test(a)}),f.orientation.y=k[0]||"auto";else;if(f.defaultViewDate){var l=f.defaultViewDate.year||(new Date).getFullYear(),m=f.defaultViewDate.month||0,o=f.defaultViewDate.day||1;f.defaultViewDate=c(l,m,o)}else f.defaultViewDate=d();f.showOnFocus=f.showOnFocus!==b?f.showOnFocus:!0},_events:[],_secondaryEvents:[],_applyEvents:function(a){for(var c,d,e,f=0;f<a.length;f++)c=a[f][0],2===a[f].length?(d=b,e=a[f][1]):3===a[f].length&&(d=a[f][1],e=a[f][2]),c.on(e,d)},_unapplyEvents:function(a){for(var c,d,e,f=0;f<a.length;f++)c=a[f][0],2===a[f].length?(e=b,d=a[f][1]):3===a[f].length&&(e=a[f][1],d=a[f][2]),c.off(d,e)},_buildEvents:function(){var b={keyup:a.proxy(function(b){-1===a.inArray(b.keyCode,[27,37,39,38,40,32,13,9])&&this.update()},this),keydown:a.proxy(this.keydown,this),paste:a.proxy(this.paste,this)};this.o.showOnFocus===!0&&(b.focus=a.proxy(this.show,this)),this.isInput?this._events=[[this.element,b]]:this.component&&this.hasInput?this._events=[[this.element.find("input"),b],[this.component,{click:a.proxy(this.show,this)}]]:this.element.is("div")?this.isInline=!0:this._events=[[this.element,{click:a.proxy(this.show,this)}]],this._events.push([this.element,"*",{blur:a.proxy(function(a){this._focused_from=a.target},this)}],[this.element,{blur:a.proxy(function(a){this._focused_from=a.target},this)}]),this.o.immediateUpdates&&this._events.push([this.element,{"changeYear changeMonth":a.proxy(function(a){this.update(a.date)},this)}]),this._secondaryEvents=[[this.picker,{click:a.proxy(this.click,this)}],[a(window),{resize:a.proxy(this.place,this)}],[a(document),{mousedown:a.proxy(function(b){this.element.is(b.target)||this.element.find(b.target).length||this.picker.is(b.target)||this.picker.find(b.target).length||a(this.picker).hide()},this)}]]},_attachEvents:function(){this._detachEvents(),this._applyEvents(this._events)},_detachEvents:function(){this._unapplyEvents(this._events)},_attachSecondaryEvents:function(){this._detachSecondaryEvents(),this._applyEvents(this._secondaryEvents)},_detachSecondaryEvents:function(){this._unapplyEvents(this._secondaryEvents)},_trigger:function(b,c){var d=c||this.dates.get(-1),e=this._utc_to_local(d);this.element.trigger({type:b,date:e,dates:a.map(this.dates,this._utc_to_local),format:a.proxy(function(a,b){0===arguments.length?(a=this.dates.length-1,b=this.o.format):"string"==typeof a&&(b=a,a=this.dates.length-1),b=b||this.o.format;var c=this.dates.get(a);return q.formatDate(c,b,this.o.language)},this)})},show:function(){return this.element.attr("readonly")&&this.o.enableOnReadonly===!1?void 0:(this.isInline||this.picker.appendTo(this.o.container),this.place(),this.picker.show(),this._attachSecondaryEvents(),this._trigger("show"),(window.navigator.msMaxTouchPoints||"ontouchstart"in document)&&this.o.disableTouchKeyboard&&a(this.element).blur(),this)},hide:function(){return this.isInline?this:this.picker.is(":visible")?(this.focusDate=null,this.picker.hide().detach(),this._detachSecondaryEvents(),this.viewMode=this.o.startView,this.showMode(),this.o.forceParse&&(this.isInput&&this.element.val()||this.hasInput&&this.element.find("input").val())&&this.setValue(),this._trigger("hide"),this):this},remove:function(){return this.hide(),this._detachEvents(),this._detachSecondaryEvents(),this.picker.remove(),delete this.element.data().datepicker,this.isInput||delete this.element.data().date,this},paste:function(b){var c;if(b.originalEvent.clipboardData&&b.originalEvent.clipboardData.types&&-1!==a.inArray("text/plain",b.originalEvent.clipboardData.types))c=b.originalEvent.clipboardData.getData("text/plain");else{if(!window.clipboardData)return;c=window.clipboardData.getData("Text")}this.setDate(c),this.update(),b.preventDefault()},_utc_to_local:function(a){return a&&new Date(a.getTime()+6e4*a.getTimezoneOffset())},_local_to_utc:function(a){return a&&new Date(a.getTime()-6e4*a.getTimezoneOffset())},_zero_time:function(a){return a&&new Date(a.getFullYear(),a.getMonth(),a.getDate())},_zero_utc_time:function(a){return a&&new Date(Date.UTC(a.getUTCFullYear(),a.getUTCMonth(),a.getUTCDate()))},getDates:function(){return a.map(this.dates,this._utc_to_local)},getUTCDates:function(){return a.map(this.dates,function(a){return new Date(a)})},getDate:function(){return this._utc_to_local(this.getUTCDate())},getUTCDate:function(){var a=this.dates.get(-1);return"undefined"!=typeof a?new Date(a):null},clearDates:function(){var a;this.isInput?a=this.element:this.component&&(a=this.element.find("input")),a&&a.val("").change(),this.update(),this._trigger("changeDate"),this.o.autoclose&&this.hide()},setDates:function(){var b=a.isArray(arguments[0])?arguments[0]:arguments;return this.update.apply(this,b),this._trigger("changeDate"),this.setValue(),this},setUTCDates:function(){var b=a.isArray(arguments[0])?arguments[0]:arguments;return this.update.apply(this,a.map(b,this._utc_to_local)),this._trigger("changeDate"),this.setValue(),this},setDate:f("setDates"),setUTCDate:f("setUTCDates"),setValue:function(){var a=this.getFormattedDate();return this.isInput?this.element.val(a).change():this.component&&this.element.find("input").val(a).change(),this},getFormattedDate:function(c){c===b&&(c=this.o.format);var d=this.o.language;return a.map(this.dates,function(a){return q.formatDate(a,c,d)}).join(this.o.multidateSeparator)},setStartDate:function(a){return this._process_options({startDate:a}),this.update(),this.updateNavArrows(),this},setEndDate:function(a){return this._process_options({endDate:a}),this.update(),this.updateNavArrows(),this},setDaysOfWeekDisabled:function(a){return this._process_options({daysOfWeekDisabled:a}),this.update(),this.updateNavArrows(),this},setDatesDisabled:function(a){this._process_options({datesDisabled:a}),this.update(),this.updateNavArrows()},place:function(){if(this.isInline)return this;var b=this.picker.outerWidth(),c=this.picker.outerHeight(),d=10,e=a(this.o.container).width(),f=a(this.o.container).height(),g=a(this.o.container).scrollTop(),h=a(this.o.container).offset(),i=[];this.element.parents().each(function(){var b=a(this).css("z-index");"auto"!==b&&0!==b&&i.push(parseInt(b))});var j=Math.max.apply(Math,i)+10,k=this.component?this.component.parent().offset():this.element.offset(),l=this.component?this.component.outerHeight(!0):this.element.outerHeight(!1),m=this.component?this.component.outerWidth(!0):this.element.outerWidth(!1),n=k.left-h.left,o=k.top-h.top;this.picker.removeClass("datepicker-orient-top datepicker-orient-bottom datepicker-orient-right datepicker-orient-left"),"auto"!==this.o.orientation.x?(this.picker.addClass("datepicker-orient-"+this.o.orientation.x),"right"===this.o.orientation.x&&(n-=b-m)):k.left<0?(this.picker.addClass("datepicker-orient-left"),n-=k.left-d):n+b>e?(this.picker.addClass("datepicker-orient-right"),n=k.left+m-b):this.picker.addClass("datepicker-orient-left");var p,q,r=this.o.orientation.y;if("auto"===r&&(p=-g+o-c,q=g+f-(o+l+c),r=Math.max(p,q)===q?"top":"bottom"),this.picker.addClass("datepicker-orient-"+r),"top"===r?o+=l:o-=c+parseInt(this.picker.css("padding-top")),this.o.rtl){var s=e-(n+m);this.picker.css({top:o,right:s,zIndex:j})}else this.picker.css({top:o,left:n,zIndex:j});return this},_allow_update:!0,update:function(){if(!this._allow_update)return this;var b=this.dates.copy(),c=[],d=!1;return arguments.length?(a.each(arguments,a.proxy(function(a,b){b instanceof Date&&(b=this._local_to_utc(b)),c.push(b)},this)),d=!0):(c=this.isInput?this.element.val():this.element.data("date")||this.element.find("input").val(),c=c&&this.o.multidate?c.split(this.o.multidateSeparator):[c],delete this.element.data().date),c=a.map(c,a.proxy(function(a){return q.parseDate(a,this.o.format,this.o.language)},this)),c=a.grep(c,a.proxy(function(a){return a<this.o.startDate||a>this.o.endDate||!a},this),!0),this.dates.replace(c),this.dates.length?this.viewDate=new Date(this.dates.get(-1)):this.viewDate<this.o.startDate?this.viewDate=new Date(this.o.startDate):this.viewDate>this.o.endDate&&(this.viewDate=new Date(this.o.endDate)),d?this.setValue():c.length&&String(b)!==String(this.dates)&&this._trigger("changeDate"),!this.dates.length&&b.length&&this._trigger("clearDate"),this.fill(),this},fillDow:function(){var a=this.o.weekStart,b="<tr>";if(this.o.calendarWeeks){this.picker.find(".datepicker-days thead tr:first-child .datepicker-switch").attr("colspan",function(a,b){return parseInt(b)+1});var c='<th class="cw">&#160;</th>';b+=c}for(;a<this.o.weekStart+7;)b+='<th class="dow">'+p[this.o.language].daysMin[a++%7]+"</th>";b+="</tr>",this.picker.find(".datepicker-days thead").append(b)},fillMonths:function(){for(var a="",b=0;12>b;)a+='<span class="month">'+p[this.o.language].monthsShort[b++]+"</span>";this.picker.find(".datepicker-months td").html(a)},setRange:function(b){b&&b.length?this.range=a.map(b,function(a){return a.valueOf()}):delete this.range,this.fill()},getClassNames:function(b){var c=[],d=this.viewDate.getUTCFullYear(),f=this.viewDate.getUTCMonth(),g=new Date;return b.getUTCFullYear()<d||b.getUTCFullYear()===d&&b.getUTCMonth()<f?c.push("old"):(b.getUTCFullYear()>d||b.getUTCFullYear()===d&&b.getUTCMonth()>f)&&c.push("new"),this.focusDate&&b.valueOf()===this.focusDate.valueOf()&&c.push("focused"),this.o.todayHighlight&&b.getUTCFullYear()===g.getFullYear()&&b.getUTCMonth()===g.getMonth()&&b.getUTCDate()===g.getDate()&&c.push("today"),-1!==this.dates.contains(b)&&c.push("active"),(b.valueOf()<this.o.startDate||b.valueOf()>this.o.endDate||-1!==a.inArray(b.getUTCDay(),this.o.daysOfWeekDisabled))&&c.push("disabled"),this.o.datesDisabled.length>0&&a.grep(this.o.datesDisabled,function(a){return e(b,a)}).length>0&&c.push("disabled","disabled-date"),this.range&&(b>this.range[0]&&b<this.range[this.range.length-1]&&c.push("range"),-1!==a.inArray(b.valueOf(),this.range)&&c.push("selected")),c},fill:function(){var d,e=new Date(this.viewDate),f=e.getUTCFullYear(),g=e.getUTCMonth(),h=this.o.startDate!==-1/0?this.o.startDate.getUTCFullYear():-1/0,i=this.o.startDate!==-1/0?this.o.startDate.getUTCMonth():-1/0,j=1/0!==this.o.endDate?this.o.endDate.getUTCFullYear():1/0,k=1/0!==this.o.endDate?this.o.endDate.getUTCMonth():1/0,l=p[this.o.language].today||p.en.today||"",m=p[this.o.language].clear||p.en.clear||"";if(!isNaN(f)&&!isNaN(g)){this.picker.find(".datepicker-days thead .datepicker-switch").text(p[this.o.language].months[g]+" "+f),this.picker.find("tfoot .today").text(l).toggle(this.o.todayBtn!==!1),this.picker.find("tfoot .clear").text(m).toggle(this.o.clearBtn!==!1),this.updateNavArrows(),this.fillMonths();var n=c(f,g-1,28),o=q.getDaysInMonth(n.getUTCFullYear(),n.getUTCMonth());n.setUTCDate(o),n.setUTCDate(o-(n.getUTCDay()-this.o.weekStart+7)%7);var r=new Date(n);r.setUTCDate(r.getUTCDate()+42),r=r.valueOf();for(var s,t=[];n.valueOf()<r;){if(n.getUTCDay()===this.o.weekStart&&(t.push("<tr>"),this.o.calendarWeeks)){var u=new Date(+n+(this.o.weekStart-n.getUTCDay()-7)%7*864e5),v=new Date(Number(u)+(11-u.getUTCDay())%7*864e5),w=new Date(Number(w=c(v.getUTCFullYear(),0,1))+(11-w.getUTCDay())%7*864e5),x=(v-w)/864e5/7+1;t.push('<td class="cw">'+x+"</td>")}if(s=this.getClassNames(n),s.push("day"),this.o.beforeShowDay!==a.noop){var y=this.o.beforeShowDay(this._utc_to_local(n));y===b?y={}:"boolean"==typeof y?y={enabled:y}:"string"==typeof y&&(y={classes:y}),y.enabled===!1&&s.push("disabled"),y.classes&&(s=s.concat(y.classes.split(/\s+/))),y.tooltip&&(d=y.tooltip)}s=a.unique(s),t.push('<td class="'+s.join(" ")+'"'+(d?' title="'+d+'"':"")+">"+n.getUTCDate()+"</td>"),d=null,n.getUTCDay()===this.o.weekEnd&&t.push("</tr>"),n.setUTCDate(n.getUTCDate()+1)}this.picker.find(".datepicker-days tbody").empty().append(t.join(""));var z=this.picker.find(".datepicker-months").find("th:eq(1)").text(f).end().find("span").removeClass("active");if(a.each(this.dates,function(a,b){b.getUTCFullYear()===f&&z.eq(b.getUTCMonth()).addClass("active")}),(h>f||f>j)&&z.addClass("disabled"),f===h&&z.slice(0,i).addClass("disabled"),f===j&&z.slice(k+1).addClass("disabled"),this.o.beforeShowMonth!==a.noop){var A=this;a.each(z,function(b,c){if(!a(c).hasClass("disabled")){var d=new Date(f,b,1),e=A.o.beforeShowMonth(d);e===!1&&a(c).addClass("disabled")}})}t="",f=10*parseInt(f/10,10);var B=this.picker.find(".datepicker-years").find("th:eq(1)").text(f+"-"+(f+9)).end().find("td");f-=1;for(var C,D=a.map(this.dates,function(a){return a.getUTCFullYear()}),E=-1;11>E;E++)C=["year"],-1===E?C.push("old"):10===E&&C.push("new"),-1!==a.inArray(f,D)&&C.push("active"),(h>f||f>j)&&C.push("disabled"),t+='<span class="'+C.join(" ")+'">'+f+"</span>",f+=1;B.html(t)}},updateNavArrows:function(){if(this._allow_update){var a=new Date(this.viewDate),b=a.getUTCFullYear(),c=a.getUTCMonth();switch(this.viewMode){case 0:this.picker.find(".prev").css(this.o.startDate!==-1/0&&b<=this.o.startDate.getUTCFullYear()&&c<=this.o.startDate.getUTCMonth()?{visibility:"hidden"}:{visibility:"visible"}),this.picker.find(".next").css(1/0!==this.o.endDate&&b>=this.o.endDate.getUTCFullYear()&&c>=this.o.endDate.getUTCMonth()?{visibility:"hidden"}:{visibility:"visible"});break;case 1:case 2:this.picker.find(".prev").css(this.o.startDate!==-1/0&&b<=this.o.startDate.getUTCFullYear()?{visibility:"hidden"}:{visibility:"visible"}),this.picker.find(".next").css(1/0!==this.o.endDate&&b>=this.o.endDate.getUTCFullYear()?{visibility:"hidden"}:{visibility:"visible"})}}},click:function(b){b.preventDefault();var d,e,f,g=a(b.target).closest("span, td, th");if(1===g.length)switch(g[0].nodeName.toLowerCase()){case"th":switch(g[0].className){case"datepicker-switch":this.showMode(1);break;case"prev":case"next":var h=q.modes[this.viewMode].navStep*("prev"===g[0].className?-1:1);switch(this.viewMode){case 0:this.viewDate=this.moveMonth(this.viewDate,h),this._trigger("changeMonth",this.viewDate);break;case 1:case 2:this.viewDate=this.moveYear(this.viewDate,h),1===this.viewMode&&this._trigger("changeYear",this.viewDate)}this.fill();break;case"today":var i=new Date;i=c(i.getFullYear(),i.getMonth(),i.getDate(),0,0,0),this.showMode(-2);var j="linked"===this.o.todayBtn?null:"view";this._setDate(i,j);break;case"clear":this.clearDates()}break;case"span":g.hasClass("disabled")||(this.viewDate.setUTCDate(1),g.hasClass("month")?(f=1,e=g.parent().find("span").index(g),d=this.viewDate.getUTCFullYear(),this.viewDate.setUTCMonth(e),this._trigger("changeMonth",this.viewDate),1===this.o.minViewMode?(this._setDate(c(d,e,f)),this.showMode()):this.showMode(-1)):(f=1,e=0,d=parseInt(g.text(),10)||0,this.viewDate.setUTCFullYear(d),this._trigger("changeYear",this.viewDate),2===this.o.minViewMode&&this._setDate(c(d,e,f)),this.showMode(-1)),this.fill());break;case"td":g.hasClass("day")&&!g.hasClass("disabled")&&(f=parseInt(g.text(),10)||1,d=this.viewDate.getUTCFullYear(),e=this.viewDate.getUTCMonth(),g.hasClass("old")?0===e?(e=11,d-=1):e-=1:g.hasClass("new")&&(11===e?(e=0,d+=1):e+=1),this._setDate(c(d,e,f)))}this.picker.is(":visible")&&this._focused_from&&a(this._focused_from).focus(),delete this._focused_from},_toggle_multidate:function(a){var b=this.dates.contains(a);if(a||this.dates.clear(),-1!==b?(this.o.multidate===!0||this.o.multidate>1||this.o.toggleActive)&&this.dates.remove(b):this.o.multidate===!1?(this.dates.clear(),this.dates.push(a)):this.dates.push(a),"number"==typeof this.o.multidate)for(;this.dates.length>this.o.multidate;)this.dates.remove(0)},_setDate:function(a,b){b&&"date"!==b||this._toggle_multidate(a&&new Date(a)),b&&"view"!==b||(this.viewDate=a&&new Date(a)),this.fill(),this.setValue(),b&&"view"===b||this._trigger("changeDate");var c;this.isInput?c=this.element:this.component&&(c=this.element.find("input")),c&&c.change(),!this.o.autoclose||b&&"date"!==b||this.hide()},moveMonth:function(a,c){if(!a)return b;if(!c)return a;var d,e,f=new Date(a.valueOf()),g=f.getUTCDate(),h=f.getUTCMonth(),i=Math.abs(c);if(c=c>0?1:-1,1===i)e=-1===c?function(){return f.getUTCMonth()===h}:function(){return f.getUTCMonth()!==d},d=h+c,f.setUTCMonth(d),(0>d||d>11)&&(d=(d+12)%12);else{for(var j=0;i>j;j++)f=this.moveMonth(f,c);d=f.getUTCMonth(),f.setUTCDate(g),e=function(){return d!==f.getUTCMonth()}}for(;e();)f.setUTCDate(--g),f.setUTCMonth(d);return f},moveYear:function(a,b){return this.moveMonth(a,12*b)},dateWithinRange:function(a){return a>=this.o.startDate&&a<=this.o.endDate},keydown:function(a){if(!this.picker.is(":visible"))return void((40===a.keyCode||27===a.keyCode)&&this.show());var b,c,e,f=!1,g=this.focusDate||this.viewDate;switch(a.keyCode){case 27:this.focusDate?(this.focusDate=null,this.viewDate=this.dates.get(-1)||this.viewDate,this.fill()):this.hide(),a.preventDefault();break;case 37:case 39:if(!this.o.keyboardNavigation)break;b=37===a.keyCode?-1:1,a.ctrlKey?(c=this.moveYear(this.dates.get(-1)||d(),b),e=this.moveYear(g,b),this._trigger("changeYear",this.viewDate)):a.shiftKey?(c=this.moveMonth(this.dates.get(-1)||d(),b),e=this.moveMonth(g,b),this._trigger("changeMonth",this.viewDate)):(c=new Date(this.dates.get(-1)||d()),c.setUTCDate(c.getUTCDate()+b),e=new Date(g),e.setUTCDate(g.getUTCDate()+b)),this.dateWithinRange(e)&&(this.focusDate=this.viewDate=e,this.setValue(),this.fill(),a.preventDefault());break;case 38:case 40:if(!this.o.keyboardNavigation)break;b=38===a.keyCode?-1:1,a.ctrlKey?(c=this.moveYear(this.dates.get(-1)||d(),b),e=this.moveYear(g,b),this._trigger("changeYear",this.viewDate)):a.shiftKey?(c=this.moveMonth(this.dates.get(-1)||d(),b),e=this.moveMonth(g,b),this._trigger("changeMonth",this.viewDate)):(c=new Date(this.dates.get(-1)||d()),c.setUTCDate(c.getUTCDate()+7*b),e=new Date(g),e.setUTCDate(g.getUTCDate()+7*b)),this.dateWithinRange(e)&&(this.focusDate=this.viewDate=e,this.setValue(),this.fill(),a.preventDefault());break;case 32:break;case 13:g=this.focusDate||this.dates.get(-1)||this.viewDate,this.o.keyboardNavigation&&(this._toggle_multidate(g),f=!0),this.focusDate=null,this.viewDate=this.dates.get(-1)||this.viewDate,this.setValue(),this.fill(),this.picker.is(":visible")&&(a.preventDefault(),"function"==typeof a.stopPropagation?a.stopPropagation():a.cancelBubble=!0,this.o.autoclose&&this.hide());break;case 9:this.focusDate=null,this.viewDate=this.dates.get(-1)||this.viewDate,this.fill(),this.hide()}if(f){this._trigger(this.dates.length?"changeDate":"clearDate");var h;this.isInput?h=this.element:this.component&&(h=this.element.find("input")),h&&h.change()}},showMode:function(a){a&&(this.viewMode=Math.max(this.o.minViewMode,Math.min(2,this.viewMode+a))),this.picker.children("div").hide().filter(".datepicker-"+q.modes[this.viewMode].clsName).css("display","block"),this.updateNavArrows()}};var k=function(b,c){this.element=a(b),this.inputs=a.map(c.inputs,function(a){return a.jquery?a[0]:a}),delete c.inputs,m.call(a(this.inputs),c).on("changeDate",a.proxy(this.dateUpdated,this)),this.pickers=a.map(this.inputs,function(b){return a(b).data("datepicker")}),this.updateDates()};k.prototype={updateDates:function(){this.dates=a.map(this.pickers,function(a){return a.getUTCDate()}),this.updateRanges()},updateRanges:function(){var b=a.map(this.dates,function(a){return a.valueOf()});a.each(this.pickers,function(a,c){c.setRange(b)})},dateUpdated:function(b){if(!this.updating){this.updating=!0;var c=a(b.target).data("datepicker"),d=c.getUTCDate(),e=a.inArray(b.target,this.inputs),f=e-1,g=e+1,h=this.inputs.length;if(-1!==e){if(a.each(this.pickers,function(a,b){b.getUTCDate()||b.setUTCDate(d)}),d<this.dates[f])for(;f>=0&&d<this.dates[f];)this.pickers[f--].setUTCDate(d);else if(d>this.dates[g])for(;h>g&&d>this.dates[g];)this.pickers[g++].setUTCDate(d);this.updateDates(),delete this.updating}}},remove:function(){a.map(this.pickers,function(a){a.remove()}),delete this.element.data().datepicker}};var l=a.fn.datepicker,m=function(c){var d=Array.apply(null,arguments);d.shift();var e;return this.each(function(){var f=a(this),i=f.data("datepicker"),l="object"==typeof c&&c;if(!i){var m=g(this,"date"),o=a.extend({},n,m,l),p=h(o.language),q=a.extend({},n,p,m,l);if(f.hasClass("input-daterange")||q.inputs){var r={inputs:q.inputs||f.find("input").toArray()};f.data("datepicker",i=new k(this,a.extend(q,r)))}else f.data("datepicker",i=new j(this,q))}return"string"==typeof c&&"function"==typeof i[c]&&(e=i[c].apply(i,d),e!==b)?!1:void 0}),e!==b?e:this};a.fn.datepicker=m;var n=a.fn.datepicker.defaults={autoclose:!1,beforeShowDay:a.noop,beforeShowMonth:a.noop,calendarWeeks:!1,clearBtn:!1,toggleActive:!1,daysOfWeekDisabled:[],datesDisabled:[],endDate:1/0,forceParse:!0,format:"mm/dd/yyyy",keyboardNavigation:!0,language:"en",minViewMode:0,multidate:!1,multidateSeparator:",",orientation:"auto",rtl:!1,startDate:-1/0,startView:0,todayBtn:!1,todayHighlight:!1,weekStart:0,disableTouchKeyboard:!1,enableOnReadonly:!0,container:"body",immediateUpdates:!1},o=a.fn.datepicker.locale_opts=["format","rtl","weekStart"];a.fn.datepicker.Constructor=j;var p=a.fn.datepicker.dates={en:{days:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],daysShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],daysMin:["Su","Mo","Tu","We","Th","Fr","Sa"],months:["January","February","March","April","May","June","July","August","September","October","November","December"],monthsShort:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],today:"Today",clear:"Clear"}},q={modes:[{clsName:"days",navFnc:"Month",navStep:1},{clsName:"months",navFnc:"FullYear",navStep:1},{clsName:"years",navFnc:"FullYear",navStep:10}],isLeapYear:function(a){return a%4===0&&a%100!==0||a%400===0},getDaysInMonth:function(a,b){return[31,q.isLeapYear(a)?29:28,31,30,31,30,31,31,30,31,30,31][b]},validParts:/dd?|DD?|mm?|MM?|yy(?:yy)?/g,nonpunctuation:/[^ -\/:-@\[\u3400-\u9fff-`{-~\t\n\r]+/g,parseFormat:function(a){var b=a.replace(this.validParts,"\x00").split("\x00"),c=a.match(this.validParts);if(!b||!b.length||!c||0===c.length)throw new Error("Invalid date format.");return{separators:b,parts:c}},parseDate:function(d,e,f){function g(){var a=this.slice(0,m[k].length),b=m[k].slice(0,a.length);return a.toLowerCase()===b.toLowerCase()}if(!d)return b;if(d instanceof Date)return d;"string"==typeof e&&(e=q.parseFormat(e));var h,i,k,l=/([\-+]\d+)([dmwy])/,m=d.match(/([\-+]\d+)([dmwy])/g);if(/^[\-+]\d+[dmwy]([\s,]+[\-+]\d+[dmwy])*$/.test(d)){for(d=new Date,k=0;k<m.length;k++)switch(h=l.exec(m[k]),i=parseInt(h[1]),h[2]){case"d":d.setUTCDate(d.getUTCDate()+i);break;case"m":d=j.prototype.moveMonth.call(j.prototype,d,i);break;case"w":d.setUTCDate(d.getUTCDate()+7*i);break;case"y":d=j.prototype.moveYear.call(j.prototype,d,i)}return c(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate(),0,0,0)}m=d&&d.match(this.nonpunctuation)||[],d=new Date;var n,o,r={},s=["yyyy","yy","M","MM","m","mm","d","dd"],t={yyyy:function(a,b){return a.setUTCFullYear(b)},yy:function(a,b){return a.setUTCFullYear(2e3+b)},m:function(a,b){if(isNaN(a))return a;for(b-=1;0>b;)b+=12;for(b%=12,a.setUTCMonth(b);a.getUTCMonth()!==b;)a.setUTCDate(a.getUTCDate()-1);return a},d:function(a,b){return a.setUTCDate(b)}};t.M=t.MM=t.mm=t.m,t.dd=t.d,d=c(d.getFullYear(),d.getMonth(),d.getDate(),0,0,0);var u=e.parts.slice();if(m.length!==u.length&&(u=a(u).filter(function(b,c){return-1!==a.inArray(c,s)}).toArray()),m.length===u.length){var v;for(k=0,v=u.length;v>k;k++){if(n=parseInt(m[k],10),h=u[k],isNaN(n))switch(h){case"MM":o=a(p[f].months).filter(g),n=a.inArray(o[0],p[f].months)+1;break;case"M":o=a(p[f].monthsShort).filter(g),n=a.inArray(o[0],p[f].monthsShort)+1}r[h]=n}var w,x;for(k=0;k<s.length;k++)x=s[k],x in r&&!isNaN(r[x])&&(w=new Date(d),t[x](w,r[x]),isNaN(w)||(d=w))}return d},formatDate:function(b,c,d){if(!b)return"";"string"==typeof c&&(c=q.parseFormat(c));var e={d:b.getUTCDate(),D:p[d].daysShort[b.getUTCDay()],DD:p[d].days[b.getUTCDay()],m:b.getUTCMonth()+1,M:p[d].monthsShort[b.getUTCMonth()],MM:p[d].months[b.getUTCMonth()],yy:b.getUTCFullYear().toString().substring(2),yyyy:b.getUTCFullYear()};e.dd=(e.d<10?"0":"")+e.d,e.mm=(e.m<10?"0":"")+e.m,b=[];for(var f=a.extend([],c.separators),g=0,h=c.parts.length;h>=g;g++)f.length&&b.push(f.shift()),b.push(e[c.parts[g]]);return b.join("")},headTemplate:'<thead><tr><th class="prev">&#171;</th><th colspan="5" class="datepicker-switch"></th><th class="next">&#187;</th></tr></thead>',contTemplate:'<tbody><tr><td colspan="7"></td></tr></tbody>',footTemplate:'<tfoot><tr><th colspan="7" class="today"></th></tr><tr><th colspan="7" class="clear"></th></tr></tfoot>'};q.template='<div class="datepicker"><div class="datepicker-days"><table class=" table-condensed">'+q.headTemplate+"<tbody></tbody>"+q.footTemplate+'</table></div><div class="datepicker-months"><table class="table-condensed">'+q.headTemplate+q.contTemplate+q.footTemplate+'</table></div><div class="datepicker-years"><table class="table-condensed">'+q.headTemplate+q.contTemplate+q.footTemplate+"</table></div></div>",a.fn.datepicker.DPGlobal=q,a.fn.datepicker.noConflict=function(){return a.fn.datepicker=l,this},a.fn.datepicker.version="1.4.1-dev",a(document).on("focus.datepicker.data-api click.datepicker.data-api",'[data-provide="datepicker"]',function(b){var c=a(this);c.data("datepicker")||(b.preventDefault(),m.call(c,"show"))}),a(function(){m.call(a('[data-provide="datepicker-inline"]'))})}(window.jQuery);

/*
* select plugin
*
* Copyright (c) 2013 Filament Group, Inc.
* Licensed under MIT
*/
(function(e,t){var n="select",r=".universalrank-custbox-custselect",i="",s={select:"custom-"+n,text:"label-text",btn:"btn-"+n};t.fn[n]=function(){return this.each(function(){var e=t(this),n=e.parent().addClass(s.select);if(e.css("opacity")>=.001){var r=e.prev().addClass(s.text),i=function(){return e[0].options[e[0].selectedIndex].value},o=t("<span class='"+s.btn+"'>"+i()+"</span>");e.before(o).bind("change",function(){o.html(i())}).bind("focus",function(){o.addClass("btn-focus")}).bind("blur",function(){o.removeClass("btn-focus")})}else{e.css("opacity","1")}})};t(function(){t(r)[n]()})})(this,jQuery);

/**
* jquery.matchHeight-min.js v0.5.2
* http://brm.io/jquery-match-height/
* License: MIT
*/
(function(b){b.fn.matchHeight=function(a){if("remove"===a){var d=this;this.css("height","");b.each(b.fn.matchHeight._groups,function(b,a){a.elements=a.elements.not(d)});return this}if(1>=this.length)return this;a="undefined"!==typeof a?a:!0;b.fn.matchHeight._groups.push({elements:this,byRow:a});b.fn.matchHeight._apply(this,a);return this};b.fn.matchHeight._apply=function(a,d){var c=b(a),e=[c];d&&(c.css({display:"block","padding-top":"0","padding-bottom":"0","border-top":"0","border-bottom":"0",height:"100px"}),
e=k(c),c.css({display:"","padding-top":"","padding-bottom":"","border-top":"","border-bottom":"",height:""}));b.each(e,function(a,c){var d=b(c),e=0;d.each(function(){var a=b(this);a.css({display:"block",height:""});a.outerHeight(!1)>e&&(e=a.outerHeight(!1));a.css({display:""})});d.each(function(){var a=b(this),c=0;"border-box"!==a.css("box-sizing")&&(c+=g(a.css("border-top-width"))+g(a.css("border-bottom-width")),c+=g(a.css("padding-top"))+g(a.css("padding-bottom")));a.css("height",e-c)})});return this};
b.fn.matchHeight._applyDataApi=function(){var a={};b("[data-match-height], [data-mh]").each(function(){var d=b(this),c=d.attr("data-match-height");a[c]=c in a?a[c].add(d):d});b.each(a,function(){this.matchHeight(!0)})};b.fn.matchHeight._groups=[];b.fn.matchHeight._throttle=80;var h=-1,f=-1;b.fn.matchHeight._update=function(a){if(a&&"resize"===a.type){a=b(window).width();if(a===h)return;h=a}-1===f&&(f=setTimeout(function(){b.each(b.fn.matchHeight._groups,function(){b.fn.matchHeight._apply(this.elements,
this.byRow)});f=-1},b.fn.matchHeight._throttle))};b(b.fn.matchHeight._applyDataApi);b(window).bind("load resize orientationchange",b.fn.matchHeight._update);var k=function(a){var d=null,c=[];b(a).each(function(){var a=b(this),f=a.offset().top-g(a.css("margin-top")),h=0<c.length?c[c.length-1]:null;null===h?c.push(a):1>=Math.floor(Math.abs(d-f))?c[c.length-1]=h.add(a):c.push(a);d=f});return c},g=function(a){return parseFloat(a)||0}})(jQuery);

/*! jquery-dateFormat 18-05-2015 */
var DateFormat={};!function(a){var b=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],c=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],d=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],e=["January","February","March","April","May","June","July","August","September","October","November","December"],f={Jan:"01",Feb:"02",Mar:"03",Apr:"04",May:"05",Jun:"06",Jul:"07",Aug:"08",Sep:"09",Oct:"10",Nov:"11",Dec:"12"},g=/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.?\d{0,3}[Z\-+]?(\d{2}:?\d{2})?/;a.format=function(){function a(a){return b[parseInt(a,10)]||a}function h(a){return c[parseInt(a,10)]||a}function i(a){var b=parseInt(a,10)-1;return d[b]||a}function j(a){var b=parseInt(a,10)-1;return e[b]||a}function k(a){return f[a]||a}function l(a){var b,c,d,e,f,g=a,h="";return-1!==g.indexOf(".")&&(e=g.split("."),g=e[0],h=e[e.length-1]),f=g.split(":"),3===f.length?(b=f[0],c=f[1],d=f[2].replace(/\s.+/,"").replace(/[a-z]/gi,""),g=g.replace(/\s.+/,"").replace(/[a-z]/gi,""),{time:g,hour:b,minute:c,second:d,millis:h}):{time:"",hour:"",minute:"",second:"",millis:""}}function m(a,b){for(var c=b-String(a).length,d=0;c>d;d++)a="0"+a;return a}return{parseDate:function(a){var b,c,d={date:null,year:null,month:null,dayOfMonth:null,dayOfWeek:null,time:null};if("number"==typeof a)return this.parseDate(new Date(a));if("function"==typeof a.getFullYear)d.year=String(a.getFullYear()),d.month=String(a.getMonth()+1),d.dayOfMonth=String(a.getDate()),d.time=l(a.toTimeString()+"."+a.getMilliseconds());else if(-1!=a.search(g))b=a.split(/[T\+-]/),d.year=b[0],d.month=b[1],d.dayOfMonth=b[2],d.time=l(b[3].split(".")[0]);else switch(b=a.split(" "),6===b.length&&isNaN(b[5])&&(b[b.length]="()"),b.length){case 6:d.year=b[5],d.month=k(b[1]),d.dayOfMonth=b[2],d.time=l(b[3]);break;case 2:c=b[0].split("-"),d.year=c[0],d.month=c[1],d.dayOfMonth=c[2],d.time=l(b[1]);break;case 7:case 9:case 10:d.year=b[3],d.month=k(b[1]),d.dayOfMonth=b[2],d.time=l(b[4]);break;case 1:c=b[0].split(""),d.year=c[0]+c[1]+c[2]+c[3],d.month=c[5]+c[6],d.dayOfMonth=c[8]+c[9],d.time=l(c[13]+c[14]+c[15]+c[16]+c[17]+c[18]+c[19]+c[20]);break;default:return null}return d.date=d.time?new Date(d.year,d.month-1,d.dayOfMonth,d.time.hour,d.time.minute,d.time.second,d.time.millis):new Date(d.year,d.month-1,d.dayOfMonth),d.dayOfWeek=String(d.date.getDay()),d},date:function(b,c){try{var d=this.parseDate(b);if(null===d)return b;for(var e,f=d.year,g=d.month,k=d.dayOfMonth,l=d.dayOfWeek,n=d.time,o="",p="",q="",r=!1,s=0;s<c.length;s++){var t=c.charAt(s),u=c.charAt(s+1);if(r)"'"==t?(p+=""===o?"'":o,o="",r=!1):o+=t;else switch(o+=t,q="",o){case"ddd":p+=a(l),o="";break;case"dd":if("d"===u)break;p+=m(k,2),o="";break;case"d":if("d"===u)break;p+=parseInt(k,10),o="";break;case"D":k=1==k||21==k||31==k?parseInt(k,10)+"st":2==k||22==k?parseInt(k,10)+"nd":3==k||23==k?parseInt(k,10)+"rd":parseInt(k,10)+"th",p+=k,o="";break;case"MMMM":p+=j(g),o="";break;case"MMM":if("M"===u)break;p+=i(g),o="";break;case"MM":if("M"===u)break;p+=m(g,2),o="";break;case"M":if("M"===u)break;p+=parseInt(g,10),o="";break;case"y":case"yyy":if("y"===u)break;p+=o,o="";break;case"yy":if("y"===u)break;p+=String(f).slice(-2),o="";break;case"yyyy":p+=f,o="";break;case"HH":p+=m(n.hour,2),o="";break;case"H":if("H"===u)break;p+=parseInt(n.hour,10),o="";break;case"hh":e=0===parseInt(n.hour,10)?12:n.hour<13?n.hour:n.hour-12,p+=m(e,2),o="";break;case"h":if("h"===u)break;e=0===parseInt(n.hour,10)?12:n.hour<13?n.hour:n.hour-12,p+=parseInt(e,10),o="";break;case"mm":p+=m(n.minute,2),o="";break;case"m":if("m"===u)break;p+=n.minute,o="";break;case"ss":p+=m(n.second.substring(0,2),2),o="";break;case"s":if("s"===u)break;p+=n.second,o="";break;case"S":case"SS":if("S"===u)break;p+=o,o="";break;case"SSS":var v="000"+n.millis.substring(0,3);p+=v.substring(v.length-3),o="";break;case"a":p+=n.hour>=12?"PM":"AM",o="";break;case"p":p+=n.hour>=12?"p.m.":"a.m.",o="";break;case"E":p+=h(l),o="";break;case"'":o="",r=!0;break;default:p+=t,o=""}}return p+=q}catch(w){return console&&console.log&&console.log(w),b}},prettyDate:function(a){var b,c,d;return("string"==typeof a||"number"==typeof a)&&(b=new Date(a)),"object"==typeof a&&(b=new Date(a.toString())),c=((new Date).getTime()-b.getTime())/1e3,d=Math.floor(c/86400),isNaN(d)||0>d?void 0:60>c?"just now":120>c?"1 minute ago":3600>c?Math.floor(c/60)+" minutes ago":7200>c?"1 hour ago":86400>c?Math.floor(c/3600)+" hours ago":1===d?"Yesterday":7>d?d+" days ago":31>d?Math.ceil(d/7)+" weeks ago":d>=31?"more than 5 weeks ago":void 0},toBrowserTimeZone:function(a,b){return this.date(new Date(a),b||"MM/dd/yyyy HH:mm:ss")}}}()}(DateFormat),function(a){a.format=DateFormat.format}(jQuery);
/* jshint ignore:end */
