from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.api import Page
import random

class Constants(BaseConstants):
    name_in_url = "investment_game"
    players_per_group = 2
    num_rounds = 8
    individual_rounds = 4
    group_rounds = 4
    min_investment = c(0)
    max_individual_investment = c(1)
    max_group_investment = c(2)
    step = c(0.25)
    players_per_group = 2
    group_endowment = 2
    group_increment = 0.5


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            players = self.get_players()
            group_matrix = []
            for i in range(0, len(players), Constants.players_per_group):
                group = players[i:i + Constants.players_per_group]
                if len(group) == Constants.players_per_group:
                    group_matrix.append(group)
                    # Record partner IDs
                    group[0].partner_id = group[1].id_in_subsession
                    group[1].partner_id = group[0].id_in_subsession

            self.set_group_matrix(group_matrix)
        else:
            self.group_like_round(1)

        for p in self.get_players():
            p.is_individual_round = self.round_number <= Constants.individual_rounds
            if p.is_individual_round:
                p.success_number = random.randint(1, 6)
            p.agreed_on_investment = False


class Group(BaseGroup):
    group_investment = models.FloatField(
        min=0,
        max=2,
        label="We would like to invest"
    )
    dice_roll = models.IntegerField()
    success = models.BooleanField()
    group_earnings = models.CurrencyField()
    success_number_group = models.IntegerField()
    chat_history = models.LongStringField(initial='')
    investment_agreed = models.BooleanField(initial=False)
    fourth_round_earnings = models.CurrencyField()

    def live_chat(self, id_in_group, data):
        response = {'id_in_group': id_in_group, 'message': data}
        return {0: response}

class Player(BasePlayer):
    is_individual_round = models.BooleanField()
    success_number = models.IntegerField(min=1, max=6)
    success_number_group = models.IntegerField(min=1, max=6)
    investment = models.CurrencyField(
        min=0,
        max=1,
        label="I would like to invest"
    )
    dice_roll = models.IntegerField(min=1, max=6)
    success = models.BooleanField()
    close_field = models.StringField(blank=True)
    earnings = models.CurrencyField()
    agreed_on_investment = models.BooleanField(initial=False)
    agreed_investment = models.FloatField(blank=True)
    proposed_investment = models.FloatField()
    investment_amount = models.FloatField()
    partner_id = models.IntegerField()
    investment = models.FloatField(initial=0)

    def set_earnings(self):
        if self.is_individual_round:
            if self.success:
                self.earnings = 6 * self.investment
            else:
                self.earnings = -1 * self.investment
        else:
            if self.group.success:
                self.earnings = 6 * self.group.group_investment
            else:
                self.earnings = -1 * self.group.group_investment

    # Consent form fields
    consent_age = models.BooleanField(
        label="I am 18 years of age or older."
    )
    consent_read = models.BooleanField(
        label="I have read and understand the information above."
    )
    consent_participate = models.BooleanField(
        label="I want to participate in this research and continue with the study."
    )

    # Survey fields
    age_check = models.BooleanField(
        label="Are you 18 years of age or older?",
        choices=[
            [True, 'Yes'],
            [False, 'No'],
        ]
    )
    gender = models.StringField(
        label="What gender do you identify as?",
        choices=['Female', 'Non-binary', 'Male'],
        widget=widgets.RadioSelect
    )
    career = models.StringField(label="What is your major?")
    native_language = models.StringField(label="What is your native language?")
    university_year = models.StringField(label="What year are you in university?",
                                         choices=['First year', 'Second year', 'Third year', 'Fourth year', 'Graduate',
                                                  'Other'], widget=widgets.RadioSelect)
    gpa = models.FloatField(label="What is your current GPA? (0-5, up to 4 decimal places)", min=0, max=5)
    smoker = models.StringField(
        label="Are you a smoker?",
        choices=[['Yes', 'Yes'], ['No', 'No'], ['Prefer not to answer', 'Prefer not to answer']],
        widget=widgets.RadioSelect
    )
    alcohol = models.StringField(
        label="Do you practice excessive alcohol consumption?",
        choices=[['Yes', 'Yes'], ['No', 'No'], ['Prefer not to answer', 'Prefer not to answer']],
        widget=widgets.RadioSelect
    )
    drugs = models.StringField(
        label="Do you use recreational drugs?",
        choices=[['Yes', 'Yes'], ['No', 'No'], ['Prefer not to answert', 'Prefer not to answer']],
        widget=widgets.RadioSelect
    )

    weekly_spending = models.IntegerField(label="What is your weekly spending in USD?")

    # Cognitive Reflection Test
    crt_linda = models.StringField(
        label="Which of the following two alternatives is more likely?",
        choices=[
            'Linda is a bank teller.',
            'Linda is a bank teller and active in the feminist movement.'
        ],
        widget=widgets.RadioSelect
    )
    crt_bat = models.FloatField(label="How much does the ball cost in dollars?")
    crt_widget = models.IntegerField(label="How many minutes would it take 100 machines to make 100 widgets?")
    crt_lake = models.IntegerField(label="How many days would it take to cover half of the lake?")
    crt_double = models.StringField(
        label="In 2021, how much will you be able to buy with your income?:",
        choices=[
            'More than today.',
            'Exactly the same as today.',
            'Less than today.'
        ],
        widget=widgets.RadioSelect
    )


    # Financial Literacy
    fin_change =  models.IntegerField(label="")
    fin_lottery = models.IntegerField(label="")
    fin_sale = models.IntegerField(label="")
    fin_cardealer = models.IntegerField(label="")
    fin_interest = models.IntegerField(label="")
    fin_disease = models.IntegerField(label="")

    # Risk Attitudes
    risk_general = models.IntegerField(label="How would you rate your willingness to take risks in general?", min=1, max=10)
    risk_driving = models.IntegerField(label="How would you rate your willingness to take risks while driving?", min=1, max=10)
    risk_career = models.IntegerField(label="How would you rate your willingness to take risks in your professional career?", min=1, max=10)
    risk_health = models.IntegerField(label="How would you rate your willingness to take risks with respect to your health?", min=1, max=10)

    # Decision Making Scenarios
    scenario_jar = models.StringField(
        label="Which jar do you prefer to guess the color of a ball from?",
        choices=[
            'I prefer to guess the color of a ball from jar 1.',
            'I am indifferent.',
            'I prefer to guess the color of a ball from jar 2.'
        ],
        widget=widgets.RadioSelect
    )
    monty_hall = models.StringField(
        label="Is it advantageous for you to change your choice?",
        choices=[
            'I prefer to keep my original choice (Door number 1).',
            'It does not matter if I change or not.',
            'I prefer to switch to Door number 2.'
        ],
        widget=widgets.RadioSelect
    )

    # Timing fields
    decision_time = models.FloatField()
    continue_field = models.StringField(label="")
    exit_survey_completed = models.BooleanField(initial=False)


template_name = 'investment_game/EndSlide.html'


def is_displayed(self):
    return self.round_number == Constants.individual_rounds