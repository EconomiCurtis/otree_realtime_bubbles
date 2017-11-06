from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random as rand
import json
from django.conf import settings

class MyPage(Page):
    
    def vars_for_template(self):

    	return{
    		'rand_init_val':rand.random(),
            'DEBUG':settings.DEBUG
    	}

class InitialAction(Page):
    form_model = models.Player
    form_fields = ['initial_action']

    def error_message(self, values):
        if values["initial_action"] == None:
            return 'Please select an action from the slider before clicking next.'


class BubblesDemo(Page):
    pass
    

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


def get_output_table(events):

    
    header = [
        'timestamp',
        'session_code',
        'player_code',
        'round_number',
        'group_id',
        'tick',
        'x',
    ]
    if not events:
        return [], []
    rows = []
 
    group = events[0].group

    tick = 0
    participant_dict = {}
    for event in events:
        if event.channel == 'group_decisions':

            # if participant_dict[event.participant] == None:
            #     participant_dict[event.participant] = []
            
            # participant_dict[event.participant].push(event.value)






            rows.append([
                event.timestamp,
                group.session.code,
                event.participant,
                group.round_number  ,
                group.id_in_subsession,
                tick,
                event.value,
            ])
            tick += 1


    return header, rows


page_sequence = [
    #MyPage,
    InitialAction,
    BubblesDemo,
    ResultsWaitPage,
    Results
]
