from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from jsonfield import JSONField
from otree_redwood.models import Event, Group as RedwoodGroup
import random

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) #<<<<<<<<<<<<<<<<<<<<



author = 'Curtis Kephart (economicurtis@gmail.com) & James Pettit (james.l.pettit@gmail.com)'

doc = """
Bubbles UI with Realtime
"""


class Constants(BaseConstants):
    name_in_url = 'realtime_bubbles'
    players_per_group = None
    num_rounds = 5

    round_length = [200,200,200,200,200]
    round_payoff_functions = ['vcm','vcm','wl','wl','foo']

    round_var_a =   [0.3, 0.3,    20,20,20]
    round_var_b =   [100, 100,    10,10,10]
    round_var_c =   [None, None,  60,60,60]



def period_load(self, config_field):
    # config_field must match Constants var name
    # Constants[config_field] config_field set in settings.py
    # config_field must be array. 
    # also breaks if there are more round numbers than length of config_field array
    if config_field in self.session.config:
        return self.session.config[config_field][self.round_number-1]
    else:
        return Constants[config_field]


class Subsession(BaseSubsession):

    def before_session_starts(self):

        players = self.get_players()

        # Grouping
        # Group based on 'players_per_group' config settings field. 
        players_per_group = self.session.config['players_per_group']

        self.group_randomly()
        group_matrix = []
        for i in range(0, len(players), players_per_group):
            group_matrix.append(players[i:i+players_per_group])
        self.set_group_matrix(group_matrix)

        for p in self.get_players():

            p.round_length = period_load(self,'round_length')
            p.payoff_var_a = period_load(self,'round_payoff_var_a')
            p.payoff_var_b = period_load(self,'round_payoff_var_b')
            p.payoff_var_c = period_load(self,'round_payoff_var_c')
            p.payoff_function = period_load(self,'round_payoff_function')




class Group(RedwoodGroup):

    def payoff_function(self, group, function_name, v1, v2, v3):

        # for player in group:
        #     group[player]['payoff'] = 12.5

        if function_name == 'vcm':
            mpcr = v1
            endow = v2
            totalcontrib = 0
            for player in group:
                totalcontrib = totalcontrib + (endow * group[player]['x'])
            for player in group:
                group[player]['payoff'] = endow - (endow * group[player]['x'] + mpcr * totalcontrib)
            
        if function_name == 'wl':
            wl_a = v1
            wl_b = v2
            wl_c = v3
            min_effort = 1000      
            for player in group:
                min_effort = min(min_effort, group[player]['x'])
            for player in group:
                group[player]['payoff'] = (wl_a * min_effort) - (wl_b * group[player]['x']) + wl_c
            effort = 1000;

        return group


    group_decisions = JSONField(null=True)
    
    
    def period_length(self):
        return self.get_player_by_id(1).round_length


    def when_all_players_ready(self):
        """Initializes decisions based on ``player.initial_decision()``.
        If :attr:`num_subperiods` is set, starts a timed task to run the
        sub-periods.
        """
        self.group_decisions = {}
        for player in self.get_players():
            self.group_decisions[player.participant.code] = {
                'id': player.id_in_group,
                'x': player.initial_action,
                'payoff': 0,
            }

        self.save()


    def _on_decisions_event(self, event=None, **kwargs):
        if not self.ran_ready_function:
            logger.warning('ignoring decision from {} before when_all_players_ready: {}'.format(event.participant.code, event.value))
            return

        player = next(player for player in self.get_players() if player.participant.code == event.participant.code)

        self.group_decisions[event.participant.code] = {
            'id': player.id_in_group,
            'x': float(event.value),
            'payoff': 12
        }
        self.group_decisions = self.payoff_function(
            self.group_decisions, 
            self.get_player_by_id(1).payoff_function,
            self.get_player_by_id(1).payoff_var_a,
            self.get_player_by_id(1).payoff_var_b,
            self.get_player_by_id(1).payoff_var_c,
            )

        self.save()
        self.send('group_decisions', self.group_decisions)


class Player(BasePlayer): 
    
    round_length = models.PositiveIntegerField(
        doc="""The length of the round timer."""
    )

    payoff_function = models.CharField(
        doc = """payoff function used""")

    payoff_var_a = models.FloatField(
        doc = """Variable `a` in the payoff function""")

    payoff_var_b = models.FloatField(
        doc = """Variable `b` in the payoff function""")

    payoff_var_c = models.FloatField(
        doc = """Variable `c` in the payoff function""")

    initial_action = models.FloatField(
        min=0.0,
        max=1.0,
        doc = """subject's initial decision""")

    round_score = models.FloatField(
        doc="""the score for that round. the integral of the payoff value for the round""")

 
    def set_round_score(self):
        decisions = list(Event.objects.filter(
                channel='decisions',
                content_type=ContentType.objects.get_for_model(self.group),
                group_pk=self.group.pk).order_by("timestamp"))

        try:
            period_start = Event.objects.get(
                    channel='state',
                    content_type=ContentType.objects.get_for_model(self.group),
                    group_pk=self.group.pk,
                    value='period_start')
            period_end = Event.objects.get(
                    channel='state',
                    content_type=ContentType.objects.get_for_model(self.group),
                    group_pk=self.group.pk,
                    value='period_end')

        except Event.DoesNotExist:
            return float('nan')

        period_duration = period_end.timestamp - period_start.timestamp

        payoff = 0

        # for i, d in enumerate(decisions):

  #           flow_payoff = d.x

  #           if i + 1 < len(decisions):
  #               next_change_time = decisions[i + 1].timestamp
  #           else:
  #               next_change_time = period_end.timestamp
  #           payoff += (next_change_time - d.timestamp).total_seconds() * flow_payoff



        self.payoff = payoff

        return {
            decisions[0].value['payoff']
        }
