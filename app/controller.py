from app import util
import json


def get_updated_debts():
    '''Function ctreats collections of updated debts, adding new fields to each debt'''
    # fetching debts collection from API request
    debts = util.get_debt()
    # creating empty list to collect all updated debts:
    updated_debts = []
    for debt in debts:
        # getting plan for given debt, using debt ID:
        plan = util.get_plan(debt['id'])
        if not plan:
            '''because of no plan - adding 'is_in_payment_plan' and 'next_payment_due_date'
            with False and None value accordingly. Assigning debt['amount'] to "remaining_amount"'''
            debt['is_in_payment_plan'] = False
            debt['next_payment_due_date'] = None
            debt['remaining_amount'] = debt['amount']
        else:
            # Because of plan gathering all debt payments into dictionary with keys:'total' and 'latest_payment:
            get_payments = util.get_payments_info(plan['id'])
            payed_amount = get_payments['total']

            '''Assign amount_to_pay. If debt has plan, we get 'amount_to_pay' from plan otherwise we get 
            'amount' from debt. Calculating remaining amount to pay and adding field 'remaining_amount' to debt'''
            amount_to_pay = plan['amount_to_pay'] if plan else debt['amount']
            remaining_amount = round(amount_to_pay - payed_amount, 2)
            debt['remaining_amount'] = remaining_amount

            if remaining_amount > 0:
                '''Because of remaining amount is bigger than 0, assigning True to 'is_in_payment_plan',finding
                latest payment and comparing with payments schedule and getting next scheduled date after latest payment. 
                Assigning result to added to debt field 'next_payment_due_date' '''
                debt['is_in_payment_plan'] = True
                latest_payment = get_payments["latest_payment"]
                debt['next_payment_due_date'] = util.get_next_payment(
                    plan, latest_payment)
            else:
                '''Because of debt is paid off - adding to debt 'is_in_payment_plan'
                and 'next_payment_due_date' with False and None value accordingly'''
                debt['is_in_payment_plan'] = False
                debt['next_payment_due_date'] = None
        # adding updated converted with sort feature to json debt to the list
        updated_debts.append(json.dumps(debt, sort_keys=True))
    return updated_debts


def display_result(arr):
    for item in arr:
        print(item)


def main():
    display_result(get_updated_debts())
