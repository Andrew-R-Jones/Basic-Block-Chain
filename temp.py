import struct
import hashlib
from functools import partial
from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone

def remove():
    released = False

    if commands[0] == '-i':
        commands.pop(0)
        item_id = commands[0]
        commands.pop(0)
        chain = make_chain()
        #flags to set and check before packing
        checked_in = False #determine the last status of the item
        found = False #check if the item has been in block
        released = False
        pack_item = 0
        pack_data = ""
        pack_state = ""
        pack_case = 0
        status = ""
        for b in chain[::-1]:
            if item_id == str(b.evidence_item_id):
                found = True
                pack_case = b.case_id
                pack_item = b.evidence_item_id
                pack_state = b.state
                if b.state.strip(' \t\r\n\0') == "CHECKEDIN":
                    checked_in = True
                elif b.state.strip(' \t\r\n\0') == "CHECKEDOUT":
                    checked_in = False
                if commands[0] == '-y' or commands[0] == '--why':
                    commands.pop(0)
                    state = commands[0]
                    status = state
                    if state == 'RELEASED':
                        released = True
                        if len(commands) < 2:
                            print("if released must give owner info")
                            exit(1)
                        commands.pop(0)
                        if commands[0] == '-o':
                            commands.pop(0)
                            pack_data = commands[0].strip('\"')
                        else:
                            print("Need to add -o REASON")
                            exit(1)
                    elif state == 'DISPOSED' or state == 'DESTROYED':
                         released=released # do nothing command
                    else:
                        print("Invalid entry")
                        exit(1)
        #move everything out of the for loop so we can check flags
        if checked_in == False:
            print("can not remove checked out item")
            exit(1)
        print("Case: " + str(b.case_id))
        print("Removed item: " + str(b.evidence_item_id))
        print("  Status: " + status)
        if released:
            print("  Owner info: " + pack_data)
        print("  Time of action: " + get_current_time())
                
        if released:
            block.pack_block(pack_case, pack_item, pack_state, datetime.utcnow().timestamp(),pack_data)
        else:
            if debug:
                print("################################################################Else pack_case:",pack_case)
            block.pack_block(pack_case, pack_item, pack_state, datetime.utcnow().timestamp(),pack_data)
        print("Item id not found")
        exit(1)
    else:
        print("Invalid Syntax")
        exit(1)

    return None