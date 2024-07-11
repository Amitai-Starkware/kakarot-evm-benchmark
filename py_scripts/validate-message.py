import os
import time
from web3 import Web3
from eth_account.messages import encode_defunct
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize Web3
rpc_url = "https://rpc.cardona.zkevm-rpc.com"
web3_polygon = Web3(Web3.HTTPProvider(rpc_url))

# Load the private key from the environment variables
private_key = os.getenv("PRIVATE_KEY")

if not private_key:
    raise Exception("Private key not found. Please set it in the .env file.")

# Validator contract address (assumed to be deployed already on Polygon)
validator_contract_address = "0xf76Fd0eB3EE37a0349012DAa73b585D849D53BB9"

# # Validator contract address (assumed to be deployed already on Polygon)
# validator_contract_address = "0x813ea23631fBD6B7d1Edf9f6F9A3a121a15e75aA"

# ABI of the Validator contract
validator_abi = [
    {
        "constant": True,
        "inputs": [
            {"name": "signer", "type": "address"},
            {"name": "message", "type": "bytes32"},
            {"name": "signature", "type": "bytes"}
        ],
        "name": "validateSignature",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "pure",
        "type": "function"
    }
]

# Function to sign a message
def sign_message(message, private_key):
    message_hash = Web3.keccak(text=message)
    message_encoded = encode_defunct(message_hash)
    signed_message = web3_polygon.eth.account.sign_message(message_encoded, private_key=private_key)
    return message_hash, signed_message.signature

# Function to validate signature on-chain
def validate_signature_on_chain(message_hash, signature):
    validator_contract = web3_polygon.eth.contract(address=validator_contract_address, abi=validator_abi)
    
    tx = validator_contract.functions.validateSignature(
        web3_polygon.eth.account.from_key(private_key).address,
        message_hash,
        signature
    ).call()
    
    return tx

# Test signature validation
def test_signature_validation():
    message = "Hello, Blockchain!"
    message_hash, signature = sign_message(message, private_key)
    
    print("Testing signature validation on Polygon...")
    is_valid = validate_signature_on_chain(message_hash, signature)
    print(f"Signature valid on Polygon: {is_valid}")

# Run the test
test_signature_validation()
