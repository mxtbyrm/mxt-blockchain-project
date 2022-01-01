from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from colorama import Fore
import time
import json
from random import choices
from string import ascii_letters, digits

class Generate_Wallet():
    def __init__(self):
        None
    
    def generate_keys(self):
        private_key = RSA.generate(1024)
        private_key_export = private_key.export_key("DER").hex()

        public_key = private_key.public_key()
        public_key_export = public_key.export_key("DER").hex()

        return (private_key_export, public_key_export)

    def save_wallet(self, wallet_address, balance, public_key, time_stamp):
        wallets_file = open("data/wallets.json", "r+")

        wallet_import = json.load(wallets_file)
        
        create_new_wallet_dict = {
            "wallet_address" : wallet_address,
            "wallet_data" : {
                "balance" : balance,
                "time_stamp": time_stamp,
                "public_key" : public_key
            }
        }

        wallet_import["wallets"].append(create_new_wallet_dict)

        wallets_file.seek(0)
        json.dump(wallet_import, wallets_file, indent=4)
        wallets_file.close()

    
    def generate_wallet(self):
        random_string = "".join(choices(ascii_letters + digits, k = 125))
        time_stamp = time.time()
        private_key, public_key = self.generate_keys()
        balance = 0.0

        wallet_address_data = {
            "random_key": random_string,
            "time_stamp" : time_stamp
        }

        wallet_address_json = json.dumps(wallet_address_data, indent=4)
        wallet_hash = "mxt_"+SHA256.new(wallet_address_json.encode()).hexdigest()

        self.save_wallet(wallet_hash, balance, public_key, time_stamp)
        
        print(f"Your wallet address: {Fore.GREEN}{wallet_hash}{Fore.RESET}")
        print(f"Your balance: {Fore.GREEN}{balance} MXT{Fore.RESET}")
        print(f"Your public key: {Fore.GREEN}{public_key}{Fore.RESET}")
        print(f"Your private key {Fore.RED}(Don't lose and don't share with anybody!){Fore.RESET}: {Fore.YELLOW}{private_key}{Fore.RESET}")

if __name__ == "__main__":
    gw = Generate_Wallet()
    gw.generate_wallet()