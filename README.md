# otree_realtime_bubbles

Realtime Bubbles is a template for oTree apps. It includes a `bubbles` user interface, and the ability to run `realtime` experiments. 

## Bubbles UI

Bubbles UI refers to a display in which the x-axis indicates users action selection and y-axis indicates current payoffs. 

Bubbles allows as input a single continuous variable from N-players. Arbitrary payoff functions that accept this input may be applied. 


Horizontal Slider:
- User control over a single continuous variable via a horizontal slider. 
- The user's action choice is displayed on the horizontal axis. 
- The slider may be restricted to binary choice, or a discrete set set of values, say, integers. 

Verticle Axis:
- payoffs are shown on vertical axis. 
- payoff information may be limited, e.g. 

Any arbitrary payoff function that takes as input one variable per user 

## Realtime

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