var BubblesCanvas = BubblesCanvas || {};
(function() {

	const colors_hex = ['#d84949', '#4850d8', '#ce48d8', '#5bd848', '#d8d348', '#3bccc2', '#d8a848','#6c5424'];
	const colors_rgb = ['216,73,73','72,80,216','206,72,216','91,216,72','216,211,72','59,204,194','216,168,72','108,84,36'];

	let ctx
	let width;
	let height;
	let minPayoff;
	let maxPayoff;
	let ymax;
	let ymin;
	const mrg = 10;

	function draw(context, group) {
		ctx = context;
		width = ctx.canvas.width;
		height = ctx.canvas.height;

		// background
		ctx.fillStyle = 'black';
		ctx.fillRect(0, 0, width, height);
		ctx.clearRect(mrg, mrg,(width - 2*mrg), (height - 2*mrg));

		//scale plot area
		minPayoff = 0;
		maxPayoff = 0;
		for (let key in group) {
			maxPayoff = Math.max(group[key].payoff, maxPayoff);
			minPayoff = Math.min(minPayoff, group[key].payoff)
		}
		maxPayoff = Math.ceil((1.1 * maxPayoff / 20)) * 20;//round up to nearest ...
		minPayoff = Math.ceil(((-1.1 * minPayoff) / 20)) * 20;//round up to nearest ...
		minPayoff = -1 * minPayoff;
		ymin = minPayoff;
		ymax = maxPayoff + 2;

		// add grid lines to plot
		// base grid lines on range
		gridrange = ymax - ymin;
		gridrange = gridrange / 5;  
		gridrange = gridrange.toFixed(0);


		// console.log("minGrid: " + minGrid + " gridrange: " + gridrange);

		let ylevel = 0;
		let logger = ""
		for (var i = 0; i < 6; i++){

			ylevel = (i * gridrange + ymin); // ensure min grid is round number
	    	ylevel_text = ylevel;
	    	logger = logger + ", " + ylevel;


		 	ctx.font = "18px Ariel";
			ctx.fillStyle = "#cccccc";
			ctx.fillText(ylevel_text, 20, 2+ mrg + (height - 2*mrg) * (1 - val_to_y(ylevel)));

			hline_at(val_to_y(ylevel));


		}

		ctx.font = "18px Ariel";
		ctx.setLineDash([5, 15, 25]);
		ctx.fillStyle = "#cccccc";
		ctx.fillText("", 20, mrg + (height - 2*mrg) * (1 - val_to_y(0)));
		hline_at(val_to_y(0));

		// plot player positions on x, y
		player_locations(group);	



	};

	function val_to_y(val){
		// requires correct ymin and ymax

		y = (val - ymin) / (ymax - ymin);
		return y;


	};

	function hline_at(ylevel){
	    
	    ylevel = mrg + (height - 2*mrg) * (1 - ylevel); // x coord for p1

		ctx.strokeStyle = "#e8e8e8";
	    ctx.setLineDash([0, 0]);
		ctx.beginPath();
		ctx.moveTo(0,  ylevel);
		ctx.lineTo(width, ylevel);
		ctx.stroke();
	};

	function player_locations(group) {
		for (let key in group) {

			if (group[key].id == oTree.idInGroup){
				ownDot(
					group[key].x,
					val_to_y(group[key].payoff),
					mrg,
					group[key].id
				);
			} else {
				playerDot(
					group[key].x,
					val_to_y(group[key].payoff),
					mrg,
					group[key].id
				);
			}
		};

	}

	function color_concat_rgba(id, alpha){
		return 'rgba(' + colors_rgb[id-1] + "," + alpha + ')';
	}

	function playerDot(x, y, mrg, player_id) {

	    x = (mrg + ((width - 2*mrg)) * x); // y coord for p1
	    y = mrg + (height - 2*mrg) * (1 - y); // x coord for p1

	    ctx.strokeStyle = "#666666"; // 🤘
	    ctx.setLineDash([0, 0]);
	    ctx.beginPath();
	    ctx.moveTo((x + 7), y);
	    ctx.arc(x, y, 7, 0, Math.PI*2, true);  // eye
	    ctx.fillStyle = color_concat_rgba(player_id, 0.6);
	    ctx.fill();
	    ctx.stroke();
	}

	function ownDot(x, y, mrg, player_id) {




	    x = (mrg + ((width - 2*mrg)) * x); // y coord for p1
	    y = mrg + (height - 2*mrg) * (1 - y); // x coord for p1

	    //virtical line - indicating location
	    ctx.strokeStyle = "#cccccc";
	    ctx.setLineDash([5, 3]);/*dashes are 5px and spaces are 3px*/
		ctx.beginPath();
		ctx.moveTo(x, height-mrg);
		ctx.lineTo(x, mrg);
		ctx.stroke();

		// circle
	    ctx.strokeStyle = "#666666"; // 🤘
	    ctx.setLineDash([0, 0]);
	    ctx.beginPath();
	    ctx.moveTo((x + 8), y);
	    ctx.arc(x, y, 8, 0, Math.PI*2, true);  // eye
	    ctx.fillStyle = 'rgba(65, 97, 255, 0.5)';
	    ctx.fill();
	    ctx.stroke();





		}



	BubblesCanvas.draw = draw;
})();