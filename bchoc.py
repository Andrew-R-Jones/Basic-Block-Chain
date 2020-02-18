#!/usr/bin/python3

import sys
import block

# global list that will hold all blocks and will create the chain
chain = []

'''
bchoc add -c case_id -i item_id [-i item_id ...]
Add a new evidence item to the blockchain and associate it with the given case identifier.
For users’ convenience, more than one item_id may be given at a time, which will create a
blockchain entry for each item without the need to enter the case_id multiple times. The state
of a newly added item is CHECKEDIN. The given evidence ID must be unique
(i.e., not already used in the blockchain) to be accepted.
'''


def add():
    print("add function")
    return None


'''
bchoc checkout -i item_id
Add a new checkout entry to the chain of custody for the given evidence item. Checkout actions
may only be performed on evidence items that have already been added to the blockchain.
'''


def checkout():
    print("checkout function")
    return None


'''
bchoc checkin -i item_id
Add a new checkin entry to the chain of custody for the given evidence item. Checkin actions may
only be performed on evidence items that have already been added to the blockchain.
'''


def checkin():
    print("checkin function")
    return None


'''
bchoc log [-r] [-n num_entries] [-c case_id] [-i item_id]
Display the blockchain entries giving the oldest first (unless -r is given).
'''


def log():
    print("log function")
    return None

'''
bchoc remove -i item_id -y reason [-o owner]
Prevents any further action from being taken on the evidence item specified. The specified
item must have a state of CHECKEDIN for the action to succeed.
'''

def remove():
    print("remove function")
    return None

'''
bchoc init
Sanity check. Only starts up and checks for the initial block.
'''

def init():
    try:
        read_from_file()
    except:
        print('Blockchain file not found. Created INITIAL block.')
        # previous_hash, case_id, evidence_item_id, state, data, data_length = len(data.encode('utf-8')) + 1, time_stamp=get_current_time()
        b = block.Block(None, None, None, 'INITIAL', 'Initial block', 14)
        chain.append(b)
    return None

'''
bchoc verify
Parse the blockchain and validate all entries.
'''
def verify():
    print("verify function")
    return None


''' runs certain function based on the command argument passed in '''
def run_commands(command):
    if command == 'add':
        add()
    elif command == 'checkout':
        checkout()
    elif command == 'checkin':
        checkin()
    elif command == 'log':
        log()
    elif command == 'remove':
        remove()
    elif command == 'init':
        init()
    elif command == 'verify':
        verify()
   
# saves the list of blocks to a file
def save_to_file():

    with open('blockchain.txt', 'w') as filehandle:
        for block in chain:
            filehandle.write('%s\n' % block)


# reads and restores the saved blocks from file, and add to list 'chain'
def read_from_file():
    l = []
    count = 0
    # define an empty list
    # open file and read the content in a list
    with open('blockchain.txt', 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            item = line[:-1]

            # add item to the list
            l.append(item)
            count = count + 1

            if count == 7:
                b = block.Block(l[0], l[2], l[3], l[4], l[5], l[6] ,time_stamp=l[1])
                chain.append(b)
                l = []
                count = 0



    print('Blockchain file found with INITIAL block.')

# initial call from command line
# ensures enough args given
if len(sys.argv) < 2:
    print('not enough arguments')
    exit()

# gets the command line arguments
commands = sys.argv[1:]

# calls function the run first command
run_commands(commands[0])

save_to_file()

# for testing 
print(f"BLOCK CHAIN START\n{chain}")
