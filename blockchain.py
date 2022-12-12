import time
import hashlib

class Block:

    def __init__(self , data, previous_hash ,block_no):
        self.data = data
        self.previous_hash = previous_hash
        self.block_no = block_no
        self.hash = 0
        self.nonce = 0 
        self.timestamp = 0


if __name__ == "__main__":
    print("hello world")
