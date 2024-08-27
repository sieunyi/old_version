from os import environ


SESSION_CONFIGS = [
    dict(
        name='investment_game',
        display_name="Juego de Inversión",
        num_demo_participants=2,
        app_sequence=['investment_game'],
        use_browser_bots = False,
    ),
]

INSTALLED_APPS = [
    'otree',
    'investment_game',
]

ROOMS = [
    dict(
        name='investment_game',
        display_name='Investment Game Room',
        participant_label_file='_rooms/juegoinversion.txt',
    ),
]
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []
GROUP_BY_ARRIVAL_TIME = True


LANGUAGE_CODE = 'en'

LANGUAGE_CODE_ISO = 'en'
USE_I18N = True

CUSTOM_BUTTONS = {
    'next': 'Siguiente',
}

REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'Rkatkgkqslek!'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6551162623333'
DEBUG = False

OTREE_AUTH_LEVEL = 'STUDY'
STUDY_PASSWORD = '20242025gg'


DEMO_PAGE_INTRO_HTML = ""

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

