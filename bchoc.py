
'''
bchoc add -c case_id -i item_id [-i item_id ...]
Add a new evidence item to the blockchain and associate it with the given case identifier.
 For users’ convenience, more than one item_id may be given at a time, which will create a 
 blockchain entry for each item without the need to enter the case_id multiple times. The state 
 of a newly added item is CHECKEDIN. The given evidence ID must be unique 
 (i.e., not already used in the blockchain) to be accepted.
'''
def add():
    return None


'''
bchoc checkout -i item_id
Add a new checkout entry to the chain of custody for the given evidence item. Checkout actions 
may only be performed on evidence items that have already been added to the blockchain.
'''
def checkout():
    return None

'''
bchoc checkin -i item_id
Add a new checkin entry to the chain of custody for the given evidence item. Checkin actions may
only be performed on evidence items that have already been added to the blockchain.
'''
def checkin():
    return None

'''
bchoc log [-r] [-n num_entries] [-c case_id] [-i item_id]
Display the blockchain entries giving the oldest first (unless -r is given).
'''
def log():
    return None

'''
bchoc remove -i item_id -y reason [-o owner]
Prevents any further action from being taken on the evidence item specified. The specified
item must have a state of CHECKEDIN for the action to succeed.
'''
def remove():
    return None

'''
bchoc init
Sanity check. Only starts up and checks for the initial block.
'''
def init():
    return None

'''
bchoc verify
Parse the blockchain and validate all entries.
'''
def verify():
    return None
