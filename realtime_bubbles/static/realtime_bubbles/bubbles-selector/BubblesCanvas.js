var BubblesCanvas = BubblesCanvas || {};
(function() {

	const colors_hex = ['#d84949', '#4850d8', '#ce48d8', '#5bd848', '#d8d348', '#3bccc2', '#d8a848','#6c5424'];
	const colors_rgb = ['216,73,73','72,80,216','206,72,216','91,216,72','216,211,72','59,204,194','216,168,72','108,84,36'];

	let ctx
	let width;
	let height;
	let minPayoff;
	let maxPayoff;
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
	  maxPayoff = -Infinity;
	  for (let key in group) {
	  	minPayoff = Math.min(group[key].payoff, minPayoff);
	  	maxPayoff = Math.max(group[key].payoff, maxPayoff);
	  }
	  maxPayoff = maxPayoff * 1.05;

	  // add grid lines to plot
	  let gridrange = (maxPayoff - minPayoff) / 5;
	  gridrange = gridrange / 5;
	  gridrange = Math.floor(gridrange);  
	  gridrange = gridrange * 5;

	  for (var i = 1; i < 6; i++){
	  	const xlevel = ((maxPayoff - (i * gridrange)) / maxPayoff);
			hline_at(xlevel);

		  ctx.font = "18px Ariel";
			ctx.fillStyle = "#cccccc";
			ctx.fillText((i * gridrange), 20, xlevel * height - 2);
		}

    player_locations(group);	
	}

	function hline_at(xlevel){
	  ctx.strokeStyle = "#cccccc";
	  ctx.beginPath();
	  ctx.moveTo(0, height * xlevel);
		ctx.lineTo(width, height * xlevel);
	  ctx.stroke();
	}

	function player_locations(group) {
		for (let key in group) {

			if (group[key].id == oTree.idInGroup){
				ownDot(
					group[key].x,
					(group[key].payoff - minPayoff) / (maxPayoff - minPayoff),
					mrg,
					group[key].id
				);
			} else {
				playerDot(
					group[key].x,
					(group[key].payoff - minPayoff) / (maxPayoff - minPayoff),
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
	    ctx.fillStyle = color_concat_rgba(player_id, 0.3);
	    ctx.fill();
	    ctx.stroke();
	}

	function ownDot(x, y, mrg, player_id) {
	    x = (mrg + ((width - 2*mrg)) * x); // y coord for p1
	    y = mrg + (height - 2*mrg) * (1 - y); // x coord for p1

	    ctx.strokeStyle = "#666666"; // 🤘
	    ctx.setLineDash([0, 0]);
	    ctx.beginPath();
	    ctx.moveTo((x + 8), y);
	    ctx.arc(x, y, 8, 0, Math.PI*2, true);  // eye
	    ctx.fillStyle = 'rgba(65, 97, 255,0.8)';
	    ctx.fill();
	    ctx.stroke();
		}

	BubblesCanvas.draw = draw;
})();