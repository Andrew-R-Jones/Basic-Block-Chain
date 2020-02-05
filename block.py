import maya

# block class
class Block: 

    # instantiates block for blockchain
    def __init__(self, previous_hash, case_id, item_id, evidence_item_id, data):
        self.previos_hash = previous_hash
        self.case_id = case_id
        self.evidence_item_id = evidence_item_id
        self.Timestamp = (maya.now()).iso8601()
        self.state = None
        self.data = data
        self.data_length = len(data.encode('utf-8'))

    ''' similar to toString, returns info about the object'''
    def __repr__(self):
        return f"BLOCK INFORMATION\nPrevious Hash: {self.previos_hash}\nTimestamp: {self.Timestamp}\nCase ID: {self.case_id}\nEvidence Item ID: {self.item_id}\nStae: {self.state}\nData Length: {self.data_length} Bytes\nData: {self.data}"

# test data for creating new block
b = Block('65cc391d-6568-4dcc-a3f1-86a2f04140f3', '987654321', 1234, 852963, "this is the data section.")
print(b)
