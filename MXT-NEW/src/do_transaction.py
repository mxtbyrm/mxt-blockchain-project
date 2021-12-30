import time
import hashlib
import string
import random
import json

class Transaction():
    def __init__(self, sender_wallet, sender_signature,reciever_wallet, amount):
        self.sender_wallet = sender_wallet
        self.sender_signature = sender_signature 
        self.reciever_wallet = reciever_wallet
        self.difficulty = 4
        self.amount = amount

    def check_wallet_address(self):
        wallets = open("src/data/wallets.json", "r")
        wallets_json = json.load(wallets)
        wallets.close()
        valid_sender = False
        valid_reciever = False
        for i in wallets_json["wallets"]:
            if i["wallet_address"] == self.sender_wallet:
                valid_sender = True
                break
        for i in wallets_json["wallets"]:
            if i["wallet_address"] == self.reciever_wallet:
                valid_reciever = True
                break
        is_valid = (valid_sender, valid_reciever)
        return is_valid

    def save_transaction(self, block):
        chain = open("src/data/chain.json", "r+")
        chain_json = json.load(chain)
        chain_json["blocks"].append(block)
        chain.seek(0)
        json.dump(chain_json, chain, indent=4)
        chain.truncate()

    def modify_amount(self):
        wallets = open("src/data/wallets.json", "r+")
        wallets_json = json.load(wallets)
        modify_sender = False
        modify_reciever = False
        for i in wallets_json["wallets"]:
            if modify_reciever == True and modify_sender == True:
                break
            if i["wallet_address"] == self.sender_wallet:
                i["wallet_data"]["balance"] -= self.amount
                modify_sender = True
            if i["wallet_address"] == self.reciever_wallet:
                i["wallet_data"]["balance"] += self.amount
                modify_reciever = True
        wallets.seek(0)
        json.dump(wallets_json, wallets, indent=4)
        wallets.truncate()

    def check_amount(self):
        wallets = open("src/data/wallets.json", "r")
        wallets_json = json.load(wallets)
        wallets.close()
        for i in wallets_json["wallets"]:
            if i["wallet_address"] == self.sender_wallet:
                if i["wallet_data"]["balance"] >= self.amount:
                    return True
                elif i["wallet_data"]["balance"] < self.amount:
                    return False

    def validate_signature(self):
        wallets = open("src/data/wallets.json", "r")
        wallets_json = json.load(wallets)
        wallets.close()
        for i in wallets_json["wallets"]:
            if i["wallet_address"] == self.sender_wallet:
                if i["wallet_data"]["wallet_signature"] == self.sender_signature:
                    return True
                elif i["wallet_data"]["wallet_signature"] != self.sender_signature:
                    return False
    
    def previous_block(self):
        blocks = open("src/data/chain.json", "r")
        blocks_json = json.load(blocks)
        blocks.close()
        previous_block = blocks_json["blocks"][-1]["block"]
        return previous_block

    def do_transaction(self):
        valid_sender, valid_reciever = self.check_wallet_address()
        if valid_sender == True and valid_reciever == True:
            verified = self.validate_signature()
            check_amount = self.check_amount()
            if check_amount:
                if verified == True:
                    while True:
                        nonce = random.randint(100000000, 1000000000)
                        time_now = time.time()
                        block_json = {
                            "sender_wallet" : self.sender_wallet,
                            "reciever_wallet" : self.reciever_wallet,
                            "parent" : self.previous_block(),
                            "transaction" : {
                                "local_time" : time_now,
                                "signature" : hashlib.sha256(
                                    json.dumps({
                                        "local_time" : time_now,
                                        "sender_signature" : self.sender_signature,
                                        "random_key" : "".join(
                                            random.choices(
                                                string.digits, k = 100
                                                )
                                            )
                                        }
                                    ).encode()
                                ).hexdigest(),
                                "amount" : self.amount
                            },
                            "nonce" : nonce
                        }
                        block_hash = hashlib.sha256(json.dumps(block_json, indent=4).encode()).hexdigest()
                        if block_hash.startswith(self.difficulty*"0"):
                            block_hash = "mxt_"+block_hash
                            block = {"block" : block_hash, "transaction":block_json}
                            self.save_transaction(block)
                            self.modify_amount()
                            break
                        else:
                            continue
                else:
                    print("Your signature didin't match with sender wallet.")
            else:
                print("Your amount isn't enough to send that much MXT.")
        else:
            print("Incorrect sender or reciever wallet")

    def generate_genesis_block(self):
        time_now = time.time()
        paragraph = "Twenty-five stars were neatly placed on the piece of paper. There was room for five more stars but they would be difficult ones to earn. It had taken years to earn the first twenty-five, and they were considered the 'easy' ones."
        json_genesis = {"local_time" : time_now, "paragraph": paragraph}
        json_genesis = json.dumps(json_genesis, indent=4)
        blocks = {"blocks" : ["mxt_"+hashlib.sha256(json_genesis.encode()).hexdigest()]}
        chain = open("src/data/chain.json", "r+")
        json.dump(blocks, chain, indent=4)
        chain.close()

if __name__ == "__main__":
    sender_addr = input("Sender wallet address: ")
    sender_sign = input("Sender signature: ")
    reciever_addr = input("Reciever address: ")
    amount = float(input("Amount: "))
    dt = Transaction(sender_addr, sender_sign, reciever_addr, amount)
    dt.do_transaction()
