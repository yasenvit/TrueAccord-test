import requests
import json
from datetime import datetime, timedelta

DEBT_ENDPOINT = "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts"
PLAN_ENDPOINT = "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans"
PAYMENTS_ENDPOINT = "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payments"
DATE_PATTERN = "%Y-%m-%d"


def get_debt():
    response = requests.get(DEBT_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    return None


def get_plan(id):
    response = requests.get(f"{PLAN_ENDPOINT}?debt_id={id}")
    if response.status_code == 200:
        if response.json():
            return response.json()[0]
    return None


def get_payments(id):
    response = requests.get(f"{PAYMENTS_ENDPOINT}?payment_plan_id={id}")
    if response.status_code == 200:
        return response.json()
    return None


def date_converter(obj):
    '''Function converts date format from date to string or vice versa '''
    if isinstance(obj, str):  # check if obj is string
        # return converted to date obj if it's string
        return datetime.strptime(obj, DATE_PATTERN)
    # return converted to string obj if it's date
    return datetime.strftime(obj, DATE_PATTERN)


def get_payments_info(id):
    '''This function returns dictionary with two key-value pairs:
        sum of all payments and latest_payment date for given ID'''
    # getting all payments for given payment_plan_id using API
    payments = get_payments(id)
    if not payments:
        return {'total': 0, 'latest_payment': None}
    amount, dates = 0, []
    # calculating sum of all payments and finding latest payment date:
    for payment in payments:
        amount += payment["amount"]
        # convert string format to date format:
        dates.append(date_converter(payment["date"]))
    return {'total': amount, 'latest_payment': max(dates)}


def get_next_payment(plan, latest_payment):
    '''Function finds next scheduled payment date after latest payment'''
    date_point = date_converter(plan['start_date'])
    if latest_payment is None:
        # return start_date from payments plan if no previous payments
        return date_point
    frequency = plan['installment_frequency']
    # assign payments frequency and find closest scheduled date after recent payment date
    interval = 1 if frequency.upper() == "WEEKLY" else 2
    while latest_payment >= date_point:
        date_point += timedelta(weeks=interval)
    # return converted to string next scheduled payment date
    return date_converter(date_point)
