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

# RPC URLs
rpc_urls = {
    "kakarot": "https://sepolia-rpc.kakarot.org",
    "polygon": "https://rpc.cardona.zkevm-rpc.com"
}

# Load the private key from the environment variables
private_key = os.getenv("PRIVATE_KEY")

if not private_key:
    raise Exception("Private key not found. Please set it in the .env file.")

# Function to deploy the Counter contract and return the contract address
def deploy_contract(network):
    rpc_url = rpc_urls[network]
    legacy_flag = "--legacy" if network == "polygon" else ""
    deploy_command = f"forge create --rpc-url {rpc_url} --private-key {private_key} {legacy_flag} src/Counter.sol:Counter"
    deploy_output = run_command(deploy_command)
    print(deploy_output)

    # Extract the contract address from the deploy output
    contract_address = None
    for line in deploy_output.split('\n'):
        if 'Deployed to' in line:
            contract_address = line.split()[-1]
            break

    if not contract_address:
        raise Exception("Failed to get the contract address")

    print(f"Counter contract deployed on {network} at address: {contract_address}")
    return contract_address

# Function to increment the counter and check its value
def increment_counter(network, contract_address):
    rpc_url = rpc_urls[network]
    legacy_flag = "--legacy" if network == "polygon" else ""
    
    for i in range(5):
        start_time = time.time()  # Record the start time
        increment_command = f"cast send {contract_address} 'increment()' --rpc-url {rpc_url} --private-key {private_key} {legacy_flag}"
        run_command(increment_command)
        print(f"Transaction {i+1} sent.")

        # Wait for a short period to ensure the transaction is processed
        time.sleep(15)  # Adjust the sleep time if necessary

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the time difference
        print(f"Time between transaction {i+1} and next: {elapsed_time:.2f} seconds")

        # Check the counter value after each increment
        get_counter_value_command = f"cast call {contract_address} 'get()' --rpc-url {rpc_url} {legacy_flag}"
        current_counter_value = int(run_command(get_counter_value_command), 16)
        print(f"Counter value after transaction {i+1}: {current_counter_value}")

    # Ensure the counter is above 5
    final_counter_value = int(run_command(get_counter_value_command), 16)
    if final_counter_value > 5:
        print(f"Final counter value is {final_counter_value}, which is above 5.")
    else:
        print(f"Final counter value is {final_counter_value}, which is not above 5.")
        raise Exception("Final counter value is not above 5.")

# Deploy and test on Kakarot
kakarot_contract_address = deploy_contract("kakarot")
increment_counter("kakarot", kakarot_contract_address)

# Deploy and test on Polygon testnet
polygon_contract_address = deploy_contract("polygon")
increment_counter("polygon", polygon_contract_address)
