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
## Pseudocode:
```
controller.py


def get_updated_debts():
    Fetch DEBTS collection
    for DEBT in DEBTS:
        fetch PLAN from PAYMENT PLANS using DEBT["id"]
        if not PLAN:
            -add DEBT["is_in_payment_plan"] = False
            -add DEBT["next_payment_due_date"] = None
            -add DEBT["remaining_amount"] = DEBT["amount"]
        else:
            -fetch all payments for this DEBT from PAYMENTS using DEBT's PLAN["id"]
            -find out "amount_to_pay" (if PLAN exists - get value from PAYMENTS["amount_to_pay"], otherwise get value from DEBT["amount"]
            -find "remaining_amount" subtracting "sum_of_all_payments" from "amount_to_pay"
            -add DEBT["remaining_amount"] = "remaining_amount"
            if "remaining_amount" > 0:
                -find "latest_payment_date"
                -calculate all scheduled "payment_dates"
                -add DEBT["next_payment_due_date"] = "scheduled_payment_date" following right after "latest_payment_date"
                -add DEBT["is_in_payment_plan"] = True
            else:
                -add DEBT["is_in_payment_plan"] = False
                -add DEBT["next_payment_due_date"] = None
         add updated, converted to JSON and sorted DEBT to new_collection_list
  
  RETURN new_collection_list
    
```

