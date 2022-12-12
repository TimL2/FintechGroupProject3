import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/businessregistry_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()


st.title("Business Registry System")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# Register New Business
################################################################################
st.markdown("## Register a New Business")

business_name = st.text_input("Enter the name of the business")
owner_name = st.text_input("Enter the owner's/LLC's name")
phone_number = st.text_input("Enter the company phone number")
business_uri = st.text_input("Enter the business website")

if st.button("Register Business"):
    tx_hash = contract.functions.registerBusiness(
        address,
        business_name,
        owner_name,
        int(phone_number),
        business_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")


################################################################################
# Edit Registry
################################################################################
st.markdown("## Edit Business Registry")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose a Business Registry Token ID", list(range(tokens)))
new_phone_number = st.text_input("Enter the new phone number")
report_uri = st.text_area("Enter notes about the change")
if st.button("Sumbmit Edits"):

    # Use the token_id and the report_uri to record the appraisal
    tx_hash = contract.functions.editPhoneNumber(
        token_id,
        int(new_phone_number),
        report_uri
    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Business Record
################################################################################
st.markdown("## Get the business registry history")
business_token_id = st.number_input("Business ID", value=0, step=1)
if st.button("Get Business Registry"):
    business_filter = contract.events.editRegistry.createFilter(
        fromBlock=0,
        argument_filters={"tokenId": business_token_id}
    )
    history = business_filter.get_all_entries()
    if history:
        for hist in history:
            report_dictionary = dict(hist)
            st.markdown("### Business Registry Event Log")
            st.write(report_dictionary)
            st.markdown("### Business Registry Details")
            st.write(report_dictionary["args"])
    else:
        st.write("This business has no history")
