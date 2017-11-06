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

### Also

Just in case I forget, from shell;

- Activate the virutal environment `venv/Scripts/activate` .. `deactivate`
- Run docker `docker-compose -f .docker-compose-....yml up`