import requests

file = open("./images/business_NFT.png", "rb")

query_params = {
    "chain": "polygon",
    "name": "NFT_Name",
    "description": "NFT_Description",
    "mint_to_address": 0xCa96e1565b570E10eA4d5bB6c05c98E63d3Adf37
}

response = requests.post(
    "https://api.nftport.xyz/v0/mints/easy/files",
    headers={"Authorization": "c4c68964-e234-4067-a0d3-93d673794589"},
    params=query_params,
    files={"file": file}
)