(function (lib, img, cjs, ss) {

var p; // shortcut to reference prototypes
lib.webFontTxtFilters = {}; 

// library properties:
lib.properties = {
	width: 160,
	height: 250,
	fps: 30,
	color: "#FFFFFF",
	webfonts: {},
	manifest: []
};



lib.webfontAvailable = function(family) { 
	lib.properties.webfonts[family] = true;
	var txtFilters = lib.webFontTxtFilters && lib.webFontTxtFilters[family] || [];
	for(var f = 0; f < txtFilters.length; ++f) {
		txtFilters[f].updateCache();
	}
};
// symbols:



(lib.Tween10 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FFFFFF").s().p("AgsgIQAmAJAGheQADBhAqAEQgtgCAABXQgChVgqgQg");

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-4.5,-9.4,9.1,18.8);


(lib.Tween9 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FFFFFF").s().p("AgwgFQArgBAFg4QAAArAxAOQgxAFAAA/QgChCgugCg");

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-4.9,-6.3,9.9,12.6);


(lib.Tween8 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#B9566C").s().p("AioAfIgFgXIE9gnIAeAWIiWApg");
	this.shape.setTransform(-3.2,-12);

	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#B9566C").s().p("AjbBuIgugrIDThmIFAhTIjPDSQgCALgkAIQggAIg5AAQg+AAhZgJg");
	this.shape_1.setTransform(-15.5,1.2);

	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#B9566C").s().p("Ai/gcIARg6IBXgyIB0g8ICjAxIgWBVQgaBLgWgpQgcg5g0gVQg5gYhQAeQhHAagIB6QgEA9ALA5IgLAfg");
	this.shape_2.setTransform(-2.6,-27.8);

	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#B9566C").s().p("AjSBCIBEggQBFgiACAAQADAACfg0IChg2IjQC8IknAZg");
	this.shape_3.setTransform(-16.5,0.1);

	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#B9566C").s().p("AkQDVQANgHACAAIAsgGIDtjWIAygYIDUi0InTGjIhoASIANgGg");
	this.shape_4.setTransform(8.5,-9.8);

	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#503822").s().p("AgTBxQguhJAJhkQABgdAggcQAJgIAMABQALABAGAKQAlA3ADA0QABAAACALIABALQAAAigBAKQgCARgIASQgKATgYAIQgIADgGAAQgMAAgHgMg");
	this.shape_5.setTransform(21.1,0.3);

	this.shape_6 = new cjs.Shape();
	this.shape_6.graphics.f("#000000").s().p("AgvApQgJgIABgJQAOgWAcgUIAxgjQAGAEAHAPQAIANgBAFQgbAcg9AqIgPgNg");
	this.shape_6.setTransform(30.4,-34.4);

	this.shape_7 = new cjs.Shape();
	this.shape_7.graphics.f("#000000").s().p("AAMghQARgQBQhAQA8gxAegmQABAWgEAqQgDArAAAUIAAA4QgBAfgLAWIgIgBQgDgyglg3QgGgKgNgBQgMgCgJAJQggAcgBAdQgEAlANAyQAGAXAWA+IADAKQhBABgXADQghADhHAOQhGANglACg");
	this.shape_7.setTransform(9.3,-4);

	this.shape_8 = new cjs.Shape();
	this.shape_8.graphics.f("#000000").s().p("AhpBhIgEgkIAdgSQAagPAlgfQAqgpAPgMQAogdAeggIjSDqg");
	this.shape_8.setTransform(-0.5,4.4);

	this.shape_9 = new cjs.Shape();
	this.shape_9.graphics.f("#B9566C").s().p("AABgFIAFgBIAJgDQgOALgGAFIgJADg");
	this.shape_9.setTransform(-8.8,9.5);

	this.shape_10 = new cjs.Shape();
	this.shape_10.graphics.f("#B9566C").s().p("AmJFTIgFgQQgDgKAAgHQAOgQAWgQQALgIAdgSQAigXAsgrQAwgwAZgXQATAEAfgCIAxgBQATABAhgHQAjgIAOgBQAugBA0gVQAXgMAcAWQAIgagKghIgUg3QgQgqghgwQgog7gcgEQgjgEgvAMQg3ARgcAHQgKACgbAPQgOCFANBhIgIAFIgLhSQgFgtAAgkQAAhFAdgiQAhgpAbgYQAkggAngOQAngQBPgnQBGgdA2AKQBBANAkA3QAVAgAjBKIgzAjQgcAWgPAWQAAAJAIAIIAQANQA/gpAbgfQAKARAAAbIgoAlQgZAWgOARQgeAlg8AxQhQBAgRAQQgeAggoAdQgQANgjAgQgoAogPANIgKADIgEAAQA9g8AagcQAxg3AWgoQgkAeg3A1IhXBUQgHAHgMACIgWABQgcABgzAFQg4AGgYABQgSABgggEQgkgFgNAAQAcAXAeABQAnACA9gGQBRgIATgBQAIAAA1gKIgRARQhBARhuAEQgxAEgZAAQgrAAgegNgAg2E2IAAAAg");
	this.shape_10.setTransform(-3.1,-22.3);

	this.shape_11 = new cjs.Shape();
	this.shape_11.graphics.f("#B9566C").s().p("AABgDIAJgDQgKAHgJAGg");
	this.shape_11.setTransform(-10.5,10.9);

	this.shape_12 = new cjs.Shape();
	this.shape_12.graphics.f("#B9566C").s().p("AAEgGQARgFgGAHQgFAFgaAIQAIgFAMgKg");
	this.shape_12.setTransform(-7.8,9.2);

	this.shape_13 = new cjs.Shape();
	this.shape_13.graphics.f("#FFFFFF").s().p("Ak2ENIAQgVIDIivIgEkBQAPgTAUgTQApgmAZgCQAPgBCLgRQB7gQACADQADAEAOBfIAMBeIg3CGIg6BPIigCLIhNAZIhlALIh8AGg");
	this.shape_13.setTransform(-11.2,-17.2);

	this.shape_14 = new cjs.Shape();
	this.shape_14.graphics.f("#795730").s().p("AitG4QhSgFg+ABQAYhFAjh5QAvingKgZQAdgCAmgHIBCgMQghgsgPg8QgPg+AIhCQAOh6BOhOQBLhOBfALQBDAIAzA0IATgSQAWAsAPA7QAiBRgLBfQgLBhg3BHQg1BHhKAUQgPATgMAfIhSDsQgaA/gEAFQhggbg9gBg");
	this.shape_14.setTransform(11.5,10.7);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_14},{t:this.shape_13},{t:this.shape_12},{t:this.shape_11},{t:this.shape_10},{t:this.shape_9},{t:this.shape_8},{t:this.shape_7},{t:this.shape_6},{t:this.shape_5},{t:this.shape_4},{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-43.3,-57.5,86.7,115.2);


(lib.Tween7 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#F9BF95").s().p("AgWBWQgYgGgHgVQgJgZACgiQACgNAFgcQgEAZgBAQQgBAhAJAaQAHAUAYAEQAVAEAPgPQAVgSAKgfQAIgXADghQABgogCgOQAEAVgCAnQgGBGgoAiQgLALgMAAQgGAAgHgCg");
	this.shape.setTransform(18,12.8);

	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#F9BF95").s().p("AgTBuQgYgEgHgUQgJgaABghQABgYAHgiIAOgpQADgHAHgKQAJgMAHgFIAIgDIAFgBIAIABIAHACQANAFANALQAKAMAEATQACAOgBAoQgDAhgIAXQgKAfgVASQgMAMgPAAIgJgBg");
	this.shape_1.setTransform(18,10.1);

	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#3CA6CF").s().p("Ag0FBQgbgFgUgRQgMgIgKgRQgGgKgMgcQgLgZgVgpQgzhigOggQgDgigDgOQAHAHANAHIAUAPIAZAXIgJgsQgThHgFhOQAZAPAaAdIAtAyQgGhegBh4IAPgBQATASAUAkIAhA6IAFgDIALhIQAHgqAJgcIACgMQADgIAGACQAJgCAFAJIAIAQQAdBQAMAwQAHgZAXgpQAYgsAHgVQAHgNANAFQAMAFADANQAKAdgCArQAAAYgEAwQASgYAEgCQAOgNAQAMQgDBEgIAoIAMgQQAIgIAJAFQADAWgHAeIgOAwIgNgPIgJgGQgLgGgKAFQgoApgWAVIgoB1QgvB5gkAVQgPAIgSAAIgPgBg");
	this.shape_2.setTransform(0.7,-33);

	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#FADBBE").s().p("AjCHjQgCgBgqABQgpACgDgCQACgOAljOQAljOABgPIgigUQgSgOgJgNIgYgkQgNgWgBgSQgFgZANgUQANgXAZACQgZhmADhkQgBgXAVgbQAbgjAEgKQAOAgAzBiQAVApALAZQAMAcAGAKQAKARAMAIQAUARAbAFQAbAEATgLQAmgVAvh5IAoh1QAWgVAogrQAMgHANALIAFAEIANAQQAwBRAKBsQAXBlgHB3QgEAOgDApQgDAggIAUQghBUgzAZQg2AQgVAUQgYAfgaCNQgZCEgBAAQiOgPhoACgACwikIgHADQgIAFgJAMQgGAJgDAHIgOApQgJApgBATQgDAgAJAZQAIAVAXAGQAXAGAQgOQAngjAHhFQACgngFgVQgEgUgKgLQgMgMgOgFIgGgBIgIgBIgIABg");
	this.shape_3.setTransform(0,15.6);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-30.7,-65.3,61.4,130.6);


(lib.Tween5 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#5ABA88").s().p("AECE0Qg5gGhrggQhTABg7AJQg8AIg3gKQg8gLgtggQgfgUhPglQhQglgWgEQgNAAgKgNIABgCIAAAAQAGgYARglQAhhIA0hBQCmjMEdgaQBVgHBKAFIAfAAIAOAFQCCAUA+BHQAnAtAGA4QAMA/gNAqQgLAbgZAVQgZAVgeAHIg0BXQADAVAAAZQADArAAATQAAAggMAIQgLAGgdAAQgVAAgdgDg");
	this.shape.setTransform(0,-37.9);

	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#000000").s().p("ADhGIIhKgeQhXghhAAWQhSAZhbAdQgIACgijNQgijNgHgBIgRg/QgKgrgFhPQgGhWgFgkIgFhpQAtAgA8ALQA3AKA8gIQBMgMByABQA4ADBKAfQAZAMANAiQALAhAHA1QALBKACAMIgDAeIACIFQgjgHgsgSg");
	this.shape_1.setTransform(3.6,27.4);

	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#FEEBB5").s().p("AjEEOQhShwAAieQAAidBShwQBShwByAAQB0AABRBwQBSBwAACdQAACehSBwQhRBwh0AAQhyAAhShwg");
	this.shape_2.setTransform(-19.8,-13.5);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-50.4,-69.1,101,138.2);


(lib.Tween4 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FEEDCA").s().p("Ag7AxQgkgrgkhmIDQBQIARAMQATAMAKAPQAfAthNAXQgWAGgUAAQg1AAgpgwg");
	this.shape.setTransform(-16.3,18.5);

	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#E65731").s().p("AiNCOQg7g7AAhTQAAhSA7g7QA7g7BSAAQBTAAA7A7QA7A7AABSQAABTg7A7Qg7A7hTAAQhRAAg8g7g");
	this.shape_1.setTransform(8.1,-53.6);

	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#6959A3").s().p("ACSF1QgdgCgugJIg1gMQgSgFgXgRIgpgbQgSgzgGgNQgQgjgZgSQgJgKgRgCIgegBQgQgegGgQQgGgVgTgwQgSgrgFgYQgPhZAYhJIADgIQgYgQgMgcQgMgbAFgcQACgNAIgXQAJgZADgLQAagbAYAHQAeAJAZAdQAKAMAeAsQAagaAPggQAjAiAGAHQAVAaACAbIgzAGQgcAFgTAMQgRAMgIATQgIATACAUQAHBkArBsQAMAfAYAiQAPAXAfAkQAgAuAuAeQAxAhA2AKQAfAFBYgIQgNARgcAWQgZAUgWALQgeAEgPABIgKgBgAjdkWQAKAKAYASQAJAIARgGQAFgOgNgPIgZgVQgOgQglgBQAGATASASg");
	this.shape_2.setTransform(-3.7,-23);

	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#FEEDCA").s().p("ADIGKQgZgChBgQQg+gQhJAEIgNgIQgHgEgHACQgBi9hAjaIgUgZQgpgPgXgHQgkgLgegEQgyhLgQhJIgLgpQgGgYAEgRQAYgSAagaIAAgBIABgBIAWgdQAGAQAQAeQgLAhAHAmQAGAiAVAfQAgAtAigJQANgCAIgOQAFgIAGgSIApAcQAYAQAUAFQAMAEAuAIIBEAMIAzgEQAFARAGA1QAFA2AFAQIBPgLQAcABAOAcQAOAcAcBzQALAsAHBDIANBxQADAXgDAnIgKAJQhWgVgzgGg");
	this.shape_3.setTransform(2.9,31.6);

	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#F9CEA0").s().p("AghAxQgUgfgHghQgHglAMghIAeABQARACAIAKQAYASAQAjQAGANASAxQgHASgEAIQgIAOgOACIgLABQgaAAgbglg");
	this.shape_4.setTransform(-16.7,2.8);

	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#E65731").s().p("ADHE7QgggBgQgCQg2gKgxghQgugeggguQgfgkgPgXQgYgigMgfQgrhsgHhkQgCgUAIgTQAIgTARgMQATgMAcgFIAzgGQgCgbgVgaQgGgHgjgiIEwBwQAjAxAaAZQB4B0gmCkQgWBggzBBQgIAKgXAQQgSgKgdgCgAlfDMQgMgxAIhDIAQhyIBKiJQgYBJAPBZQAFAYASArQATAwAGAVIgXAdIAAABIgBAAQgKALgbAWIgdAXQgJAFgHABIgBAAQgNAAgFgXg");
	this.shape_5.setTransform(-1.8,-24);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_5},{t:this.shape_4},{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-37.7,-73.7,75.6,147.5);


(lib.Tween3 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FADBBE").s().p("ABBD3IiKjNQgbgngmhFQgshTgRgcQgWglgkhgQglhkADgSIJII4QgoBTg/DOIh9i2g");
	this.shape.setTransform(-8,41.5);

	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FADBBE").s().p("AkjjLQgBgNACgGQACgKAUgPQAZgVBFgpQBQgvAfgIQALgBAhAyIAsBFQARgQAIgFQAQgKAQAFQASAFgBA0QAAAZgEAZIgKAlQgGAUgLANQgxAygugEQgDAOAzBFQAxBCAmAnIC5Dig");
	this.shape_1.setTransform(-8,19);

	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#D81236").s().p("ABsELQhFgHifhQQighQghhfQgKgbADgcIAGgWIDdjDQAaBYBAA9QAtAsBRApIB7A7QA7AjARAqIixCbQgCAKgWAAIgNgBg");
	this.shape_2.setTransform(1.2,-57.6);

	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#808083").s().p("AlREFIJ/oyIAkAoIp/Izg");
	this.shape_3.setTransform(3.5,-20.7);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-37.3,-84.4,74.7,168.9);


(lib.Tween2 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FEEDCA").s().p("AAABjQgbARgugSQgKgFgKgLIgRgUQgJgPgIgQQgQgfALgIQAIgHANABQAHABAPAGIAJg5QAGgpAIgDQAWgEA+AHQA3AGAWAGQARAEAEAFQADADADAJQAHAKAFBIQAFBHgDAdg");
	this.shape.setTransform(-7.5,-57.5);

	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FEEDCA").s().p("AhbIOQi6hbCzhyQA4gkgcl5QgsmfgFhUICVgBQAIA1AxDIQA1DUAVB4QBKGdiOAqIAjCSQiAgXhbgtg");
	this.shape_1.setTransform(2.6,9.3);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-21.3,-68.6,42.6,137.3);


(lib.Tween1 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#5ABA88").s().p("AkzDeIinkPQgPgXgLggQgHgVgKgmQgJggghjiQgdjQgDgcIBXidQAsgDBYgKQBMgGA3AEQALABAJAJQAIAIADAMQAHAfABBCQAcAPAVBUQAYBcATAUQAjAkFFGYQFPGhAHAHIusHGIApphg");
	this.shape.setTransform(22.7,68);

	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#2277B8").s().p("AhnFNQgEgMg6guQgegZgGgJIhtieQgGgKgEgLQgJgbALgdQAMgbAcgRIACgBQAQgKAPgDQABgWAMgTQAMgUAVgNIACgBQATgMAWgDIAAgEQAKgkAhgTIADgCQAdgSAiADIg5iwQgLgiATghQATggAmgNIADgBQAkgMAiAQQAjAPALAiIBuFVQAjAMAYAbQAXAZAKAhQAKAdgBAfQgBAOgJA0QgQBSABAPIA7C5IlzB5g");
	this.shape_1.setTransform(-49.4,-99.7);

	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#FADBBE").s().p("Ah9BLQgOgugOhNQgQhcgIghQgJgqgFhnQgFhqAIgQQAEgMADgFQAFgJAYgJQAegLBPgSQBYgVAgACQADABhOAWQhUAYAHATQAWgLAJgCQASgFANAKQAOAKgOAxQgJAZgLAWQgEAHgMAtQgLAngMAHQgVAMBCAZIAoAQQgCATAZBJQAaBNAYAwIBsEPQg/BCh8CyIiEnBgAANjQIABgEQAvAUgDAAQgDAAgqgQgAANjQIAAAAg");
	this.shape_2.setTransform(-28.9,-41.5);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-81.9,-151.1,163.8,302.3);


(lib.Path = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#CED5D8").s().p("AhfBGQgJgNAWgeQAWgbAogdQAmgdAigMQAjgLAJAMQAJANgVAeQgWAbgoAdQgmAdgjAMQgQAFgLAAQgMAAgFgGg");
	this.shape.setTransform(9.9,7.7);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(0,0,19.8,15.3);


(lib.Tween6 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#000000").s().p("Ag+E/QgFgNAGgLQAIgPAWgPQgggRgfgZQgxAjgsALIgLgGQAXgGAZgLQAVgMAagRQghgcghgiQgYAWgbAFQgXACgXgLQgIgEgHgFQgGgEgHgGIgDgGIgDgHIgIgQIAAgCIADACQAMAPAHAGQAMALAMAGQAWALATgEQAXgCAWgVQgigngeguQgZglgRgiQgPghgGggQgFgYABgaIAGgNIAGgLIABgBIAAgDIABgBIABgBQgHAcADAcQADAoAVAtQAQAfAZAnQAdArAhAnQAQgSAKgUQANgaAFgkQAEgZADgsIAFhTQAGgyAKgsQAMgyARgiQAGgNAJgOIAQAAIgLANQgGAJgEAJQgRAigMAxQgKArgFAxIgFBSQgDAsgEAaQgGAmgNAbQgLAWgRAUQAhAkAiAcQBGgzBKheQA8hJA6hcQAPgXAKgWQANgbAGgWQAEgTgBgPIABAAIABACIAEAFIAEAGQgBAfgVAtQgLAWgPAXQg7Bdg7BHQhKBehGA0QAfAYAhAQQAWgOArgVQAegNAzgVIBMggQA/gbAdg6QAOgdACgNIAAADIgFAaIgJAeQgeA0g7AaIhNAfIhQAjQgkAQgWAPQAiAQAnAFQApAHAmgHIgRAHIgSAHQhAADhAggQgaATgFAMQgDAGAAAEQABAFAEAFg");
	this.shape.setTransform(1.2,0);

	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#EC5B33").s().p("AgQFCQhBgDg7gdQg7gdgrgxQgagegSgjIAEAGQAHAHAGADQAGAFAIAEQAXALAYgCQAbgEAYgXQAgAjAiAbQgaARgWAMQgYAMgXAFIALAHQArgMAxgiQAgAYAgARQgXAQgIAPQgFALAEAMIANABQgEgFAAgEQgBgFADgGQAGgMAagSQA/AfBAgDIASgHIARgHQgmAHgpgGQgmgGgkgQQAXgPAkgPIBQgjIBNggQA7gaAfgzIAIgeIAGgbQgGA6gZA0QgdA7gxArQgbAXgfARQgXANgaAJQgzARg1AAIgRAAgAhKDYQBHgzBKhfQA6hGA8heQAPgXAKgWQAVgsACggIgFgGIgEgFIAOAPQAqAwAVA7QAUA8gDA9IgBALQgDANgOAeQgcA5g/AbIhMAgQg0AVgdAOQgrAUgWAPQghgRgggYgAiWCSQARgTALgXQANgbAGglQAFgaACgtIAGhSQAEgxALgrQALgxARgiQAEgJAHgJIALgNIgQABQgKANgGANQgRAjgMAyQgKArgFAyIgFBTQgDAsgEAZQgGAkgNAaQgKAVgPARQgigngcgrQgagmgQggQgVgtgDgoQgCgcAGgbIAAgBQAbgxArglQAwgqA7gVQA8gUA9ADQBBADA7AdQAwAYAlAlQACAPgFATQgFAXgOAbQgKAVgOAXQg6Bdg9BIQhKBehFAzQgjgcghgkgAj6CiQgNgGgMgLQgHgGgMgPIgDgCIgHgRQgUg8ADg9QADhBAdg6IAGgKIgGALIgGANQgCAaAFAZQAGAfAQAhQAQAiAaAmQAdAtAjAnQgXAVgXADIgIAAQgQAAgQgIg");

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-32.2,-32.2,64.6,64.6);


(lib.Tween6_1 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#503822").s().p("Ag9BAIACgdIBXgjIARgoIADgeQAQAXgDAQQgEAfg5ArQgiAcgQAAQgIAAgDgHg");
	this.shape_2.setTransform(3,-47);

	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#503822").s().p("AgUgOIgWhKIBVAcQgDAjABByg");
	this.shape_3.setTransform(1,-20.9);

	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#503822").s().p("Ag+HAQgWgdgXgtIgSgmIAqmwIBsmOIBDAKQAEAOAMAiQALAdAEAaQAJA8gVE9QgYFhgpBiQgUAwgaAAQgbAAgjgvg");
	this.shape_4.setTransform(-7.3,23.7);

	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#503822").s().p("AABBWQhWgIANg4QAEgRAOgTIA9hIIALAKIAbAvQATAhAHAWQARA9hFAAIgSgBg");
	this.shape_5.setTransform(-2.2,-31.8);

	this.instance = new lib.Path();
	this.instance.setTransform(-10,-70.3,1,1,0,0,0,9.9,7.7);

	this.shape_6 = new cjs.Shape();
	this.shape_6.graphics.f("#CED5D8").s().p("AiFBsQgvhGAGghQAJgoBbhGQBThCA7AuQAWASAeAqIA3BQIhPAWIhlA+QgSAYgYANQgQAJgPAAQgeAAgZglg");
	this.shape_6.setTransform(-3.7,-64.9);

	this.shape_7 = new cjs.Shape();
	this.shape_7.graphics.f("#503822").s().p("AgfJ5Qh2gqgFgYQgci8AgjTQAejGBOi5QAXg4AHgdQAKgxgQgnQgIgUgjg2QgdgtgHghQgFgUAKgeQANgmABgLQANAWAXAgIAmA2QAKg0AhgdIAkgkQAVgVATgKQARgGAPAPIAVAdQAAAZgUAdIgjAxIgSAPQgKAJgGAIQgCAPACAgQgBALgIAqQgHAgABAVIAIBPQAFAxAAAeIABAuQAAAagHASIgOAuIgZBLQgPAtgNAeIgaA+QgRAlgEAbQgFAggQAzQgVA+gFATIgKAoQgGAYgJAPIDBDeQgdgUhQgdgABkqHQgHAPAHARQAHARAQACQAWgDANgYQgFgTgUgLQgIgFgHAAQgLAAgHALg");
	this.shape_7.setTransform(-8.3,11.3);

	this.shape_8 = new cjs.Shape();
	this.shape_8.graphics.f("#795730").s().p("AgaALQgGgPAHgPQALgSAUAMQAUALAEARQgNAYgTAEQgQgCgIgSg");
	this.shape_8.setTransform(4.5,-51.6);

	this.shape_9 = new cjs.Shape();
	this.shape_9.graphics.f("#CED5D8").s().p("AhVCRIhriaID2i0ICLDBIjZC6g");
	this.shape_9.setTransform(-0.2,-56.5);

	this.shape_10 = new cjs.Shape();
	this.shape_10.graphics.f("#CED5D8").s().p("AhRCJQgngwhAhlQgvhMBvgrQA4gVBAgGIA+gkQAlA0BBBVQAYAfAIAYQAOAmgzA/Qg9BKhqAWIAAAAQgbAAgug6g");
	this.shape_10.setTransform(5.2,-47.2);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_10},{t:this.shape_9},{t:this.shape_8},{t:this.shape_7},{t:this.shape_6},{t:this.instance},{t:this.shape_5},{t:this.shape_4},{t:this.shape_3},{t:this.shape_2}]}).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-25.1,-79.4,50.3,159);


