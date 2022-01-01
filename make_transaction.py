from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from colorama import Fore
import time
import json


class Transaction():


    def __init__(self, sender_wallet, sender_private_key, recipient_wallet, amount):
        self.sender_wallet = sender_wallet
        self.sender_private_key = sender_private_key
        self.recipient_wallet = recipient_wallet
        self.amount = amount
    

    def check_wallet_address(self):
        wallet_exist = False
        wallets_data = open("data/wallets.json", "r")
        load_wallets = json.load(wallets_data)

        for i in range(0,len(load_wallets["wallets"])+1):
            if load_wallets["wallets"][i]["wallet_address"] == self.sender_wallet:
                wallet_exist = True
                break

        return wallet_exist


    def check_amount(self):
        wallets_data = open("data/wallets.json", "r")
        load_wallets = json.load(wallets_data)
        balance = 0

        for i in load_wallets["wallets"]:
            if i["wallet_address"] == self.sender_wallet:
                balance = i["wallet_data"]["balance"]
                break

        if balance >= self.amount:
            return True

        else:
            return False
    

    def verify_signature(self, data, signature):
        wallets_file = open("data/wallets.json", "r")
        wallets_json = json.load(wallets_file)
        wallets_file.close()

        for i in wallets_json["wallets"]:
            if i["wallet_address"] == self.sender_wallet:
                public_key = RSA.import_key(bytes.fromhex(i["wallet_data"]["public_key"])) 
                sign_data = pkcs1_15.new(public_key)

                verification = sign_data.verify(
                    msg_hash=SHA256.new(data.encode()),
                    signature=bytes.fromhex(signature)
                )
                
                return verification
    

    def get_previous_block(self):
        chain_data = open("data/chain.json", "r")
        load_chain = json.load(chain_data)
        chain_data.close()

        previous_block = load_chain["blocks"][-1]["block_hash"]

        return previous_block


    def sign_transaction_data(self, transaction_data):
        private_key = RSA.import_key(bytes.fromhex(self.sender_private_key))
        sign_data = pkcs1_15.new(private_key)
        signed_transaction_data = sign_data.sign(SHA256.new(transaction_data.encode()))

        return signed_transaction_data.hex()


    def save_pending_transaction(self, transaction_data):
        pending_transaction_data = open("data/pending_transactions.json", "r+")
        load_pending_trnasaction = json.load(pending_transaction_data)

        add_pending_transaction = {
            "transaction": transaction_data
        }

        load_pending_trnasaction["pending_transactions"].append(add_pending_transaction)
        pending_transaction_data.seek(0)
        json.dump(load_pending_trnasaction, pending_transaction_data, indent=4)
        pending_transaction_data.close()


    def generate_genesis_block(self):
        msg = "Merhaba bugun mxt coin'in ilk kodunu yazdım."
        time_stamp = time.time()

        gb_json = json.dumps({
            "msg" : msg,
            "time_stamp": time_stamp
        }, indent=4).encode()

        gb_hash = SHA256.new(gb_json).hexdigest()
        chain_data = open("data/chain.json", "r+")
        load_chain = json.load(chain_data)
        
        block = {"block_hash": gb_hash}

        load_chain["blocks"].append(block)

        chain_data.seek(0)
        json.dump(load_chain, chain_data, indent=4)
        chain_data.close()


    def make_transaction(self):
        check_wallet_address = self.check_wallet_address()

        if check_wallet_address == True:
            check_amount = self.check_amount()

            if check_amount == True:
                time_stamp = time.time()

                transaction_data = {
                    "sender_wallet_address": self.sender_wallet,
                    "recipient_wallet_address": self.recipient_wallet,
                    "time_stamp": time_stamp,
                    "amount": self.amount
                }

                json_transaction_data = json.dumps(transaction_data, indent=4)
                signature = self.sign_transaction_data(json_transaction_data)

                try:
                    verification = self.verify_signature(json_transaction_data, signature)

                    transaction_data["contents"] = {
                        "signature": signature,
                        "previous_block": self.get_previous_block(),
                        "confirmed": False,
                        "worker_wallet_address": None,
                        "work": None
                    }

                    self.save_pending_transaction(transaction_data)

                    print(f"{Fore.GREEN}Your transaction waiting for mining!{Fore.RESET}")

                except ValueError:
                    print(f"{Fore.RED}Your private key was wrong!{Fore.RESET}")

            else:
                print(f"{Fore.RED}Wallets balance doesn't have enough money.{Fore.RESET}")

        else:
            print(f"{Fore.RED}Sender wallet address is not valid.{Fore.RESET}")




#TEST
dt = Transaction(
    "mxt_95769ec77082fb33bb5e160781187a071c3ad463875ff0074189d841899ad7fe",
    "3082025b020100028181009df416eb880cd402de4a8cc9a4c2e998d9c179aa0536f13b0eddea1772c6eff3ff802dc486d3d8c60ad07bdf7054058a3cd2be08aa1b706697f619cb47d402911e637a5179e942d5272726cbeb4bd31f652fdebd78626def559c7fd79308c726f4dd6d2c360269db0ff62944181c91ddd60ab63476ed9bc10486de73d7572eed0203010001028180148e352462306f2fcf5f6aca7c0d5c8a867e19f7f1154917eb33a078fc381cf6872fd664eeb9e78a405288e8574d2bea654774b11a78172cd6c6516d85b3b6c09919e03a8efeec5295bdefb8f6b75caf63f0b3532c0918ec654a3b452d29f1bb8e0b558b0c38f7d5651f224dc393539083e2b24c912ab2d84bd648f637b808d1024100c8736935ae355ebd7eed9701fe479f6f6a17a0f0b23fa7d74e46f24282381e855a784d01a767b51a18704ef913d2a7bf09716f47facc87f033a90980b5cc2b91024100c9b9c9ac1393ac93cd4773e44bfe1e7d0c16ae1bea68e487c98accc2f096d21d12d875c0d51112ada7219db93b691e9da2431c37c9f20e8a5ebe27e63237879d024008e0436a631a6de58a374f168181fe675a954d451b3f8259205837e6060a221fd98fb6293a9677087ec88a56b13004c98acb8117f8dd11afeb39b2f80614d261024001b61dcbe3eea0cc3035a6fa0cdaff0f388708bb1be5ffea56ff627554ed32a32481c99df530cbe3c54337bf568db1c0cc9b9d25ac04edb2a6d31e2b89c986d102406231180aafce0680863fa91c7c7eb517a7b9b12d06559fe0f44299ef77f804f54095e7305435bc7dcda3799e58f098598cde0e8ca44b6fa3ea4e98a34c4b8466",
    "mxt_0b0cee1cc3714754f4ab8119e096283437ea67ceb7ba514f994b62bc2017641a",
    10
    ) 

dt.make_transaction()