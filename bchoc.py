#!/usr/bin/python3

import sys
import block
import hashlib
import os
import struct
import os.path
from os import path
from block import get_current_time
from block import make_chain
import datetime
from datetime import datetime, timedelta, timezone

########################################################################################
###############     FOR SUBMISSION      ################################################
#file_path = os.environ["BCHOC_FILE_PATH"]
#debug = False
###############     FOR DUBUG AND TESTING       ########################################
file_path = 'blockchain'
debug = True
########################################################################################
if (path.exists(file_path) == False): #check if there is a file yet
    open(file_path, 'w').close() #create the file


chain = [] # global list that will hold all blocks and will create the chain

# returns true if the item was found in the block chain. false, if it was not found
# return exit code 1 if the block was found in the chain with a released state
def in_chain(item_id):
    chain = make_chain()
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
    chain = make_chain()
    last_block = chain[-1]
    sha1 = hashlib.sha1(repr(last_block).encode('utf-8')).hexdigest()
    return sha1


def add_to_block_chain(case_id, item_id):
    if debug:
        print("add to block ITEMID:",item_id)
    #make sure item_id is type int
    item_id= int(item_id)
    if not in_chain(item_id):
        block.pack_block(case_id,item_id, "CHECKEDIN",datetime.utcnow().timestamp(),"")
        return True
    else: 
        return False


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
        if debug:
            print("at input item_id:", item_id)
        if add_to_block_chain(case_id, item_id):
            add_output_string += "\nAdded item: " + item_id
            for block in chain:
                if block.evidence_item_id == item_id:
                   add_output_string += "\n  Status: " + block.state
                   add_output_string += "\n  Time of action: " + block.time_stamp
        # exits with error if the item id was already added to the blockchain
        else:
            exit(1)

    print(add_output_string)

    return None


'''
bchoc checkout -i item_id
Add a new checkout entry to the chain of custody for the given evidence item. Checkout actions
may only be performed on evidence items that have already been added to the blockchain.
'''


def checkout():
    #

    if commands[0] == '-i':
        item_id = commands[1]
        chain = make_chain()
        reverse_chain = chain[::-1]
        found = False
        disposed = False
        destroyed = False
        released = False
        for b in reverse_chain:
            print(b.evidence_item_id)
            if int(item_id) == b.evidence_item_id:
                found=True
                state_val = b.state.strip(' \t\r\n\0') #strip padding


                if state_val == 'CHECKEDIN':   # need to add a new block 'transaction' at the end of the chain for the check out
                    timestamp=datetime.utcnow().timestamp()
                    state_val = 'CHECKEDOUT'
                    block.pack_block(b.case_id, b.evidence_item_id, state_val, timestamp,"")
                    #got to get the timestamp..... need to add state and timestamp
                    print("Case: " + str(b.case_id))
                    print("Checked out item: " + str(b.evidence_item_id))
                    print("  Status: " + state_val)
                    print("  Time of action: " + str(timestamp))
                    return

                elif b.state == 'CHECKEDOUT':
                    print("Error: Cannot check out a checked out item. " +
                          "Must check it in first.")
                    #return 1
                    exit(1) #changed by Jared, if you do echo $? it says 0 unless
                    # you specify exit(1) instead of return 1
        if not found:
            print("item not found in the block")
            exit(1)
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
        found = False
        chain = make_chain()
        case = 0
        evidence = 0
        checked_in = True
        disposed = False
        destroyed = False
        released = False
        for b in chain:
            if item_id == str(b.evidence_item_id):
                found=True
                case = b.case_id
                evidence = b.evidence_item_id
                if b.state.strip(' \t\r\n\0') == "CHECKEDIN":
                    checked_in = True
                elif b.state.strip(' \t\r\n\0') == "CHECKEDOUT":
                    checked_in = False
                elif b.state.strip(' \t\r\n\0') == "DESTROYED":
                    destroyed = True
                elif b.state.strip(' \t\r\n\0') == "DISPOSED":
                    disposed = True
        if not found:
            print("Item not in blockChain")
            exit(1)
        if disposed:
            print("cannot checkin item that has been disposed")
            exit(1)
        if checked_in:
            print("error already checked in")
            exit(1)

        block.pack_block(case,evidence,"CHECKEDIN",datetime.utcnow().timestamp(),"")
        print("Case: " + str(case))
        print("Checked in item: " + str(evidence))
        print("  Status: " + "CHECKEDIN")
        print("  Time of action: " + get_current_time())
        return 
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
        chain = make_chain()
        checked_in = False #determine the last status of the item
        found = False #check if the item has been in block
        pack_item = 0
        pack_data = ""
        pack_state = ""
        pack_case = 0
        for b in chain[::-1]:
            if item_id == str(b.evidence_item_id):
                found = True
                released = False
                pack_case = b.case_id
                pack_item = b.evidence_item_id
                if b.state.strip(' \t\r\n\0') == "CHECKEDIN":
                    checked_in = True
                elif b.state.strip(' \t\r\n\0') == "CHECKEDOUT":
                    checked_in = False
                if commands[0] == '-y' or commands[0] == '--why':
                    commands.pop(0)
                    state = commands[0]
                    pack_state = state
                    if state == 'RELEASED':
                        released = True
                        commands.pop(0)
                        if commands[0] == '-o':
                            commands.pop(0)
                            pack_data = commands[0].strip('\"')
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
                print("Case: " + str(b.case_id))
                print("Removed item: " + str(b.evidence_item_id))
                print("  Status: " + state)
                if released:
                    print("  Owner info: " + pack_data)
                print("  Time of action: " + get_current_time())
                
                if released:
                    block.pack_block(pack_case, pack_item, pack_state, datetime.utcnow().timestamp(),pack_data)
                else:
                    if debug:
                        print("################################################################Else pack_case:",pack_case)
                    block.pack_block(pack_case, pack_item, pack_state, datetime.utcnow().timestamp(),pack_data)

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
    chain = make_chain()
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


