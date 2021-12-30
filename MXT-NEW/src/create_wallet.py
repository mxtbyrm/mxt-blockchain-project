# Copyright (c) 2021 Sm4rtyF0x
# Importing additional libraries
import hashlib
import json
import random
import time
from string import ascii_letters, digits

# Creating generate wallet class 
class GenerateWallet():
    def __init__(self) -> None:
        self.time = time.time()    
    
    # Generating wallet signature for wallet address.
    def generate_signature(self, wallet_address):
        while True:
            random_key = "".join(random.choices(ascii_letters + digits, k=100))
            store_signature_data = {"local_time" : self.time, "unique_key" : random_key, "wallet_address" : wallet_address}
            json_signature_data = json.dumps(store_signature_data, indent=4)
            signature = hashlib.sha256(json_signature_data.encode()).hexdigest()
            if signature.startswith("00") and signature.endswith("00"):
                return "mxt_"+signature
    
    # Generating wallet address for new user.
    def generate_wallet(self):
        random_key = "".join(random.choices(ascii_letters + digits, k=100))
        store_wallet_data = {"local_time" : self.time, "unique_key" : random_key}
        json_wallet_data = json.dumps(store_wallet_data, indent=4)
        wallet_address = hashlib.sha256(json_wallet_data.encode()).hexdigest()
        return "mxt_"+wallet_address
    
    # Saving wallet data to wallets.json file
    def save_wallet(self):
        wallet_address = self.generate_wallet()
        wallet_signature = self.generate_signature(wallet_address)
        print("Your wallet address: "+wallet_address)
        print("Your secret wallet signature (don't share): "+wallet_signature)
        json_file = open("src/data/wallets.json", "r+")
        load_json = json.load(json_file)
        load_json["wallets"].append({"wallet_address" : wallet_address, "wallet_data" : {"wallet_signature" : wallet_signature, "balance" : 0}})
        json_file.seek(0)
        json.dump(load_json, json_file, indent=4)
        json_file.close()

        
# Running generate wallet
gw = GenerateWallet()
gw.save_wallet()
