import subprocess
import time
import json

# Function to run a shell command and get the output
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {result.stderr}")
    return result.stdout.strip()

# RPC URL and private key
rpc_url = "https://rpc.cardona.zkevm-rpc.com"
private_key = "d3f1c6e55105bebef8309d8725f05c086e7e7f61fa4e3a57107428843bceb1d9"

# Deploy the LoopStorageContract
deploy_command = f"forge create --rpc-url {rpc_url} --private-key {private_key} src/LoopStorage.sol:LoopStorage --legacy"
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

print(f"LoopStorageContract deployed at address: {contract_address}")

# Define commands to interact with the contract
commands = [
    f"cast send {contract_address} 'storeValues(uint256)' 100 --rpc-url {rpc_url} --private-key {private_key} --legacy",
    f"cast call {contract_address} 'getValues()' --rpc-url {rpc_url} --legacy"
]

# Execute the commands and measure time taken
for i, command in enumerate(commands):
    start_time = time.time()  # Record the start time
    output = run_command(command)
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the time difference
    print(f"Command {i+1} output: {output}")
    print(f"Time for command {i+1}: {elapsed_time:.2f} seconds")