def check_duplicate_parents():

    chain = make_chain()
    parent_list = []


    for block in chain:

        parent_hash = block.previous_hash
            
        # checks for duplicate of parent hash
        if parent_hash in parent_list: 
            print('State of blockchain: ERROR')
            print(f"Bad block: {hashlib.sha1(repr(block).encode('utf-8')).hexdigest()}")
            print(f"Parent block: {block.previous_hash}")
            print('Two blocks found with same parent.')
            return True
        # otherwise add the hash to the list
        else:
            parent_list.append(parent_hash)
    return False


# Block contents do not match block checksum.
# Pretty sure this is covered when the parent hashes
# if anything is altered, the hashes would be wrong and therefore
# the checksums would also fail..
def confirm_checksums():

    return False


# this function checks that any removed blocks have not been
# checked back in or out after the removal

def confirm_removed():

    index = 0

    # nested for loop to match each block to the rest of the blocks 
    for block in range(len(chain)):

        if block.state == 'RELEASED' or block.state == 'DISPOSED' or block.state == 'DESTROYED':
            print('chill pythohn lol')

            #iterate the rest of the chain to confirm the item was not checked back in or out
            for b in chain[index:]:
                if b.state == 'CHECKEDIN' or b.state == 'CHECKEDOUT':
                    print('State of blockchain: ERROR')
                    print(f"Bad block: {hashlib.sha1(repr(block).encode('utf-8')).hexdigest()}")
                    print('Item checked out or checked in after removal from chain.')
                    return True
        else:
            index = index + 1

    return False


'''
bchoc verify
Parse the blockchain and validate all entries.
'''
def verify():

    error = False

    print("Transactions in blockchain: " + str(len(chain)))
    # check for correct parent hashes. 
    if check_duplicate_parents():
        exit(1)
    elif verify_parent_hashes():
        exit(1)
    elif confirm_checksums():
        exit(1)
    elif confirm_removed():
        exit(1)
    
    else:
        print('State of blockchain: CLEAN')

    # check that contents and checksum match



''' runs certain function based on the command argument passed in '''


def run_commands(command):

    if command == 'init':
        if len(commands) > 1:
            print("too many parameters")
            exit(1)
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


# saves the list of blocks to a file
def read_from_file():
    #get the chain from block
    chain = make_chain()
    if len(chain) == 0:
        timestamp = datetime.utcnow().timestamp()
        block.pack_block(0,0,"INITIAL",timestamp,"") #initial block paramters
        chain = make_chain() #chain now holds init block might not need it
        return False
    else:
        return True
      
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
