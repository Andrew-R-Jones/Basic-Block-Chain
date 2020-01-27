blockchain = [['1']]

def get_last_block():
    return blockchain[-1]


def add_value(transaction_data):
    blockchain.append([get_last_block(), transaction_data])


print(blockchain)


add_value('2')
add_value('3')
add_value('4')


print(blockchain)
