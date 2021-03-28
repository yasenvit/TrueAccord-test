from app import util
import json


def get_updated_debts():
    '''Function creates collections of updated debts, adding new fields to each debt'''
    # fetch debts collection from API request
    debts = util.get_debt()
    # create empty list to collect all updated debts:
    updated_debts = []
    for debt in debts:
        # get plan for given debt, using debt ID:
        plan = util.get_plan(debt['id'])
        if not plan:
            '''Plan doesn't exist, therefore add new fields debt['is_in_payment_plan'] and debt['next_payment_due_date']
            with False and None values accordingly. Assign debt['amount'] to added new field debt['remaining_amount']'''
            debt['is_in_payment_plan'] = False
            debt['next_payment_due_date'] = None
            debt['remaining_amount'] = debt['amount']
        else:
            # gather all debt payments into dictionary with keys:'total' and 'latest_payment:
            get_payments = util.get_payments_info(plan['id'])
            payed_amount = get_payments['total']
            # Calculating remaining amount to pay and adding field DEBT['remaining_amount']:
            remaining_amount = round(plan['amount_to_pay'] - payed_amount, 2)
            debt['remaining_amount'] = remaining_amount

            if remaining_amount > 0:
                '''Remaining amount is bigger than 0, so that:
                    - assign True to added dept['is_in_payment_plan'],
                    - find latest payment and compare it with payments schedule and get next scheduled date after latest payment. 
                    - assign result to added dept['next_payment_due_date'] '''
                debt['is_in_payment_plan'] = True
                latest_payment = get_payments["latest_payment"]
                debt['next_payment_due_date'] = util.get_next_payment(
                    plan, latest_payment)
            else:
                '''Debt is paid off, so that adding to debt 'is_in_payment_plan'
                and 'next_payment_due_date' with False and None values accordingly'''
                debt['is_in_payment_plan'] = False
                debt['next_payment_due_date'] = None
        # add updated converted with sort feature to json debt to the list
        updated_debts.append(json.dumps(debt, sort_keys=True))
    return updated_debts


def display_result(arr):
    for item in arr:
        print(item)


def main():
    display_result(get_updated_debts())
