import json
import datetime
from dateutil.relativedelta import relativedelta

class CardDataFactory:
    def card_approved(self):
        with open('gate-simulator/data.json') as json_file:
            data = json.load(json_file)
            return data[0]['number']

    def card_declined(self):
        with open('gate-simulator/data.json', 'r') as json_file:
            data = json.load(json_file)
            return data[1]['number']

    def card_invalid(self):
        return '4444 4444 4444 4444'

    def short_card_number(self):
        return '1234'

    def month_valid(self):
        now = datetime.datetime.now()
        next_month = now + relativedelta(months=1)
        return next_month.strftime("%m")

    def month_invalid(self):
        now = datetime.datetime.now()
        prev_month = now - relativedelta(months=1)
        return prev_month.strftime("%m")

    def year_valid(self):
        now = datetime.datetime.now()
        return now.strftime("%y")

    def year_invalid(self):
        now = datetime.datetime.now()
        prev_year = now - relativedelta(years=1)
        return prev_year.strftime("%y")

    def holder_valid(self):
        return 'Ivan Ivanov'

    def empty_field(self):
        return ''

    def cvv_valid(self):
        return '999'

    def cvv_invalid(self):
        return '99'