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
rpc_url = "https://sepolia-rpc.kakarot.org"
private_key = "d3f1c6e55105bebef8309d8725f05c086e7e7f61fa4e3a57107428843bceb1d9"

# Deploy the ComplexContract
deploy_command = f"forge create --rpc-url {rpc_url} --private-key {private_key} src/ComplexContract.sol:ComplexContract"
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

print(f"ComplexContract deployed at address: {contract_address}")

# Define commands to interact with the contract
commands = [
    f"cast send {contract_address} 'incrementCounter()' --rpc-url {rpc_url} --private-key {private_key}",
    f"cast send {contract_address} 'addValue(uint256,uint256)' 1 100 --rpc-url {rpc_url} --private-key {private_key}",
    f"cast call {contract_address} 'computeFactorial(uint256)' 5 --rpc-url {rpc_url}",
    f"cast call {contract_address} 'findMax(uint256[])' '[1,2,3,4,5]' --rpc-url {rpc_url}",
    f"cast call {contract_address} 'calculateSum(uint256[])' '[1,2,3,4,5]' --rpc-url {rpc_url}"
]

# Execute the commands and measure time taken
for i, command in enumerate(commands):
    start_time = time.time()  # Record the start time
    output = run_command(command)
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the time difference
    print(f"Command {i+1} output: {output}")
    print(f"Time for command {i+1}: {elapsed_time:.2f} seconds")
