from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random as rand

class MyPage(Page):
    
    def vars_for_template(self):

    	return{
    		'rand_init_val':rand.random()
    	}


class BubblesDemo(Page):
    pass
    

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    #MyPage,
    BubblesDemo,
    ResultsWaitPage,
    Results
]
