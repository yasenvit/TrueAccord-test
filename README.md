# TrueAccordTest
API response manipulation
# Prerequisites
* Python version: 3.8 and up

## Setup
* requests
```
$ python -m pip install requests
```
## Installation
* Clone the repo
```
$ git clone https://github.com/yasenvit/TrueAccord-test.git
```
## Usage
```
$ python3 run.py
```
## Logic flow:
```
controller.py
def get_updated_debts():



    API get DEBTS collection
    for each DEBT in DEBTS:
        API get PLAN from PAYMENT PLANS using DEBT["id"]
        if PLAN doesn't exist:
            -add DEBT["is_in_payment_plan"] = False
            -add DEBT["next_payment_due_date"] = None
            -add DEBT["remaining_amount"] = DEBT["amount"]
        else (PLAN exists):
            -API get all payments for this DEBT from PAYMENTS using DEBT's PLAN["id"]
            -calculate remaining_amount subtracting "sum_of_all_payments" from PLAN["amount_to_pay"]
            -add DEBT["remaining_amount"] = remaining_amount
            if remaining_amount > 0:
                -find "latest_payment_date" in gathered payments info before
                -calculate all scheduled "payment_dates"
                -add DEBT["next_payment_due_date"] = "scheduled_payment_date" following right after "latest_payment_date"
                -add DEBT["is_in_payment_plan"] = True
            else (remaining_amount = 0):
                -add DEBT["is_in_payment_plan"] = False
                -add DEBT["next_payment_due_date"] = None
        add updated, converted to JSON and sorted DEBT to new_collection_list
  
  returning new_collection_list
    
```

