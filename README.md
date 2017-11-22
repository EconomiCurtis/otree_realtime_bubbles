# Realtime Bubbles

Realtime Bubbles is a template oTree app. It includes a `bubbles` user interface run in  `realtime`. 

<img src="/_static/docs/gif_bubbles_ui.gif" width="100%" alt="I like big Bubbles, and I cannot lie">


## Bubbles UI

Bubbles UI refers to a display in which the x-axis shows users action selection and y-axis indicates current payoffs. 

Bubbles allows as input a single continuous variable from N-players. Arbitrary payoff functions that accept this input may be applied. 

Horizontal Slider:
- User control over a single continuous variable via a horizontal slider. 
- The user's action choice is displayed on the horizontal axis. 

Verticle Axis:
- payoffs are shown on vertical axis. 
- payoff information may be limited, e.g. 

Any arbitrary payoff function that takes as input one variable per user 

## Realtime

It uses Redwood 3 (http://otree-redwood.readthedocs.io/en/latest/getting_started.html) for realtime components. 


## Payoff Functions

Bubbles UI can accept any artibrary payoff with any number of players and single action input. 

Realtime bubbles already has two payoff functions implemented, weakest link (`'wl'`) and a public goods (`'vcm'`). 
- See `settings.py` and the configuration file fields `round_length`, `round_payoff_function`, `round_payoff_var_a`,`round_payoff_var_b`, and `round_payoff_var_c` for an example of how to make use of these built in payoff functions. 
- The fields are accepted as input in `models.py` `before_session_starts`. 

Currently, the payoff function must be implemented in two places,
- in python in models.py under `set_round_score` (this is for initial positions, logging and for messages between players) and
- in javascript, in `static/realtime_bubbles/bubbles-app/PayoffFunction.js` to draw the user interface. 

## Initial action selections

A special dedicate page asks players for their initial positions. See `InitialAction.html` under templates, plus `views.py` for how this is handled. Once all players have selected their initial action, the realtime game starts. 

## Realtime messages between players

Any time a player changes their action selection, a `group_decisions` event message is sent to all players. This passing through `models.py`-`payoff_function` updating current flow payoffs. Only after this channel event message process occurs are new actions selections and payoffs distributed, updating what players see. 

## Round Scores

oTree's `payoff` player field is not updated. Instead, the player field `round_score` is calculated by taking the intagral of the player's flow payoffs over the full period. This is handled in `models.py` `set_round_score`, and called when the Results page is presented to players. 

Since it's possible for some player clicks to be received after the period has technically ended, there's some error handling of this. However, all these 'extra' messages are logged and stored. 

## Output Data

Under otree-redwood, all `group_decisions` and `state` channel events are used to generate the real-time log file (see http://otree-redwood.readthedocs.io/en/latest/concepts.html for some details). This creates an events log. At the session-round-group level, a [dictionary](https://docs.python.org/2/tutorial/datastructures.html#dictionaries) is generated, with keys the player's unique participant code, to a value that is a dictionary of all values desired to be stored in this group_decisions message. In the current, basic setup, this logs that player's `id` their player number in the group, `x`  their current action selection, and `payoff`, their current flow payoff given all player's actions and the payoff function and its parameterization. 

For example, one of these group_decision message may look like: 

	{
		'6526jupr': {'id': 1, 'x': 0.93, 'payoff': 87.321}, 
		'ytvj7a0p': {'id': 2, 'x': 0.98, 'payoff': 87.306}, 
		'rtehp0np': {'id': 3, 'x': 1.0,  'payoff': 87.3. }
	}

Along with `timestamp`, `session_code` and other informaiton. 

See `views.py` `get_output_table` for how how these channel events are converted into the CSV output file. 

**Gotcha** - be sure that your config's app name in `settings.py` matches the name of the otree app (for example here, `realtime_bubbles`). Otherwise, the experiment's data download link will not appear in oTree's "/export/" tab. If it's setup correctly, a link under "Third-party data exports" will appear under the config's `display_name`. 

Since it's possible for some player clicks to come in after the period has technically ended, note that some `group_decisions` messages may be logged after the `state` `period_end` message has arrived. Again, these are all events that came into the otree-redwood server after the round ended. 


### Also Curtis Notes

Installation
- oTree http://otree.readthedocs.io/en/latest/install.html
- otree-redwood http://otree-redwood.readthedocs.io/en/latest/getting_started.html

#### Install on your mac

- Clone repo
- navigate in
- setup virtual environment `virtualenv venv` `source venv/bin/activate`
- setup `pip3 install -r requirements.txt`
 - You have needed to install jsonfield manually, since there might be a [package bug](https://stackoverflow.com/questions/11015692/pip-fails-to-install-packages-from-requirements-txt). 
 - You may need to install `pip install -U git+git://github.com/oTree-org/otree-core.git#egg=otree-core`, and `pip install -U otree-core` mannually. And you may have to do this in a particular order, installing the latest version of otree-core after otree-redwood. 


Just in case I forget, from shell;

- Activate the virutal environment `venv/Scripts/activate` .. `deactivate`. Sometimes `source venv/Scripts/activate`
- Run docker `docker-compose -f .docker-compose-....yml up`

Inspector tools:

- In the inspecter console during the experiment:
  - `document.querySelector('redwood-decision').groupDecisions` to get list of group decisions. 
