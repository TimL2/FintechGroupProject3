import requests

import http.client

conn = http.client.HTTPSConnection("api.nftport.xyz")

headers = {
    'Content-Type': "application/json",
    'Authorization': "c4c68964-e234-4067-a0d3-93d673794589"
    }

conn.request("GET", "/v0/contracts/0x5162c16d209340b5c13af4428e30f76f6e567eb1a7837bd9ff800025e9d8cec4?chain=polygon", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

file = open("./images/business_NFT.png", "rb")

response = requests.post(
    "https://api.nftport.xyz/v0/files",
    headers={"Authorization": 'c4c68964-e234-4067-a0d3-93d673794589'},
    files={"file": file}
)
