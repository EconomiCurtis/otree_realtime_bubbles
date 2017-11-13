from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)


from otree_redwood.models import Event, DecisionGroup
import random


author = 'Curtis Kephart (economicurtis@gmail.com) & James Pettit (james.l.pettit@gmail.com)'

doc = """
Bubbles UI with Realtime
"""


class Constants(BaseConstants):
	name_in_url = 'realtime_bubbles'
	players_per_group = None
	num_rounds = 5

	round_lengths = [200,200,200,200,200]
	round_payoff_functions = ['vcm','vcm','wl','wl','foo']

	round_var_a =   [0.3, 0.3,    20,20,20]
	round_var_b =   [100, 100,    10,10,10]
	round_var_c =   [None, None,  60,60,60]


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
			p.round_lengths = Constants.round_lengths[self.round_number-1]
			p.payoff_var_a = Constants.round_var_a[self.round_number-1]
			p.payoff_var_b = Constants.round_var_b[self.round_number-1]
			p.payoff_var_c = Constants.round_var_c[self.round_number-1]
			p.payoff_function = Constants.round_payoff_functions[self.round_number-1]


class Group(DecisionGroup):
	
	def period_length(self):
		return None

	def initial_actions(self):
		return {
			player.participant.code: player.initial_decision()
			for player in self.get_players()
		}

    # def period_length(self):
    #     return parse_config(self.session.config['config_file'])[self.round_number-1]['period_length']


class Player(BasePlayer):
	

	def initial_decision(self):
		return {
			'id': self.id_in_group,
			'x': self.initial_action,
			'payoff': None,
		}

	round_lengths = models.PositiveIntegerField(
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

