import maya

def get_current_time():
    return (maya.now()).iso8601()


def get_data_length(data):
    # add 1 for null char
    return len(data.encode('utf-8')) + 1

# block class
class Block: 

    # instantiates block for blockchain
    def __init__(self, previous_hash, case_id, evidence_item_id, state, data=None, data_length=None, time_stamp=get_current_time()):
        self.previous_hash = previous_hash
        self.case_id = case_id
        self.evidence_item_id = evidence_item_id
        self.state = state
        self.data = data
        self.data_length = data_length
        self.time_stamp = time_stamp


    ''' similar to toString, returns info about the object'''
    def __repr__(self):
        return f"{self.previous_hash}\n{self.time_stamp}\n{self.case_id}\n{self.evidence_item_id}\n{self.state}\n{self.data_length}\n{self.data}"



#test data for creating new block
#b = Block('65cc391d-6568-4dcc-a3f1-86a2f04140f3', '987654321', 852963, 'INITIAL' ,"this is the data section.")
#print(b)
