#!/usr/bin/python3

import sys
import block
import hashlib
import os
import struct

from block import get_current_time




########################################################################################
###############     FOR SUBMISSION      ################################################
#file_path = os.environ["BCHOC_FILE_PATH"]
########################################################################################

########################################################################################
###############     FOR DUBUG AND TESTING       ########################################
file_path = 'blockchain.txt'
########################################################################################

# global list that will hold all blocks and will create the chain
chain = []

STATE = {
    "init": b"INITIAL\0\0\0\0",
    "in": b"CHECKEDIN\0\0",
    "out": b"CHECKEDOUT\0",
    "dis": b"DISPOSED\0\0\0",
    "des": b"DESTROYED\0\0",
    "rel": b"RELEASED\0\0\0",
    "INITIAL": b"INITIAL\0\0\0\0",
    "CHECKEDIN": b"CHECKEDIN\0\0",
    "CHECKEDOUT": b"CHECKEDOUT\0",
    "DISPOSED": b"DISPOSED\0\0\0",
    "DESTROYED": b"DESTROYED\0\0",
    "RELEASED": b"RELEASED\0\0\0",
}

block_head_fmt = "20s d 16s I 11s I"
block_head_len = struct.calcsize(block_head_fmt)
block_head_struct = struct.Struct(block_head_fmt)


# returns true if the item was found in the block chain. false, if it was not found
# return exit code 1 if the block was found in the chain with a released state
def in_chain(item_id):

    found = False
    previously_removed = False

    for block in chain:
        if item_id == block.evidence_item_id:
            found = True
            if block.state == 'RELEASED' or block.state == 'DISPOSED' or block.state == 'DESTROYED':
                previously_removed = True

    # exit with error code if the block was in the chain and it was already released
    if previously_removed:
        exit(1)
    else:
        return found

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
        return True
    else: return False


'''
bchoc add -c case_id -i item_id [-i item_id ...]
Add a new evidence item to the blockchain and associate it with the given case identifier.
For users’ convenience, more than one item_id may be given at a time, which will create a
blockchain entry for each item without the need to enter the case_id multiple times. The state
of a newly added item is CHECKEDIN. The given evidence ID must be unique
(i.e., not already used in the blockchain) to be accepted.
'''


def add():

    add_output_string = ""


    if commands[0] == '-c':
        case_id = commands[1]
        commands.pop(0)
        commands.pop(0)
    else:
        exit(1)

    if len(commands) < 2:
        exit(1)
    # check the length for item -i and item id string
    if commands[0] != '-i' or not commands[1]:
        print('no item id')
        exit(1)

    add_output_string += "Case: " + case_id
    while commands:
        commands.pop(0)
        item_id = commands.pop(0)

        if add_to_block_chain(case_id, item_id):

            #print("Case: " + case_id)
            add_output_string += "\nAdded item: " + item_id
            for block in chain:
                if block.evidence_item_id == item_id:
                   add_output_string += "\n  Status: " + block.state
                   add_output_string += "\n  Time of action: " + block.time_stamp
        # exits with error if the item id was already added to the blockchain
        else:
            exit(1)

    print(add_output_string)
    save_to_file()

    return None


'''
bchoc checkout -i item_id
Add a new checkout entry to the chain of custody for the given evidence item. Checkout actions
may only be performed on evidence items that have already been added to the blockchain.
'''


def checkout():

    # need to find the last block with item_id i, and check whether it is checked in or checked out
    # iterate from the last element in reverse to find that element

    if commands[0] == '-i':
        item_id = commands[1]

        reverse_chain = chain[::-1]

        for b in reverse_chain:
            if item_id == b.evidence_item_id:
                if b.state == 'CHECKEDIN':   # need to add a new block 'transaction' at the end of the chain for the check out

                    previous_hash = get_last_block_hash()
                    # previous_hash, case_id, evidence_item_id, state, data, data_length = len(data.encode('utf-8')) + 1, time_stamp=get_current_time()
                    new_block = block.Block(previous_hash, b.case_id, item_id, 'CHECKEDOUT')
                    chain.append(new_block)
                    print("Case: " + new_block.case_id)
                    print("Checked out item: " + new_block.evidence_item_id)
                    print("  Status: " + new_block.state)
                    print("  Time of action: " + str(new_block.time_stamp))

                    return

                elif b.state == 'CHECKEDOUT':
                    print("Error: Cannot check out a checked out item. " +
                          "Must check it in first.")
                    #return 1
                    exit(1) #changed by Jared, if you do echo $? it says 0 unless
                    # you specify exit(1) instead of return 1
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
        for b in chain:
            if item_id == b.evidence_item_id:

                previous_hash = get_last_block_hash()
                # previous_hash, case_id, evidence_item_id, state, data, data_length = len(data.encode('utf-8')) + 1, time_stamp=get_current_time()
                new_block = block.Block(previous_hash, b.case_id, item_id, 'CHECKEDIN')
                chain.append(new_block)
                print("Case: " + new_block.case_id)
                print("Checked in item: " + new_block.evidence_item_id)
                print("  Status: " + new_block.state)
                print("  Time of action: " + str(new_block.time_stamp))
                return

                '''
                block.state = 'CHECKEDIN'
                block.time_stamp = get_current_time()
                print("Case: " + block.case_id)
                print("Checked in item: " + block.evidence_item_id)
                print("  Status: " + block.state)
                print("  Time of action: " + str(block.time_stamp))
                '''
    else:
        print("Invalid command")
        return 1

    return None


'''
bchoc log [-r] [-n num_entries] [-c case_id] [-i item_id]
Display the blockchain entries giving the oldest first (unless -r is given).
'''


