import datetime
import maya


class Block:


    def __init__(self, case_id, item_id):
        self.case_id = case_id
        self.item_id = item_id
        self.Timestamp = (maya.now()).iso8601()
        self.state = None


    def __repr__(self):
        return f"BLOCK INFORMATION\nCase ID Hash: {self.case_id}\nEvidence Item ID: {self.item_id}\nTimestamp: {self.Timestamp}"


##dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)

'''
print(dir(datetime))
now = datetime.datetime.today()

now2 = maya.now()


print(now)
print(now2)
print(now2.iso8601())
'''
b = Block('65cc391d65684dcca3f186a2f04140f3', '987654321')
print(b)


previous_hash = 0
transactions = []
block_hash = 0
