import subprocess
import time
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Function to run a shell command and get the output
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {result.stderr}")
    return result.stdout.strip()

# Load the private key from the environment variables
private_key = os.getenv("PRIVATE_KEY")

if not private_key:
    raise Exception("Private key not found. Please set it in the .env file.")

# Deployed token addresses
kakarot_token_address = "0x3311CbBCc6E936c5129435a61A66cc70A52B6D28"
polygon_token_address = "0xDb998D816563dE12DC541a70d5838Aa1277d202a"

# Define the deployer address
deployer_address = "0x9b5623432dF06A583f7E2dDE6AD26507ae491FB0"
zero_address = "0x0000000000000000000000000000000000000000"

# RPC URLs
rpc_urls = {
    "kakarot": "https://sepolia-rpc.kakarot.org",
    "polygon": "https://rpc.cardona.zkevm-rpc.com"
}

# Function to check balance
def check_balance(network, token_address, account_address):
    rpc_url = rpc_urls[network]
    balance_command = f"cast call {token_address} 'balanceOf(address)' {account_address} --rpc-url {rpc_url}"
    balance = run_command(balance_command)
    return int(balance, 16)

# Function to test transfers
def test_transfers(network, token_address):
    rpc_url = rpc_urls[network]
    legacy_flag = "--legacy" if network == "polygon" else ""
    
    # Check initial balance
    initial_balance = check_balance(network, token_address, deployer_address)
    print(f"Initial balance on {network}: {initial_balance}")

    # Perform 2 transfers to the zero address
    for i in range(2):
        if initial_balance < 100:
            print(f"Insufficient balance for transfer {i+1} on {network}.")
            break
        
        transfer_command = f"cast send {token_address} 'transfer(address,uint256)' {zero_address} 100 --rpc-url {rpc_url} --private-key {private_key} {legacy_flag}"
        try:
            start_time = time.time()  # Record the start time
            run_command(transfer_command)
            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time  # Calculate the time difference
            print(f"Transfer {i+1} on {network} to zero address completed.")
            print(f"Time for transfer {i+1} on {network}: {elapsed_time:.2f} seconds")
            
            # Update initial_balance after each transfer
            initial_balance = check_balance(network, token_address, deployer_address)
        except Exception as e:
            print(f"Transfer {i+1} on {network} failed: {e}")

    # Check final balance
    final_balance = check_balance(network, token_address, deployer_address)
    print(f"Final balance on {network}: {final_balance}")

# Test transfers on Kakarot
print("Testing transfers on Kakarot...")
test_transfers("kakarot", kakarot_token_address)

# Test transfers on Polygon testnet
print("Testing transfers on Polygon...")
test_transfers("polygon", polygon_token_address)
