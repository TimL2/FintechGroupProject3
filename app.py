import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from datetime import date
# Image allows for open, save, show of images
# ImageDraw allows editting of image
# ImageFont allows choice of font
from PIL import Image, ImageDraw, ImageFont

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
industries = ['Agriculture/AgTech', 'Basic Metal Production', 'Chemical', 'Commerce', 'Construction', 'Education/EdTech', 'Financial Services/FinTech', 'Food', 'Forestry',
                'Health Services', 'Hotels/Tourism/Catering', 'Mechanical/Electrical Engineering', 'Media', 'Oil and Gas Production', 'Postal/Telecommunications', 
                'Public Services', 'Shipping', 'Textiles', 'Transport', 'Transport Equipment Manufacturing', 'Utilities']
business_name = st.text_input("Enter the name of the business")
owner_name = st.text_input("Enter the owner's/LLC's name")
phone_number = st.text_input("Enter the company phone number")
business_uri = st.text_input("Enter the business website")
industry_name = st.selectbox("Desired Industry", options=industries)
current_time = date.today().strftime("%b-%d-%Y")


if st.button("Register Business"):
    tx_hash = contract.functions.registerBusiness(
        address,
        business_name,
        owner_name,
        int(phone_number),
        industry_name,
        business_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    t_id = contract.functions.totalSupply().call()
    # assign variable name and open image
    NFT = Image.open('./images/default.png')

    # convert image into editable form
    edit = ImageDraw.Draw(NFT)

    # Font selection
    myFont = ImageFont.truetype('./fonts/futur.TTF', 55)
    tokenFont = ImageFont.truetype('./fonts/Filxgirl.TTF', 75)

    edit.text((15, 30), business_name, fill =(255, 0, 0), font=myFont)
    edit.text((15, 123), industry_name, fill =(255, 0, 0), font=myFont)
    edit.text((15, 216), business_uri, fill =(255, 0, 0), font=myFont)
    edit.text((900, 315), str(t_id-1), fill = (0, 0, 0), font=tokenFont)
    edit.text((450, 315), current_time, fill = (255, 255, 255), font=tokenFont)

    # show and save the image

    NFT.show()
    NFT.save('./images/business_NFT.png')
    st.markdown("---")


################################################################################
# Edit Registry
################################################################################
st.markdown("## Edit Business Registry")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose a Business Registry Token ID", list(range(tokens)))
new_phone_number = st.text_input("Enter the new phone number")
report_uri = st.text_area("Enter notes about the change")

if st.button("Submit Edits"):

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
business_token_id = st.selectbox("Business ID", list(range(tokens)))
if st.button("Get Business Registry"):
    business_filter = contract.events.Transfer.createFilter(
        fromBlock=0,
        argument_filters={"tokenId": business_token_id}
    )
    edit_filter = contract.events.editRegistry.createFilter(
        fromBlock=0,
        argument_filters={"tokenId": business_token_id}
    )
    st.markdown("### Business Registry Event Log")
    history = business_filter.get_all_entries()
    if history:
        for hist in history:
            report_dictionary = dict(hist)
            st.write(report_dictionary)
    else:
        st.write("This business has no history")
    st.markdown("### Registry Edits") 
    edit_history = edit_filter.get_all_entries()
    if edit_history:
        for hist in edit_history:
            report_dictionary = dict(hist)
            st.write(report_dictionary)
    else:
        st.write("This business has no edits")        
            
            
    token_details = contract.functions.businessListing(business_token_id).call()
    st.markdown("### Current Business Registry Details")
    st.write(f'Name:     {token_details[0]}')
    st.write(f'Owner:     {token_details[1]}')
    st.write(f'Phone:     {token_details[2]}')
    st.write(f'Industry:     {token_details[3]}')
    