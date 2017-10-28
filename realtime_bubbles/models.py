from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)


from otree_redwood.models import Event, DecisionGroup
import random


author = 'Your name here'

doc = """
Bubbles UI with Realtime
"""


class Constants(BaseConstants):
	name_in_url = 'realtime_bubbles'
	players_per_group = None
	num_rounds = 1
	mpcr = 0.3


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

class Group(DecisionGroup):
	
	def period_length(self):
		return 1200

    # def period_length(self):
    #     return parse_config(self.session.config['config_file'])[self.round_number-1]['period_length']


class Player(BasePlayer):
	

	def initial_decision(self):
		return random.random()

	round_time = models.PositiveIntegerField(
		doc="""The length of the real effort task timer."""
	)

	payoff_var_a = models.FloatField(
		doc = """Variable `a` in the payoff function""")
