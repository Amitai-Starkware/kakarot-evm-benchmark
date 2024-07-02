import subprocess
import time

# Function to run a shell command and get the output
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {result.stderr}")
    return result.stdout.strip()

# RPC URL and private key
rpc_url = "https://sepolia-rpc.kakarot.org"
private_key = "d3f1c6e55105bebef8309d8725f05c086e7e7f61fa4e3a57107428843bceb1d9"

# Deploy the Counter contract
deploy_command = f"forge create --rpc-url {rpc_url} --private-key {private_key} src/Counter.sol:Counter"
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

print(f"Counter contract deployed at address: {contract_address}")

# Increment the counter 5 times
for i in range(5):
    start_time = time.time()  # Record the start time
    increment_command = f"cast send {contract_address} 'increment()' --rpc-url {rpc_url} --private-key {private_key}"
    run_command(increment_command)
    print(f"Transaction {i+1} sent.")
    
    # Wait for a short period to ensure the transaction is processed
    time.sleep(15)  # Adjust the sleep time if necessary

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the time difference
    print(f"Time between transaction {i+1} and next: {elapsed_time:.2f} seconds")

    # Check the counter value after each increment
    current_counter_value = int(run_command(get_counter_value_command), 16)
    print(f"Counter value after transaction {i+1}: {current_counter_value}")

# Ensure the counter is above 5
final_counter_value = int(run_command(get_counter_value_command), 16)
if final_counter_value > 5:
    print(f"Final counter value is {final_counter_value}, which is above 5.")
else:
    print(f"Final counter value is {final_counter_value}, which is not above 5.")
    raise Exception("Final counter value is not above 5.")
