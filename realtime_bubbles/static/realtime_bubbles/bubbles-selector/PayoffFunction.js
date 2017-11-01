var PayoffFunction = PayoffFunction || {};
(function() {
  // PAYOFF FUNCTION TOWN

  // vcm parameters
  const mpcr = 0.3;
  const endow = 100;

  // wl
  const wl_a = 20
  const wl_b = 10
  const wl_c = 60

  function compute(group, func) {
  	/* Group is a dictionary mapping players by participant code to their decision and payoff.

      e.g.
      groupDecisions = {
        'abc': {
          id: 1,
          x: 0.3,
          payoff: ?,
        },
        'xyz': {
          id: 2,
          x: 0.5,
          payoff: ?,
        },
      }

  	*/
  	if (func == 'vcm') {
      // calc total group contribution
      let totalcontrib = 0;
      for (let key in group) {
          totalcontrib = totalcontrib + group[key].x;
      }

      // calc individual payoffs
      for (let key in group) {
        group[key].payoff = (endow) - (endow * group[key].x) + (mpcr * totalcontrib);
      }
  	} else if (func == 'wl'){
      // find the weakest link
      let min_effort = 1.0;
      for (let key in group) {
        min_effort = Math.min(group[key].x, min_effort);
      }

      // calc individual payoffs
      for (let key in group) {
        group[key].payoff = (wl_a * min_effort) - (wl_b * group[key].x) + wl_c;
      }
  	}

  	return group;
  }

  PayoffFunction.compute = compute;

})();