def log(reverse, num_entries, item_id):

    count = 0

    # -1 means no -n amount was entered
    if num_entries == -1:
        num_entries = len(chain)

    # reverse if -r was used
    if reverse:
        c = chain[::-1]
    else:
        c = chain

    for block in c:

        # iterate through the chain and display the blocks with specified item id's information
        # if num_entries was provided the for loop iterates n times, otherwise it iterates the entire chain
        if item_id == block.evidence_item_id:
            count = count + 1
            print("Case: " + block.case_id)
            print("Item: " + block.evidence_item_id)
            print("Action: " + block.state)
            print("Time of action: " + block.time_stamp)
            print("")
            if count == num_entries:
                return


    return None


'''
bchoc remove -i item_id -y reason [-o owner]
Prevents any further action from being taken on the evidence item specified. The specified
item must have a state of CHECKEDIN for the action to succeed.
'''

def remove():

    released = False

    if commands[0] == '-i':
        commands.pop(0)
        item_id = commands[0]
        commands.pop(0)
        for b in chain[::-1]:
            if item_id == b.evidence_item_id:
                if b.state != "CHECKEDIN":
                    return
                if commands[0] == '-y' or commands[0] == '--why':
                    commands.pop(0)
                    state = commands[0]
                    if state == 'RELEASED':
                        released = True
                        commands.pop(0)
                        if commands[0] == '-o':
                            commands.pop(0)
                            new_block_data = commands[0].strip('\"')
                        else:
                            print("Need to add -o REASON")
                            return 1
                    elif state == 'DISPOSED' or state == 'DESTROYED':
                        state = state
                    else:
                        print("Invalid entry")
                        return 1
                else:
                    print("Invalid Syntax")
                    return 1
                print("Case: " + b.case_id)
                print("Removed item: " + b.evidence_item_id)
                print("  Status: " + state)
                if released:
                    print("  Owner info: " + new_block_data)
                print("  Time of action: " + b.time_stamp)

                previous_hash = get_last_block_hash()
                # previous_hash, case_id, evidence_item_id, state, data, data_length = len(data.encode('utf-8')) + 1, time_stamp=get_current_time()

                if released:
                    new_block = block.Block(previous_hash, b.case_id, b.evidence_item_id, state, new_block_data, len(
                    new_block_data.encode('utf-8')) + 1)

                else:
                    new_block = block.Block(previous_hash, b.case_id, b.evidence_item_id, state)

                chain.append(new_block)

                return None

        print("Item id not found")
        return 1
    else:
        print("Invalid Syntax")
        return 1

    return None


'''
bchoc init
Sanity check. Only starts up and checks for the initial block.
'''
def init():

    if read_from_file():
        print('Blockchain file found with INITIAL block.')
    else:
        print('Blockchain file not found. Created INITIAL block.')



def verify_parent_hashes():

    error_found = False
    real_previous_hash = hashlib.sha1(repr(chain[0]).encode('utf-8')).hexdigest()

    for block in chain[1:]:

        if block.previous_hash != real_previous_hash:
            print('State of blockchain: ERROR')
            print(f"Bad block: {hashlib.sha1(repr(block).encode('utf-8')).hexdigest()}")
            print('Parent block: NOT FOUND')
            return True
        else:
            real_previous_hash = hashlib.sha1(repr(block).encode('utf-8')).hexdigest()


    return False





'''
bchoc verify
Parse the blockchain and validate all entries.
'''
def verify():

    error = False

    print("Transactions in blockchain: " + str(len(chain)))
    # check for correct parent hashes. 
    error = verify_parent_hashes()

    # check that contents and checksum match



    if not error: print('State of blockchain: CLEAN')

''' runs certain function based on the command argument passed in '''


def run_commands(command):

    if command == 'init':
        init()
        exit(0)

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
        commands.remove('log')

        # ensures there is at least two commands given -i abc123
        if len(commands) < 2: 
            exit(1)

        if commands[0] == '-r' or commands[0] == '--reverse':
            reverse = True
            commands.pop(0)
        else:
            reverse = False
        if commands[0] == '-n':
            num_entries = int(commands[1])
            commands.pop(0)
            commands.pop(0)
        else:
            num_entries = -1

        if commands[0] == '-i':
            item_id = commands[1]
        else:
            print("no item id provided")
            return
        log(reverse, num_entries, item_id)

    elif command == 'remove':
        commands.remove('remove')
        remove()

    elif command == 'verify':
        verify()

    save_to_file()

# saves the list of blocks to a file


def save_to_file():

    with open(file_path, 'w') as filehandle:
        for block in chain:
            filehandle.write('%s\n' % block)


# reads and restores the saved blocks from file, and add to list 'chain'
# returns True if blockchain file was previous created
# returns False if no blockchain file was found
def read_from_file():
    l = []
    count = 0
    # define an empty list
    # open file and read the content in a list

    try:
        with open(file_path, 'r') as filehandle:

            for line in filehandle:
                # remove linebreak which is the last character of the string
                item = line[:-1]

                # add item to the list
                l.append(item)
                count = count + 1

                if count == 7:
                    #  previous_hash, case_id, evidence_item_id, state,data, data_length = len(data.encode('utf-8')) + 1, time_stamp=get_current_time()
                    b = block.Block(l[0], l[2],  l[3],  l[4], l[6], l[5], time_stamp=l[1])
                    chain.append(b)
                    l = []
                    count = 0
        
        return True

    except:
        # previous_hash, case_id, evidence_item_id, state, data, data_length = len(data.encode('utf-8')) + 1, time_stamp=get_current_time()
        b = block.Block(None, None, None, 'INITIAL', 'Initial block', 14)
        chain.append(b)
        save_to_file()

        return False






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

# save_to_file()

# for testing
#print(f"BLOCK CHAIN START\n{chain}")
