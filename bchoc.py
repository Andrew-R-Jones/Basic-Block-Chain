#!/usr/bin/python3

import sys
import block
import hashlib

from block import get_current_time

# global list that will hold all blocks and will create the chain
chain = []


# returns true if the item was found in the block chain. false, if it was not found
def in_chain(item_id):

    for block in chain:
        if item_id == block.evidence_item_id:
            return True

    return False

# TODO
# calculates the hash of the parent block, assumes the last block is the parent
# since a block can only be added to the end of the chain
def get_last_block_hash():

    last_block = chain[-1]
    sha1 = hashlib.sha1(repr(last_block).encode('utf-8')).hexdigest()

    return sha1


def add_to_block_chain(case_id, item_id):

    if not in_chain(item_id):
        previous_hash = get_last_block_hash()
        # previous_hash, case_id, evidence_item_id, state, data, data_length = len(data.encode('utf-8')) + 1, time_stamp=get_current_time()
        b = block.Block(previous_hash, case_id, item_id, 'CHECKEDIN')
        chain.append(b)


'''
bchoc add -c case_id -i item_id [-i item_id ...]
Add a new evidence item to the blockchain and associate it with the given case identifier.
For users’ convenience, more than one item_id may be given at a time, which will create a
blockchain entry for each item without the need to enter the case_id multiple times. The state
of a newly added item is CHECKEDIN. The given evidence ID must be unique
(i.e., not already used in the blockchain) to be accepted.
'''
def add():

    if commands[0] == '-c':
        case_id = commands[1]
        commands.pop(0)
        commands.pop(0)

    while commands:
        commands.pop(0)
        item_id = commands.pop(0)

        add_to_block_chain(case_id, item_id)

    save_to_file()

    return None


'''
bchoc checkout -i item_id
Add a new checkout entry to the chain of custody for the given evidence item. Checkout actions
may only be performed on evidence items that have already been added to the blockchain.
'''


def checkout():

    if commands[0] == '-i':
        item_id = commands[1]
        for block in chain:
            if item_id == block.evidence_item_id:
                if block.state == 'CHECKEDIN':
                    block.state = 'CHECKEDOUT'
                    block.time_stamp = get_current_time()
                    print("Case: " + block.case_id)
                    print("Checked out item: " + block.evidence_item_id)
                    print("  Status: " + block.state)
                    print("  Time of action: " + str(block.time_stamp))
                else:
                    print("Error: Cannot check out a checked out item. " +
                    "Must check it in first.")
                    return 1
    else:
        print("Invalid command")
        return 1

    return None


'''
bchoc checkin -i item_id
Add a new checkin entry to the chain of custody for the given evidence item. Checkin actions may
only be performed on evidence items that have already been added to the blockchain.
'''


def checkin():

    if commands[0] == '-i':
        item_id = commands[1]
        for block in chain:
            if item_id == block.evidence_item_id:
                block.state = 'CHECKEDIN'
                block.time_stamp = get_current_time()
                print("Case: " + block.case_id)
                print("Checked in item: " + block.evidence_item_id)
                print("  Status: " + block.state)
                print("  Time of action: " + str(block.time_stamp))
    else:
        print("Invalid command")
        return 1

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
        print('Blockchain file found with INITIAL block.')
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

    if command == 'init':
        init()

    else:
        try:
            read_from_file()
        except:
            print("No blockchain initialized.")
            exit()

    if command == 'add':
        commands.remove('add')
        add()
    elif command == 'checkout':
        commands.remove('checkout')
        checkout()
    elif command == 'checkin':
        commands.remove('checkin')
        checkin()
    elif command == 'log':
        log()
    elif command == 'remove':
        remove()

    elif command == 'verify':
        verify()

    save_to_file()

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
                #  previous_hash, case_id, evidence_item_id, state,data, data_length = len(data.encode('utf-8')) + 1, time_stamp=get_current_time()
                b = block.Block(l[0], l[2],  l[3],  l[4], l[6], l[5] , time_stamp=l[1])
                chain.append(b)
                l = []
                count = 0



# initial call from command line
# ensures enough args given
if len(sys.argv) < 2:
    print('not enough arguments')
    exit()

# gets the command line arguments
commands = sys.argv[1:]
#print(f"commands: {commands}")

# calls function the run first command
run_commands(commands[0])

#save_to_file()

# for testing
#print(f"BLOCK CHAIN START\n{chain}")
