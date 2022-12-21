from pinata import Pinata
from dotenv import load_dotenv
load_dotenv()
pinata = Pinata(PINATA_API_KEY, PINATA_SECRET_API_KEY, jwt_token)

file = request.files['./images/business_NFT.png']

response = pinata.pin_file(file)
print(response)