// stage content:
(lib._160x600 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// timeline functions:
	this.frame_87 = function() {
		contGSAP();
	}
	this.frame_205 = function() {
		contGSAP();
	}
	this.frame_373 = function() {
		this.stop();
	}

	// actions tween:
	this.timeline.addTween(cjs.Tween.get(this).wait(87).call(this.frame_87).wait(118).call(this.frame_205).wait(168).call(this.frame_373).wait(1));

	// Couch
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#A08880").s().p("AiOAnIBcgyQCDhFBogoQAGA9AeBbQgWgGgRAzQkQhLiCB3QAGgpBIgpg");
	this.shape.setTransform(-28.1,177.6,0.307,0.307);

	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#7F7F7F").s().p("AgjA1QgMgBAAgMQgEgBAAgHIAChPIAIgEQAFgCBYACIgRBaQACANgQAAIgzABIgFAAg");
	this.shape_1.setTransform(-18.1,211.7,0.307,0.307);

	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#7F7F7F").s().p("AiyEFQgEgBAAgHIALoEIBkgKIBLACQBIAEAngGQAfAMAYgMQAGACAHABQi3AlgEACQgUAKgEAcIgIBAQgMBygSBtQgMBUgQBSQABANgPAAIg6ABQgMgBAAgMg");
	this.shape_2.setTransform(-26.3,218.6,0.307,0.307);

	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#4D352F").s().p("ACMCnIzDAKIwOgDIpmgFIm7gDQhfAEgegJIgWgQIgnhhIAZgpIgBgXQgChDACgdIACgTQCCAmAbBgQAaBgV9giQAxgBXMAJQCTACAwi7QAgC6B0ACId9gEQDDgBPigPQBTgNAgjeQALAxgBA9IgBANIgDBMQgCBBgDAQQgFAZgDAXQj7gPk5ASI5OAWIgqgCQqugjgjArIkHgNg");
	this.shape_3.setTransform(80.1,173.6,0.307,0.307);

	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#7F7F7F").s().p("AB6EZQgMgCAAgQIg1kkIgYitQgFgbgcgDIhQgNIAAA1QgBAJgLAAIg5gDQgQgCAAgNIgOg/QgRACgCgKIAZgIQAWAPALAAQEUgHAFACQARAHASABIAXHwQABARgDAMQAEAOgPAAIg/AEIgBAAg");
	this.shape_4.setTransform(188.6,218,0.307,0.307);

	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#8C6E64").s().p("Eg5TAQgQgEgBAAgHIALoGIgFABQgdAIgTgNQgsgUgCgyIgEmaQgFkXgDCFIgBAJQAAg0gBgPQgJiRAOh0QAGgpBHgqIBdgzQCFhFBogoIgBgZQgChDACgdIACgTQAEgRAGgOQAvhtAIgRIAFgIQAWgiAqgKQAZgGCMgDQJtgiJcAbIJcgEIAKAAINzAYQCbgIBOAlQBOAmgBBSQAJgkASgUQALgnArgWQATgKAdgHQBJgRFsAeQAcACEKgLQETgKFagOILIgfIPpgZQBUgGA+CyQAHAUAHAaQALAxgBA9QArgMAwAZIBkAyQBPAnBTBKQBRBHABBsIAIGKQgCgEgBCSIgBgvQgBgNgBEnQAEBHgVAcQgKANgjAKQgOAFgPgBIAXHyQABAQgDANQAEAOgPgBIhAAEQgMgBAAgQIg1knIgYitQgFgbgegDIhQgMIAAA1QgBAIgLAAIg5gDQgQgBAAgOIgOg+QgRABgCgJQgaAHgNgGQgGgDABgLQhcAEnzACInlAAQhYgBh4ABQhtAAgCABQgDABhygCIijgDItoACQoWAHgMgEMgshAARQhYgChtABQhYAAgLABIi+ACIgRBcQACANgQAAIg6ABQgMgBAAgMQgEAAAAgHIAChSQgRAHgRgEQi3AlgGACQgUAKgEAcIgIBAQgMBygSBvQgMBUgQBSQABANgPAAIg6ABQgMgBAAgMg");
	this.shape_5.setTransform(80.9,194.2,0.307,0.307);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_5},{t:this.shape_4},{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(374));

	// Far Left Guy
	this.shape_6 = new cjs.Shape();
	this.shape_6.graphics.f("#3CA6CF").s().p("AqVFDQgMgBgPgQQgjgkgLgVQgYgwAphXQASgmA5hWQBaiLCWhUQCWhUCmgEQBqgDCDAgQBQATCYA0QAxAQAWAJQAmAQAbATQA5AmAtBHQAZAnAsBcIAfA6QASAjAEAUQALA+huABIqZAOQkNAEhNADQhzADgYACQhMAIg5AbQgPAHgHAAIAAAAg");
	this.shape_6.setTransform(3,169.1,0.307,0.307);

	this.timeline.addTween(cjs.Tween.get(this.shape_6).wait(374));

	// Left Guy
	this.shape_7 = new cjs.Shape();
	this.shape_7.graphics.f("#5ABA88").s().p("AD7EaQgdgChKACQhBABgmgFQgMgBghABQgdABgQgEQgXgEgoAAQguABgSgCQgQgCggAGQggAFgQgCQhHgGg2AGQgUAFgtgaQgsgZgWAHQgqAEgyAAIhigBIAAnLQAGADCnghQCmggABABQAHAHBegIQBjgJAFACIASAKIB1AGQBFAEAugKQAbgJAbAaIALgMIA4ATQAiAMAXACIACgCQA7AVAxAVQA1AWAGAGQANANhLgCQg+gCAFABQBuAOAUAFQBJAPAvAiQAHAHATADQASACAHAGQAAALgFAkQgEAcADARQARAkAnBiQAmBiARAkQgmgEhDACQhKACgfgCQgbgBhkAFIgwACQguAAghgHg");
	this.shape_7.setTransform(55.6,169.1,0.307,0.307);

	this.shape_8 = new cjs.Shape();
	this.shape_8.graphics.f("#5ABA88").s().p("ACcAKIg4gRIgLAKQgagYgcAJQgsAKhHgEIh1gGIgRgKQADACApgCQAqgCACACQBogDCOAQQAKABBVAeIgCACQgXgCgigMgAjWgWIAAAAIAAAAg");
	this.shape_8.setTransform(57,160.9,0.307,0.307);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_8},{t:this.shape_7}]}).wait(374));

	// Far Right Guy
	this.shape_9 = new cjs.Shape();
	this.shape_9.graphics.f("#B9566C").s().p("AlwGPQlgAChVgFIBRj6IA3gjQAggVAUgSIAigcQAUgRALgMQAMgSAXggIAjg0IAagmQAPgVAPgOQAWgUAVgdQBEg5BPgZQAhgNAtgEIBRgDIAJAAIASACIArAIQAUABAbgJQAcgJA6gZQA4gYAfgJQBKgaBfACQBEACBnATIA6ADQAiABAXAFQAbAHAUB5QAQBbAAApQAsAIAWC7QAWC5gdAfQgFAGgYARQgTANgFAPIgbAUQgoAAgTACIhFgBQgpABgbAJQgeAGhBABQg/ABggAHIiAABQhUAAgtACQhOgEllACg");
	this.shape_9.setTransform(155.9,164.1,0.307,0.307);

	this.timeline.addTween(cjs.Tween.get(this.shape_9).wait(374));

	// Right Girl
	this.shape_10 = new cjs.Shape();
	this.shape_10.graphics.f("#B7DFD9").s().p("ArHDiQAKgvgGiKQgEh2AehVQAnirB5gyQBegmCMAkQAQAEAbAIIA0ASIgCACIASAWIAAABQB/CNBxgmQBDgWAthIIgDgDIAAAAQAHgTAjgRQBEggCKAFQArACAaAIQAiALAYAaQAgAiAlBJQAPAfAOA+IAeCHQAWBZARCWQAMBvAMALI3FAvg");
	this.shape_10.setTransform(97.8,167.3,0.307,0.307);

	this.timeline.addTween(cjs.Tween.get(this.shape_10).wait(374));

	// Far Left Guy Head
	this.instance = new lib.Tween8("synched",0);
	this.instance.setTransform(0.1,166,0.307,0.307,16.9,0,0,-4.7,37.6);

	this.timeline.addTween(cjs.Tween.get(this.instance).to({startPosition:0},87).to({regX:-4.8,rotation:1},22).to({startPosition:0},67).to({regX:-4.7,rotation:16.9},13).to({startPosition:0},80).to({regY:37.8,rotation:0,x:1.2,y:161.1},9).to({regY:37.6,rotation:6},24).to({regY:37.8,rotation:0},22).to({regX:-4.8,rotation:7.7},26).to({regX:-4.7,rotation:0},23).wait(1));

	// Far Left Guy Arm
	this.instance_1 = new lib.Tween6_1("synched",0);
	this.instance_1.setTransform(-12.5,170.8,0.307,0.307,87.7,0,0,-12.5,73.6);

	this.timeline.addTween(cjs.Tween.get(this.instance_1).to({startPosition:0},269).to({regX:-12.6,regY:73.7,rotation:0},9).to({regX:-12.7,regY:73.5,rotation:17.5},24).to({regX:-12.6,regY:73.7,rotation:0},22).to({regX:-12.5,regY:73.5,rotation:17.7},26).to({regX:-12.6,regY:73.7,rotation:0},23).wait(1));

	// Left Guy Head
	this.instance_2 = new lib.Tween7("synched",0);
	this.instance_2.setTransform(52.8,163.9,0.307,0.307,17.9,0,0,-8.6,25.7);

	this.timeline.addTween(cjs.Tween.get(this.instance_2).to({startPosition:0},46).to({regX:-8.5,rotation:-6.8,x:45.3,y:164.5},17).to({rotation:-6.8},78).to({regX:-8.6,rotation:17.9,x:52.8,y:163.9},15).to({startPosition:0},113).to({regX:-8.3,rotation:0,x:57.8,y:153.9},9).to({regX:-8.4,rotation:-5.2,x:55,y:154.1},31).to({regX:-8.3,rotation:0,x:57.8,y:153.9},22).to({regX:-8.4,regY:25.9,rotation:-8.7,x:55.2,y:153},26).to({regX:-8.3,regY:25.7,rotation:0,x:57.8,y:153.9},16).wait(1));

	// Left Guy Arm
	this.instance_3 = new lib.Tween1("synched",0);
	this.instance_3.setTransform(68.9,188.4,0.307,0.307,-61.7,0,0,10.7,65.2);

	this.timeline.addTween(cjs.Tween.get(this.instance_3).to({startPosition:0},269).to({regX:10.4,regY:65,rotation:0,x:39,y:169.3},9).to({regX:10.6,rotation:28.7},24).to({regX:10.4,rotation:0},22).to({regX:10.6,regY:65.1,rotation:33.7},26).to({regX:10.4,regY:65,rotation:0},23).wait(1));

	// Right Girl Head
	this.instance_4 = new lib.Tween4("synched",0);
	this.instance_4.setTransform(101.4,161.1,0.307,0.307,-4.7,0,0,12.1,27.9);

	this.timeline.addTween(cjs.Tween.get(this.instance_4).to({startPosition:0},37).to({regX:12,regY:28.1,rotation:11.5,x:102.5,y:162.2},17).to({startPosition:0},56).to({regX:12.1,regY:27.9,rotation:-4.7,x:101.4,y:161.1},18).to({rotation:-4.7},141).to({regX:12.2,regY:28,rotation:0,x:99,y:158.2},9).to({regX:11.9,rotation:7.2,x:99.9},17).to({regX:12.2,rotation:0,x:99},22).to({regX:12.1,rotation:16.2},26).to({regX:12.2,rotation:0},30).wait(1));

	// Right Girl Arm
	this.instance_5 = new lib.Tween2("synched",0);
	this.instance_5.setTransform(109.7,198.1,0.307,0.307,-18.3,0,0,-0.5,58.5);

	this.timeline.addTween(cjs.Tween.get(this.instance_5).to({startPosition:0},269).to({regX:-0.4,regY:58.2,rotation:0,x:112.1,y:171},9).to({regY:58.1,rotation:-2.9,x:114.1,y:178.6},24).to({regY:58.2,rotation:0,x:112.1,y:171},22).to({x:114.5,y:177.5},26).to({x:112.1,y:171},23).wait(1));

	// Far Right Guy Head
	this.instance_6 = new lib.Tween5("synched",0);
	this.instance_6.setTransform(156.1,158.9,0.307,0.307,-9.2,0,0,-24.5,25);

	this.timeline.addTween(cjs.Tween.get(this.instance_6).to({startPosition:0},269).to({regX:-24.8,regY:25.2,rotation:0,x:155.1,y:154.8},9).to({rotation:8.7},27).to({rotation:0},22).to({rotation:-13.2},26).to({rotation:0},20).wait(1));

	// Far Right Guys Arm
	this.instance_7 = new lib.Tween3("synched",0);
	this.instance_7.setTransform(140.9,175.2,0.307,0.307,-88,0,0,14.2,79.2);

	this.timeline.addTween(cjs.Tween.get(this.instance_7).to({startPosition:0},269).to({regX:14.3,rotation:0},9).to({rotation:-24.2},24).to({rotation:0},22).to({regX:14.1,regY:79.5,rotation:-14},26).to({regX:14.3,regY:79.2,rotation:0},23).wait(1));

	// Layer 32
	this.shape_11 = new cjs.Shape();
	this.shape_11.graphics.f("#3C2F24").s().p("AjyBhIAPhRICjgMIAAhkICBAAIAABkICjAMIAPBRg");
	this.shape_11.setTransform(80.4,173.9);

	this.shape_12 = new cjs.Shape();
	this.shape_12.graphics.f("#FFFFFF").s().p("AgPAEIAAgHIAfAAIAAAHg");
	this.shape_12.setTransform(80.5,162);

	this.shape_13 = new cjs.Shape();
	this.shape_13.graphics.f("#333333").s().p("ABBF4IiBAAIowAAIAArvIThAAIAALvgAgOFmIAfAAIAAgKIgfAAgAo+FGIR9AAIAAqLIx9AAg");
	this.shape_13.setTransform(80.4,126.6);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_13},{t:this.shape_12},{t:this.shape_11}]}).wait(374));

	// hoop
	this.shape_14 = new cjs.Shape();
	this.shape_14.graphics.f("#000000").s().p("AheADIgCgBQAAAAAAAAQgBgBAAAAQAAAAAAgBQAAAAAAAAQAAAAAAAAQAAAAAAAAQAAgBABAAQAAAAAAgBIACAAIC8AAIADAAQAAABAAAAQABAAAAABQAAAAAAAAQAAAAAAAAQAAAAAAAAQAAABAAAAQAAAAgBABQAAAAAAAAIgDABg");
	this.shape_14.setTransform(104.6,116.8);

	this.shape_15 = new cjs.Shape();
	this.shape_15.graphics.f("#F49231").s().p("AAngWIAACNIgWAAIAAguIg/gZIALgLIi4AAQgEAAgCgCQgDgCAAgEQAAgDADgCQACgDAEAAIC+AAIABAAIAtAAIAAisIAWAAIAABkIC+C8IgPAPgAjeAaQAAAAAAABQAAAAgBABQAAAAAAAAQAAABAAAAQAAABAAAAQAAABAAAAQABAAAAAAQAAABAAAAIADABIC+AAIACgBQAAAAABgBQAAAAAAAAQAAAAAAgBQAAAAAAgBQAAAAAAgBQAAAAAAAAQAAgBAAAAQgBgBAAAAIgCAAIi+AAIgDAAg");
	this.shape_15.setTransform(117.2,113.8);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_15},{t:this.shape_14}]}).wait(374));

	// net
	this.shape_16 = new cjs.Shape();
	this.shape_16.graphics.f("#FFFFFF").s().p("AvNVSIiqiaQgcgagDgIQgFgIAAgkQgMmFgklIQgOh0gNhgQgskkhAjyQhTlCh/j+QiFkKjIjvICCABQBsCABPB8QB2C4BbDhIDTiYImtn9ICAAAIGrH0IEqDyIFSj9IjDnoIBwAAIDCHhIFAD+IFKkCIDLndIBtAAIjKHjIE+D2IEnjyIGnnmIB4AAImoHvIDACQQBejaB3izQBNh1Bqh+IB5AAQjEDkiFECQiCD3haE5QhHDqg4FCQg3E2geE0QgNCEgJCSQACAUgQAPIjODEQgxAugmACQgmAAg0grIlDkQIksEOQhLBFgjAFQgvAIhGg/IkykLIk9ERQhKBAgoAFIgIABQgtAAg7g1gAwmOeIAJDOIDACsIFgksIk7kTgAlZPnIFLEeIFQkwIlEkWgAHkPRIFJEVIDAi1IARjKIjdi1gArhKSIE6EQIE8kPIk3kIgABmKOIEsD/IE+kdIkrj2gAwuMhICpiLIjEisQAPCTAMCkgANtJtICdB/QARifAWiRgAlQFIIFQEaIFXkoIlNkRgAxWFNIEoECIE/kFIkmj6gAHxE3IEsD0IEnkIIkpjtgArCAQIEmD3IFJkLIkkjwgABrgGIE5D9IEqj8Ik4j4gAy7jOQAvDOAhDiIEMjRIkykAgANlgIID2DCQAojfA3jKIgngegAw9kuIEwEAIFMkCIkwj5gAkpkyIE1EAIE/kIIk0j2gAHgk7IE4D2IEukDIk0jvgA1CqbQAlBlAcBgIACAGIB6BmIFMj6IkXjmgAqhplIEvD3IFCj8IktjvgABiprIE0D0IExj6IkxjsgANZpyIE0DtIB2hlIACgHQAjhqAjhWIjding");
	this.shape_16.setTransform(104,124,0.048,0.048);

	this.shape_17 = new cjs.Shape();
	this.shape_17.graphics.f("#FFFFFF").s().p("AvFVSQhXhOhchNQgggagDgIQgGgIgEgjQhUmHhvlLQgmh3gZhfQhNkngTjxQgblAg7j7QhCkJi9jrIB/AAQBqCBA6B6QBWC2AnDfQB+hJB8hLQifj+jMj+IB/AAQDKD5ClD6QB+B4CGB8QDHh+C9h+QhCj3hcjzIBvAAQBcDvBED1QCUCBCdCDQC1iBCviEQBzj1BkjuIBsAAQhkDyhwD4QCcB+CmCCQCah8CUh8QDPj9DOj0QA7gBA8ABQjOD4jMEDIDLCXQBTjlBvi3QBHh5Boh+IB5ABQi/Djh0EPQhzEChRFFQhEDyhBE9QhEEsgnEmQgRB+gMCOQAAASgPAQQhpBghmBhQgwAsgmADQgnAAgxgqQiiiIimiFQiRCCiRCJQhLBDghAGQguAHhHg9QiaiFiniFQiRCHiWCJQhJA9gnAHIgIAAQgtAAg6g0gAxSOdQAYBnATBoQBrBVBjBXQCliWCdiVQiwiKi8iKQhqBhhlBjgAlxPpQC2COCoCOQChiYCiiTQisiJi1iKQijCQidCSgAHUPXQCrCICjCIQBehZBihYIAUjDIjjiwQikCJibCLgAs2KTQC8CJCxCJQCOiHCYiDIlnkJQicCAiQCBgAA3KYQCoB/CfB9QCaiKCliIIlEjzQinCFibCEgAx0MfICUiJIjwiuIBcE3gANiKAICjB9QATiaAbiLQhqBUhnBUgAm5FQIGBEcQCliQC1iOQi6iJi1iMQi+CNiuCKgAz5FJIFnEHQCQiBCfh/Qiuh/ilh/QisB7iXB8gAHIFOQCmB5CgB5QCbh+Chh9Qifh4iih4QijB9ieB8gAteATQCjB+CqB+QCniDC0iCQigh7iUh6QjACAi0B+gAAaAKQCqCCCvCCQCdh8Ckh7Qish+ikiAQinB6ijB3gANZAYIELDGQAvjcA4jMIgrggQiiCEilB+gA13jUQAZDOBADkQCEhmCShmQipiDiViDIgxAggAmQkpQCcCDCoCFIFhkFQigh/iWiAQi3CAi4B8gAG2kkQClCACrB/QClh/ChiDIlKj8QikCAioB/gAzjkyQCSCCCjCEQC5h+DAh/QiYiAiMh/QjEB8jGB6gAAwpgQCXB+ChB/IFNj8Qihh9iVh6QikB7irB7gANNpfQCgB8CqB+IB6hoQACgDAAgDQAihuAfhZQh4hYhzhYQiMB2iQB1gAr6piQCJB9CXB/QC6h8C2h/QiRh7iKh5Qi2B5i/B6gA2wqgQAPBkAKBgQACACgBAEIBvBnQDJh5DFh8Qh+h1h3hzQiPBWiTBWg");
	this.shape_17.setTransform(104.1,124,0.048,0.048);

	this.shape_18 = new cjs.Shape();
	this.shape_18.graphics.f("#FFFFFF").s().p("Av1X7QhYhPhahMQgfgagBgGQgGgKgDghQg8l4hYk7QgehxgUhcQhJkSgYk8QggmyhAliQhKlzi7jvIB+AAQBqCCA8CZQBZDiAsE9ID2jOQillmjLkGIB+AAQDMEBCqFeQB/ClCJCvIF/lfQhFlZhej6IBvAAQBeD3BHFUQCVCwCfC2IFglqQBwlRBij2IBsABQhiD5htFXIE/FcQCYiuCVinQDMleDQj5IB3AAQjPD/jMFkQBjBhBnBsQBTk+BwjgQBHiTBqiAQA6AAA/ABQjADkh2FyQh2FjhSGtQhCE2hFErQhREog6EfQgaB7gSCLQgBAQgNASQhtBehjBkQgwAsglAEQgnAAgugoQidiFiciAQiVCBiSCIQhJBCgiAIQgvAGhHg9QiaiEihiDQiYCDiZCHQhKA7gmAIIgIAAQguAAg7g1gAxxRRQASBgAOBnQBnBTBjBXIFQkiQiqiGiyiEQhxBchtBfgAmQSdQCvCKClCNQCjiYCpiQQiiiDiriFQitCMimCNgAGxSHQCfCCCdCFQBehbBjhXQANhfARhgIjRioQisCIieCKgAtBNTQCyCDCrCFQCViCCih/IlXj/QijB8iaB8gAAtNVQCdB6CWB4QCeiJCsiGIkwjoIlNEFgAyJPXICdiCQhxhUhyhSIBGEogANMM0ICWB2QAciXAkiHQhtBUhpBUgAmvIbIFwERQCuiNC4iNIljkNIlzEWgAzwIXIFXD7QCbh7Clh7Qioh8ikh9QisB7ifB5gAHLIQQCdBzCVBzQCeh+Clh8QiXh0ich0IlCD8gAtMDkQCjB9ClB7QCriCC0iEQihh7iViUQi+CdizCAgAAqDVIFQD9IFAj7Qiqh8iiiXQikCVigB8gA1mgYQAdDxA6DWQCGhlCThnQipiDiVifQgbAUgXATgANbDVQCCBgCBBhQAyjSA2jrIgqgmQigCgihCCgAmCiGQCcCjCqCKQCsiKCvinQififiXiuQi0Cxi3CggAzSiNQCSClCkCKQC4iHC+igQiaijiNivQjCCsjDCegAG/iJQChCdCqCDQChiJCeilQilifiginQiiCwijCkgArwopQCLCuCZCnQC4ilC0ixQiViriKioQi1Cpi8CrgAA5opQCXCtChCkQCkioCiivQigiriUinIlKFYgA2mp8QARCLAMCEQACABgBAHQA3BGA5BEQDHiiDDitQiCikh3igIkfDygANPowQCcCqCoCgQA7hEA+hFQADgEAAgFQAhiVAfh6Qh3h4hxh3IkYFGg");
	this.shape_18.setTransform(104.1,124.8,0.048,0.048);

	this.shape_19 = new cjs.Shape();
	this.shape_19.graphics.f("#FFFFFF").s().p("AvcY5QhWhOhVhJQgfgbgBgEQgGgKgEggQg/lkhhkeQgkhqgWhWQhTj7gXlMQginohAmwQhKm5i7jrIB+AAQBpCBA9CrQBZD8AuF+ID4j2QiqmrjKkGQA/AAA/ABQDLD/CvGhQCBDDCQDQIF7mhQhPmYhdj5IBvgBQBdD2BSGTQCbDPCpDXQCwjaCnjTQBgmOBhj0IBsABQhhD5hcGTIFXGZQCOjPCLjDQC2mdDPj2QA6gCA9ACQjPD9i0GjQBqBxBxB+QA7l4Bmj2QBBiiBpiAQA6AABAABQjBDihcGtQhYGng/HeQg4FHhlEYQhyEZhZENQgmBzgcCFQgDAPgOASQhvBbhgBjQgvArghAGQgmgCgsgmQiSiBiTh6QiXB7iRCHQhKBBghAJQgwAFhEg8QiYiDiYh8QiWB8iRCGQhIA6gkAJIgGAAQgtAAg3g1gAxXSgQASBZAPBjQBjBOBfBXQCgiRCkiHQijh+iuh6QhvBXhnBYgAmNTnQCmCACjCMQCkiWCuiIQiah8inh7Qi2CEikCFgAGsTQQCTB5CQCBQBchaBmhTQAThcAahaIi8ibQi1CAihCEgAswOzQCuB5CkB8QCTh7Cph1IlQjsQimB0iYBzgAA8OyQCYBxCMBxQCjiEC1h9QiJhriThrIlgD1gAxxQvQBLg9BPg8QhwhNh1hLQAlCAAmCRgANYONQBFA3BCA3QAriNAziAQh3BQhuBPgAmbKQQC4B/CzB9QC4iEDEiFQith7i3iCQjLCKi4CAgAzfKQQCwB0CpBzQCYhxCnh1IlNjoQiuB2idBxgAHyKAQCWBrCIBqQCnh5Cyh1QiMhtiXhtQiqB9iqB2gAs5FsQCjB3CmByQCxh6C8iBQikh2iZiWQjEChi1B9gABUFXQCtB6CiB2IFSj0Qioh2ioiZQinCaiqB5gA1fB2QAdDxBCDIQCFhgCUhjQith8iYijQgbAVgYAUgAOYFQQCBBaB4BbQBHjFA3jwIgrgnQiiCniqCAgAzJgDQCWCqCoCGQC7iFDCioQigitiQjKQjEDIjHCsgAllgCQChCpCvCFQC2iICyivQinipikjIQiyDPi7CrgAH3gLQCpCiCpB9QCniHCeiuQitioiri/QicDMijCxgArhnYQCQDOCfC1QC6i2C0jRQiejHiRjIQi0DJi6DKgA2io2IAeE9QABABAAAIQA4BPA7BKQDJizDFjOQiHjBh5i/IkgEigABancQChDKCqCzQCli6CajNQisjGiejGQicDLikDLgAN9npQCoDFCzCuQA4hNA+hNQABgFAAgEIAxk5QiCiMh6iLIkHGAg");
	this.shape_19.setTransform(104.1,125.1,0.048,0.048);

	this.shape_20 = new cjs.Shape();
	this.shape_20.graphics.f("#FFFFFF").s().p("AL9Y6QjOiUi7iNQitB4iYCHQhKA/gjAJQgzAFhMg8QiviHi8iHImPECQhkA4gxAIQhCABhQg5Qh1hThnhOQgngdABgEQgHgLABghQgJmBAElBQgBh2AHhdQARkZgIlMQggnRhQlpQhYl/i4jtQA7gBBDABQBnCCA/CcQBcDmA3FJQB0hpB6hqQixl3jFkDQA/ABA/gBQDGD/C1FuQCECtCOC8QDAi6C2i1QhKlwhgj2IBvgCQBhD2BKFqQCSC8CLDFQCkjEC4i9QCBltBmjyIBsABQhmD3iAFzQCPC3CaDTQCji+Chi1QDnmHDKj6QA5gCA/ADQjND/jkGRQBaBxBgB9QBqlsB8jzQBLigBpiAIB6AAQi+DkiRGlQicGbhQHWQg1FBAXE5QgFE1gKEnIgNELQgCAOgNAUQiFBVh7BaQhAAkgtADQgzgHg8gqgAHRTXQDDCQDTCWQB0hSB4hPQAEhiAIhgQiShiiIhgQi+B9i2CCgAnBTWQDICNCwCSQCiicC+iIQi/iQifiHQiuCPjMCNgA1KR0QAABhAGBpQB5BVB/BdQDliQDciMQjIiNjBiMQidBciZBdgAAgOKQCbCAC1CGQCxiEC8h7QjCiFitiBQiwCAieB/gAukN5QC/CLDECMQC9iBCuiAQiviEiwiJQjAB9jPB6gAOdObQBlBEBlBGQAHibAKiMQhtBPhuBOgA1QP3IDdiAQh5hZhuhWQABCPAJCggAm1JBQC9CRCwCNQCiiUC3iGQjBiSiYiNQilCSjICJgAG/JNQC1CBDCCHQClh5Cbh0QjFiHi4iEQiYB4iiB4gA1VIrQCeCDC1CGQDRh4DEh9QiriGidiBQjOB5jSB6gAAPD0QCYCGC8COQCbh6Cbh2QjEiOihiiIklEMgAtND5QCbCDCoCDQDEiDChiHQiRiCiQiZQi5CcjOCDgAR/H+QgBjZAVj0IgtgsQiRCgiTB8IE9DdIAAAAgA1YgXQgGD3ADDfQCqhmCuhlQieiMiCinQgdAVgYATgAGChkQCeCpDECVQCRiFCbifQiqi0iZjBIlLFbgAlyh1QCWCqCTCQIEykyQiXiwh+i6QieC8ioCmgAzAiOQCMCtCaCUQDSiKC4igQiciwiPi9QjBCxjEClgAMcoXQCSDFCrC4QA5hJBAhHQACgGAAgDQAlinAniJIjVkYQibCyiUCygAAdovQCAC+CaC2QChipCsi6QiXjDiGi6QitC1idC3gArfo6QCNC9CYC0QCsisCji7QiEi7iKizQixCxi1CzgA2UqdQAUCPANCPQACAAgBAIQA0BKA6BLQDDioDDi0QiHiwh6ipQiLB8iKB+g");
	this.shape_20.setTransform(104.1,125.1,0.048,0.048);

	this.shape_21 = new cjs.Shape();
	this.shape_21.graphics.f("#FFFFFF").s().p("AMpY3QjjiSjLiMQiyB5iZCGQhOBAgiAJQgyAFhMg8QitiIi4iGImUECQhmA4gvAIQhDgBhPg3Qh0hUhihNQgmgeACgDQgHgLAEghQAWmBAslAQALh4APhcQAqkYgSlNQg/nSh9lnQiDmAi2jrIB9gBQBmCCBKCcQBrDlBbFJQBihqBthpQjPl3jFkCQA+ABBAgBQDFD+DQFuQCNCtCQC9QCqi7Csi0QhRlxhej1QA3gBA5AAQBcD1BPFqQCQC8CCDFQCajFC8i8QCLluBsjxIBsACQhrD2iOFzQCHC2CIDTQCoi9Cti2QEAmHDNj5QA5gDA/AEQjQD/kAGQQBQBxBRB8QCJlrCNjzQBTifBqiAQA6gCBAADQi9Dii5GlQjHGZhdHYQg7FCBKE3QAtEyAoElQALB8AHCOQgDAOgLAUQiJBViIBbQhHAlgwAEQg6gHhAgqgAHbTXQDVCODtCUQB9hTB8hOIgIjCQiohgiZhfQi6B7i4CFgAm9TXQDECNCwCSQChidDAiHQjLiQiZiGQilCOjMCNgA0yR1QgJBhAABoQB0BVB9BeIHGkcQjCiOixiKQieBaidBegAuHN7QCvCJC+CNQC7iCCnh+QipiEijiIQi1B8jOB6gAAWOMQCZB/DCCFQCwiEC4h7QjZiEixiAQikCAiVB/gASHQiQgQicgLiKQhjBPhpBPIDnCIIAAAAgA0tP4IDgiAQhuhahfhUQgNCNgGChgAmoJEIFZEdQCWiUCriFQjBiTiJiMQiVCRi7CKgAGbJQQC7B/DXCGQCbh7CLhyQjaiHi8iCQiLB4iXB5gA0GItQCGCBCkCIQDNh4C7h8QiciIiIiAQjCB5jMB6gAgHD4QCHCFC9COQCQh6CPh3QjFiMiQijQiTCNh7CAgAsYD7QCICECaCDQC3iECSiFQiEiDh/iZQipCbi/CDgARMH/QghjZAPjzIgrgsQiKCfiFB9QCbBqCxByIAAAAgAzsgVQgID4gPDeIFHjLQiLiNh1imIgwAogAFRhhQCPCpDCCVQCFiFCXigQigi1iIjAQiuC3iXClgAljhyQCECqCGCRQB9iQCeiiQiIiyhxi5QiVC7iXCngAxjiMQCBCtCGCUQDCiKCoifQiOiyiMi8QirCxisClgALnoWQCADFCeC4QA5hJBAhHQACgGAAgDQAsioAyiIIi5kXQilCxiZCygAANotQBzC/CNC2QCYipCwi7QiJjEh7i5QivCziVC5gAq7o4QCMC9CKC1QCditCWi7Qh6i8iIiyQioCwifC0gA0Rl2QA1BKA4BLQCpioCri0IkMlZQh8B7hzB/QAhCPAXCPIAAAAQABAAABAIg");
	this.shape_21.setTransform(104.1,125.1,0.048,0.048);

	this.shape_22 = new cjs.Shape();
	this.shape_22.graphics.f("#FFFFFF").s().p("AhTU8Ij3jrIjrDgQg2AzgeADQglADg0gxIiMiGQgXgWgDgIQgDgGgDgfQgklUg1krQgThsgThaQg7kchJjxQhllKiGkQQiQkjjNkNIBzAAQBvCSBTCLQB6DLBkDyICoihImro5IByAAIGTIYIATAWIESEGIEbkNIjHonIBmAAIDDIfIEiEWIEikWIC8ofIBmAAIjAInIEbENIESkGIAUgWIGSoYIBzAAImsI5ICpChQBjjxB7jMQBSiJBviUIB0AAQjOENiQEjQiGEQhkFKQhJDuhAE/Qg7EnglEaQgOB2gOCAQACATgOAMIirCjQgoAmgeAAQgeAAgogmIj/jzIjsDhQg7A4gcADIgHAAQggAAg0gxgAkJQTIEJD+IEKj+IkKkAgAGLQTIEFD4ICeiXIAUiyIixipgAtCPCIAVCyICdCXIEFj4IkGj6gABULpID3DsIEFj6Ij2jrgApQLbIEGD6ID2jsIkFj5gALSLbIB+B5QATiSAXiHgAtPNUIB+h5IipigQAXCHAUCSgAkYGyIEYENIEZkNIkZkNgAGbGyID2DrID+jzIj2jrgAuPGqID+DzID3jrIj/jzgABQB2IEKD+ID/jzIkKj8gApYCBID/DzIEJj+Ij+jxgALaCBIDNDDQArjbA4jKIghgfgAwKhhQA4DKArDbIDOjDIkQkBgAkNi5IENEDIEOkDIkOkCgAGPi5IEKD8IEPkBIkJj+gAuoi+IEPEBIEKj8IkQkDgABAn5IEPECIEPkDIkPkCgApdn6IEPEDIEPkCIkQkDgALgn6IEJD+IBvhpIACgHQAlhvAjhdIjAi4gAyio4QApBqAfBiIADAHIBuBpIEJj+IkBj2g");
	this.shape_22.setTransform(103.9,123.9,0.048,0.048);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[]}).to({state:[{t:this.shape_16,p:{scaleY:0.048,y:124}}]},267).to({state:[{t:this.shape_17}]},1).to({state:[{t:this.shape_18}]},1).to({state:[{t:this.shape_19}]},1).to({state:[{t:this.shape_20}]},1).to({state:[{t:this.shape_21}]},1).to({state:[{t:this.shape_16,p:{scaleY:0.054,y:124.8}}]},1).to({state:[{t:this.shape_22}]},1).wait(100));

	// net
	this.shape_23 = new cjs.Shape();
	this.shape_23.graphics.f("#FFFFFF").s().p("AhTU8Ij3jrIjrDgQg2AzgeADQglADg0gxIiMiGQgXgWgDgIQgDgGgDgfQgklUg1krQgThsgThaQg7kchJjxQhllKiGkQQiQkjjNkNIBzAAQBvCSBTCLQB6DLBkDyICoihImro5IByAAIGTIYIATAWIESEGIEbkNIjHonIBmAAIDDIfIEiEWIEikWIC8ofIBmAAIjAInIEbENIESkGIAUgWIGSoYIBzAAImsI5ICpChQBjjxB7jMQBSiJBviUIB0AAQjOENiQEjQiGEQhkFKQhJDuhAE/Qg7EnglEaQgOB2gOCAQACATgOAMIirCjQgoAmgeAAQgeAAgogmIj/jzIjsDhQg7A4gcADIgHAAQggAAg0gxgAkJQTIEJD+IEKj+IkKkAgAGLQTIEFD4ICeiXIAUiyIixipgAtCPCIAVCyICdCXIEFj4IkGj6gABULpID3DsIEFj6Ij2jrgApQLbIEGD6ID2jsIkFj5gALSLbIB+B5QATiSAXiHgAtPNUIB+h5IipigQAXCHAUCSgAkYGyIEYENIEZkNIkZkNgAGbGyID2DrID+jzIj2jrgAuPGqID+DzID3jrIj/jzgABQB2IEKD+ID/jzIkKj8gApYCBID/DzIEJj+Ij+jxgALaCBIDNDDQArjbA4jKIghgfgAwKhhQA4DKArDbIDOjDIkQkBgAkNi5IENEDIEOkDIkOkCgAGPi5IEKD8IEPkBIkJj+gAuoi+IEPEBIEKj8IkQkDgABAn5IEPECIEPkDIkPkCgApdn6IEPEDIEPkCIkQkDgALgn6IEJD+IBvhpIACgHQAlhvAjhdIjAi4gAyio4QApBqAfBiIADAHIBuBpIEJj+IkBj2g");
	this.shape_23.setTransform(103.9,123.9,0.048,0.048);

	this.timeline.addTween(cjs.Tween.get(this.shape_23).to({_off:true},267).wait(107));

	// ball
	this.instance_8 = new lib.Tween6("synched",0);
	this.instance_8.setTransform(26.1,117.1,0.191,0.191);
	this.instance_8._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_8).wait(257).to({_off:false},0).wait(1).to({x:32,y:112.2},0).wait(1).to({x:38.7,y:107.3},0).wait(1).to({x:46.4,y:102.9},0).wait(1).to({x:55.4,y:99.3},0).wait(1).to({x:65.7,y:97.6},0).wait(1).to({x:76.8,y:98.9},0).wait(1).to({x:87.7,y:103.6},0).wait(1).to({x:97.7,y:111.3},0).wait(1).to({x:103.7,y:117.7},0).wait(1).to({y:121.1},0).wait(1).to({y:124.4},0).wait(1).to({y:127.8},0).wait(1).to({y:131.2},0).wait(1).to({y:134.5},0).wait(1).to({y:137.9},0).wait(1).to({y:141.3},0).wait(1).to({y:144.6},0).wait(1).to({y:148},0).to({_off:true},1).wait(98));

	// TV flashesB
	this.instance_9 = new lib.Tween9("synched",0);
	this.instance_9.setTransform(82.2,125.4,0.218,0.218,0,0,0,0.2,-0.5);
	this.instance_9._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_9).wait(355).to({_off:false},0).to({regX:0.1,regY:-0.6,scaleX:1.77,scaleY:1.77,rotation:360,x:82.1,y:125.5},3).to({_off:true},1).wait(15));

	// TV flashesA
	this.instance_10 = new lib.Tween10("synched",0);
	this.instance_10.setTransform(75.7,111.7,0.182,0.182);
	this.instance_10._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_10).wait(333).to({_off:false},0).to({scaleX:1.49,scaleY:1.49,rotation:-360},3).to({_off:true},1).wait(37));

	// TV flashesB
	this.instance_11 = new lib.Tween9("synched",0);
	this.instance_11.setTransform(77.8,129.7,0.218,0.218,0,0,0,0.2,-0.7);
	this.instance_11._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_11).wait(275).to({_off:false},0).to({regX:0.1,regY:-0.6,scaleX:1.77,scaleY:1.77,rotation:360,y:129.8},3).to({_off:true},1).wait(95));

	// TV flashesA
	this.instance_12 = new lib.Tween10("synched",0);
	this.instance_12.setTransform(75.7,129.2,0.182,0.182);
	this.instance_12._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_12).wait(310).to({_off:false},0).to({scaleX:1.49,scaleY:1.49,rotation:-360},3).to({_off:true},1).wait(60));

	// TV flashesB
	this.instance_13 = new lib.Tween9("synched",0);
	this.instance_13.setTransform(108.3,107.9,0.218,0.218,0,0,0,0.2,-0.7);
	this.instance_13._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_13).wait(290).to({_off:false},0).to({regX:0.1,regY:-0.6,scaleX:1.77,scaleY:1.77,rotation:360,y:108},3).to({_off:true},1).wait(80));

	// TV flashesA
	this.instance_14 = new lib.Tween10("synched",0);
	this.instance_14.setTransform(49.6,111.7,0.182,0.182);
	this.instance_14._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_14).wait(281).to({_off:false},0).to({scaleX:1.49,scaleY:1.49,rotation:-360},3).to({_off:true},1).wait(89));

	// TV flashesB
	this.instance_15 = new lib.Tween9("synched",0);
	this.instance_15.setTransform(47.3,116.7,0.218,0.218,0,0,0,0,-0.5);
	this.instance_15._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_15).wait(269).to({_off:false},0).to({regX:0.1,regY:-0.6,scaleX:1.77,scaleY:1.77,rotation:360},3).to({_off:true},1).wait(101));

	// TV flashesA
	this.instance_16 = new lib.Tween10("synched",0);
	this.instance_16.setTransform(110.6,111.7,0.182,0.182);
	this.instance_16._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_16).wait(273).to({_off:false},0).to({scaleX:1.49,scaleY:1.49,rotation:-360},3).to({_off:true},1).wait(97));

	// TV flashesB
	this.instance_17 = new lib.Tween9("synched",0);
	this.instance_17.setTransform(77.8,116.7,0.218,0.218,0,0,0,0.2,-0.5);
	this.instance_17._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_17).wait(266).to({_off:false},0).to({regX:0.1,regY:-0.6,scaleX:1.77,scaleY:1.77,rotation:360},3).to({_off:true},1).wait(104));

	// TV flashesA
	this.instance_18 = new lib.Tween10("synched",0);
	this.instance_18.setTransform(82.5,114.1,0.182,0.182);
	this.instance_18._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_18).wait(209).to({_off:false},0).to({scaleX:0.87,scaleY:0.87,rotation:-360},3).to({_off:true},1).wait(161));

	// TV flashesA
	this.instance_19 = new lib.Tween10("synched",0);
	this.instance_19.setTransform(110.6,111.7,0.182,0.182);
	this.instance_19._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_19).wait(268).to({_off:false},0).to({scaleX:1.49,scaleY:1.49,rotation:-360},3).to({_off:true},1).wait(102));

	// TV flashesA
	this.instance_20 = new lib.Tween10("synched",0);
	this.instance_20.setTransform(32.5,132.8,0.182,0.182);
	this.instance_20._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_20).wait(171).to({_off:false},0).to({scaleX:1.26,scaleY:1.26,rotation:-360},3).to({_off:true},1).wait(199));

	// TV flashesA
	this.instance_21 = new lib.Tween10("synched",0);
	this.instance_21.setTransform(32.5,124.1,0.182,0.182);
	this.instance_21._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_21).wait(128).to({_off:false},0).to({scaleX:0.87,scaleY:0.87,rotation:-360},3).to({_off:true},1).wait(242));

	// TV flashesB
	this.instance_22 = new lib.Tween9("synched",0);
	this.instance_22.setTransform(57.6,106.8,0.218,0.218,0,0,0,0.2,-0.7);
	this.instance_22._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_22).wait(93).to({_off:false},0).to({regX:0.1,scaleX:1.15,scaleY:1.15,rotation:360,y:106.7},3).to({_off:true},1).wait(277));

	// TV flashesB
	this.instance_23 = new lib.Tween9("synched",0);
	this.instance_23.setTransform(35.8,132.9,0.218,0.218,0,0,0,0,-0.5);
	this.instance_23._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_23).wait(10).to({_off:false},0).to({regX:0.1,regY:-0.7,scaleX:0.87,scaleY:0.87,rotation:360},3).to({_off:true},1).wait(360));

	// TV flashesA
	this.instance_24 = new lib.Tween10("synched",0);
	this.instance_24.setTransform(86.9,111,0.182,0.182);
	this.instance_24._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance_24).wait(36).to({_off:false},0).to({scaleX:0.87,scaleY:0.87,rotation:-360},3).to({_off:true},1).wait(334));

	// TV
	this.shape_24 = new cjs.Shape();
	this.shape_24.graphics.f("#3C2F24").s().p("AsYE9IAzkGIITgqIgCAAIAAlJIGpAAIAAFJIgBAAIISAqIAzEGg");
	this.shape_24.setTransform(80.4,173.9,0.307,0.307);

	this.shape_25 = new cjs.Shape();
	this.shape_25.graphics.f("#FFFFFF").s().p("Ag0AQIAAgfIBpAAIAAAfg");
	this.shape_25.setTransform(80.5,161.9,0.307,0.307);

	this.shape_26 = new cjs.Shape();
	this.shape_26.graphics.f("#1F1812").s().p("A/xTHMAAAgmNMA/jAAAMAAAAmNg");
	this.shape_26.setTransform(80.4,126.6,0.307,0.307);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_26},{t:this.shape_25},{t:this.shape_24}]}).wait(374));

	// Couch Shadow
	this.shape_27 = new cjs.Shape();
	this.shape_27.graphics.f("rgba(0,0,0,0.247)").s().p("At1A7QitgMhfgPQhigPAAgRQAAgQBigQQBfgPCtgMQFwgYIFAAQIGAAFvAYQCuAMBfAPQBiAQAAAQQAAAilvAZQlvAZoGAAQoFAAlwgZg");
	this.shape_27.setTransform(85.4,222.3);

	this.timeline.addTween(cjs.Tween.get(this.shape_27).wait(374));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(40.1,214,250.6,141.8);

})(lib = lib||{}, images = images||{}, createjs = createjs||{}, ss = ss||{});
var lib, images, createjs, ss;